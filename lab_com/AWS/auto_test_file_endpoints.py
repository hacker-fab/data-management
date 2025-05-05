"""
This module contains examples of a few endpoint calls
"""
import requests

# Constants
BASE_URL = "https://fbc4oam2we.execute-api.us-east-2.amazonaws.com/prod"

TEST_FILE_NAME = "PNG_test.png"  # Replace with the path to your test file


def get_file_upload_url_and_key(job_id):
    """
    Generate a presigned URL for uploading an image.
    """
    response = requests.post(f"{BASE_URL}/generate_upload_url", json={"job_id": job_id})
    assert response.status_code == 200, "Failed to generate upload URL"
    upload_url = response.json().get("upload_url")
    s3_key = response.json().get("s3_key")

    print(f"Upload URL: {upload_url}")
    return upload_url, s3_key


def upload_file(file_name, upload_url):
    """
    Upload a file to the presigned URL.
    """
    with open(file_name, "rb") as file:
        response = requests.put(upload_url, data=file)
    if response.status_code != 200:
        print(f"Upload failed. Status code: {response.status_code}, response: {response.text}")
    assert response.status_code == 200, "Upload failed"
    print("File uploaded successfully")



def enqueue_job(machine, input_parameters, priority):
    """
    Enqueue a job with the specified parameters.
    """
    job_data = {
        "machine": machine,
        "input_parameters": input_parameters,
        "priority": priority
    }
    response = requests.post(f"{BASE_URL}/jobs", json=job_data)
    assert response.status_code == 200, "Failed to enqueue job"
    job_id = response.json().get("job_id")
    print(f"Job enqueued: {job_id}")
    return job_id

def download_file(s3_key):
    """
    Download a file from S3 using the presigned URL.
    """

    # get the presigned URL for download
    response = requests.post(f"{BASE_URL}/generate_download_url", json={"s3_key": s3_key})
    assert response.status_code == 200, "Failed to generate download URL"
    download_url = response.json().get("download_url")
    print(f"Download URL: {download_url}")

    # download the file using the presigned URL
    response = requests.get(download_url)
    if response.status_code != 200:
        print(f"Failed to download file. Status code: \
              {response.status_code}, Response text: {response.text}")
    assert response.status_code == 200, "Failed to download file"
    with open("downloaded-" + TEST_FILE_NAME, "wb") as file:
        file.write(response.content)

def test_upload_and_download_file():
    """
    Test uploading a file, providing the S3 key as a job parameter, fetching the job,
    and then downloading the file using the presigned URLs.
    """
    # Step 1: Generate a presigned upload URL and S3 key
    # Passing None as job_id since it's not required here
    upload_url, s3_key = get_file_upload_url_and_key(None)
    print(f"Generated upload URL: {upload_url}")
    print(f"S3 Key: {s3_key}")

    # Step 2: Upload a file
    upload_file(TEST_FILE_NAME, upload_url)
    print(f"File uploaded successfully to S3 key: {s3_key}")

    # Step 3: Enqueue a job with the S3 key as a parameter
    job_id = enqueue_job(
        machine="lithographer",
        input_parameters={"x": 100.0, "y": 200.0, "image_s3_key": s3_key},
        priority=2
    )
    print(f"Job enqueued: {job_id}")

    # Step 4: Fetch the job from the queue
    response = requests.get(f"{BASE_URL}/jobs/next", params={"machine": "lithographer"})
    assert response.status_code == 200, "Failed to fetch next job"
    fetched_job = response.json()
    assert fetched_job.get("job_id") == job_id, "Fetched wrong job"
    fetched_s3_key = fetched_job["input_parameters"]["image_s3_key"]
    print(f"Fetched job successfully. S3 Key: {fetched_s3_key}")

    # Step 5: Download the file using the fetched S3 key
    download_file(fetched_s3_key)
    print("File downloaded successfully.")

if __name__ == "__main__":
    test_upload_and_download_file()
