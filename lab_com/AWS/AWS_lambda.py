import boto3
import json
import uuid
import time
import logging
from decimal import Decimal

### This code runs on the AWS instance as a lambda function for managing the API requests ###

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("JobQueue")

def lambda_handler(event, context):
    """
    Handles API requests for different endpoints.
    """
    logger.info("Received event: %s", json.dumps(event, indent=2, default=decimal_serializer))

    # Extract HTTP method and route
    route = event.get("routeKey", "")
    method = event["requestContext"]["http"]["method"]
    body = json.loads(event.get("body", "{}"))  # Parse JSON body safely

    logger.info("Processing route: %s with method: %s", route, method)

    # Routing based on the request
    if route == "GET /jobs/next" and method == "GET":
        return get_next_job()
    elif route == "POST /job_completion" and method == "POST":   # Ensure correct endpoint
        return update_job_completion(body)
    elif route == "POST /jobs" and method == "POST":
        return enqueue_job(body)
    elif route == "GET /jobs_by_id" and method == "GET":
        return get_jobs_by_id(event)
    elif route == "GET /jobs_by_machine" and method == "GET":
        return get_jobs_by_machine(event)
    else:
        logger.warning("Invalid request received: %s", route)
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid request"})}

# **Helper Function to Convert Decimal to Native Python Types**
def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# **1️⃣ Function to Update Job Completion (Completed or Failed)**
def update_job_completion(body):
    job_id = body.get("job_id", "-1")
    logger.info("Received job completion request: %s", body)

    # **Check if job_id is missing, invalid, or set to "-1"**
    if not job_id or not isinstance(job_id, str) or len(job_id) < 8 or job_id == "-1":
        logger.error("Invalid job_id received: %s", job_id)
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid or missing job_id"})}

    # Retrieve the job from DynamoDB to verify it exists
    response = table.get_item(Key={"job_id": job_id})
    if "Item" not in response:
        logger.error("Job ID not found: %s", job_id)
        return {"statusCode": 410, "body": json.dumps({"message": f"Job ID {job_id} not found"})}

    output_parameters = body.get("output_parameters", {})
    status = body.get("status", "").capitalize()
 
    if status not in ["Completed", "Failed"]:
        logger.error("Invalid status received: %s", status)
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid status, must be 'Completed' or 'Failed'"})}

    timestamp = int(time.time())
    table.update_item(
        Key={"job_id": job_id},
        UpdateExpression="SET #s = :s, output_parameters = :o, #t = :t",
        ExpressionAttributeNames={"#s": "status", "#t": "timestamp"},
        ExpressionAttributeValues={":s": status, ":o": output_parameters, ":t": timestamp}
    )

    logger.info("Job %s updated to %s", job_id, status)
    return {"statusCode": 200, "body": json.dumps({"message": f"Job {job_id} marked as {status}."})}

# **2️⃣ Function to Add a New Job**
def enqueue_job(body):
    job_id = str(uuid.uuid4())
    machine = body.get("machine", "unknown")
    input_parameters = body.get("input_parameters", {})
    priority = body.get("priority", 1)
    timestamp = int(time.time())
    logger.info("Adding new job with ID: %s", job_id)

    table.put_item(Item={
        "job_id": job_id,
        "machine": machine,
        "status": "Pending",
        "input_parameters": input_parameters,
        "output_parameters": {},
        "timestamp": timestamp,
        "priority": priority
    })

    return {"statusCode": 200, "body": json.dumps({"message": "Job added", "job_id": job_id})}

# **3️⃣ Function to Get the Next Pending Job and Mark It "In Progress", Then Return Updated Data**
def get_next_job():
    logger.info("Fetching next job from queue")
    response = table.scan(
        FilterExpression="#s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "Pending"}
    )

    jobs = response.get("Items", [])
    if not jobs:
        logger.warning("No pending jobs found")
        return {"statusCode": 404, "body": json.dumps({"message": "No pending jobs found"})}

    jobs.sort(key=lambda x: x.get("priority", 1), reverse=True)
    next_job = jobs[0]
    logger.info("Next job selected: %s", next_job["job_id"])

    table.update_item(
        Key={"job_id": next_job["job_id"]},
        UpdateExpression="SET #s = :s, #t = :t",
        ExpressionAttributeNames={"#s": "status", "#t": "timestamp"},
        ExpressionAttributeValues={":s": "In Progress", ":t": int(time.time())}
    )

    updated_job = table.get_item(Key={"job_id": next_job["job_id"]}).get("Item", {})
    logger.info("Updated job details: %s", updated_job)

    return {"statusCode": 200, "body": json.dumps(updated_job, default=decimal_serializer)}

def get_jobs_by_id(event):
    """
    Fetch a job by its ID.
    """
    job_id = event.get("queryStringParameters", {}).get("job_id")
    
    if not job_id:
        return {"statusCode": 400, "body": json.dumps({"message": "Missing job_id parameter"})}
    
    response = table.get_item(Key={"job_id": job_id})
    
    if "Item" not in response:
        return {"statusCode": 404, "body": json.dumps({"message": "Job not found"})}
    
    return {"statusCode": 200, "body": json.dumps(response["Item"], default=decimal_serializer)}

def get_jobs_by_machine(event):
    """
    Fetch jobs by machine.
    """
    machine = event.get("queryStringParameters", {}).get("machine")
    
    if not machine:
        return {"statusCode": 400, "body": json.dumps({"message": "Missing machine parameter"})}
    
    response = table.scan(
        FilterExpression="#m = :m",
        ExpressionAttributeNames={"#m": "machine"},
        ExpressionAttributeValues={":m": machine}
    )
    
    jobs = response.get("Items", [])
    if not jobs:
        return {"statusCode": 404, "body": json.dumps({"message": "No jobs found for the specified machine"})}
    
    return {"statusCode": 200, "body": json.dumps(jobs, default=decimal_serializer)}

# **Helper Function to Convert Decimal to Native Python Types**
def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")