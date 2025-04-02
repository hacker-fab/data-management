"""
This module contains examples of a few endpoint calls
"""
import requests

# Constants
BASE_URL = "https://fbc4oam2we.execute-api.us-east-2.amazonaws.com/prod"

def test_jobqueue_api():
    """
    Test the job queue API endpoints.
    """
    # Step 1: POST /jobs - Enqueue a new job
    job_data = {
        "machine": "lithographer",
        "input_parameters": {"x": 100.0, "y": 200.0, "image": "foo.png"},
        "priority": 2
    }
    response = requests.post(f"{BASE_URL}/jobs", json=job_data)
    assert response.status_code == 200, "Failed to enqueue job"
    job_id = response.json().get("job_id")
    print(f"Job enqueued: {job_id}")

   

    # Step 4: GET /jobs/next - Fetch job from queue
    response = requests.get(f"{BASE_URL}/jobs/next", params={"machine": "lithographer"})
    assert response.status_code == 200, "Failed to fetch next job"
    assert response.json().get("job_id") == job_id, "Fetched wrong job"
    print("Job fetched successfully")
    

if __name__ == "__main__":
    test_jobqueue_api()
