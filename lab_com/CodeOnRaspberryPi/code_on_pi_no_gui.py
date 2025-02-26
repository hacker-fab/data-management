import gpiod
import time
import requests


## This file is deprecated ##
## Development has continued on the version of this file with GUI support ##
## Please refer to lab_com_gui.py for the latest version of this file ##

IO_PIN = 17  # Change to your GPIO pin number
chip = gpiod.Chip('gpiochip4')
line = chip.get_line(IO_PIN)

# Request the GPIO line for output
line.request(consumer="gpio_test", type=gpiod.LINE_REQ_DIR_OUT)

# Define the base URL as a constant
BASE_URL = "https://fbc4oam2we.execute-api.us-east-2.amazonaws.com/prod"

def get_next_job():
    """
    Fetch the next job from the queue.
    """
    endpoint = f"{BASE_URL}/jobs/next"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching next job: {e}")
        return None

try:
    while True:

        job = get_next_job()
        if job:
            print("Next job:", job)
            job_input_parameters = job.get("input_parameters", {})

            job_id = job.get("job_id", "unknown")

            on_time = 5

            if "time" in job_input_parameters:
                on_time = job_input_parameters["time"]

            line.set_value(1)  # Turn on
            print("GPIO ON")

            print(f"Keeping GPIO on for {on_time} seconds...")

            time.sleep(on_time) 

            line.set_value(0)  # Turn off
            print("GPIO OFF")
            
            print("Job completed. Now, we'll enter a string and send it back to the server.")
            print("Eventually, this will be informaiton from the spincoater (or other device)")
            user_input = input("Please enter a string: ")
            print("User input recorded & sent back to server.")

            # Send the user input back to the server
            endpoint = f"{BASE_URL}/job_completion"
            data = {
                "job_id": job_id,
                "status": "completed",
                "output_parameters": {"user_input": user_input}
            }

            try:
                response = requests.post(endpoint, json=data)
                response.raise_for_status()  # Raise an error for bad status codes
                print("Job completion posted successfully.")
            except requests.exceptions.RequestException as e:
                print(f"Error posting job completion: {e}")

        else:
            print("No job found.")

        time.sleep(5)  # Wait for 5 seconds before checking again



except KeyboardInterrupt:
    print("\nExiting program")
    line.release()  # Release the GPIO line properly