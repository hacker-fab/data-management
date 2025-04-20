import requests

JOB_QUEUE_BASE_URL = "https://fbc4oam2we.execute-api.us-east-2.amazonaws.com/prod"

def get_file_upload_url_and_key(job_id):
    """
    Generate a presigned URL for uploading an image.
    """
    response = requests.post(f"{JOB_QUEUE_BASE_URL}/generate_upload_url", json={"job_id": job_id})
    assert response.status_code == 200, "Failed to generate upload URL"
    upload_url = response.json().get("upload_url")
    s3_key = response.json().get("s3_key")
    
    print(f"Upload URL: {upload_url}")
    return upload_url, s3_key


def upload_file(file_obj, upload_url):
    """
    Upload a file object to the presigned URL.
    """
    try:
        # Use the file object directly (e.g., from request.FILES in views.py)
        response = requests.put(upload_url, data=file_obj)
        if response.status_code != 200:
            print(f"Upload failed. Status code: {response.status_code}, response: {response.text}")
        assert response.status_code == 200, "Upload failed"
        print("File uploaded successfully")
    except Exception as e:
        print(f"Error during file upload: {str(e)}")
        raise


def enqueue_job(machine, input_parameters, priority):
    """
    Enqueue a job with the specified parameters.
    """
    job_data = {
        "machine": machine,
        "input_parameters": input_parameters,
        "priority": priority
    }
    response = requests.post(f"{JOB_QUEUE_BASE_URL}/jobs", json=job_data)
    job_id = response.json().get("job_id")
    print(f"Job enqueued: {job_id}")
    return response, job_id
