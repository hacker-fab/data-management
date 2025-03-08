"""
This module contains the GUI for the job queue system.
"""

import time
import threading
import tkinter as tk
from tkinter import ttk
import sys
import requests
import gpiod
import serial

IO_PIN = 17  # Change to your GPIO pin number
chip = gpiod.Chip('gpiochip4')
line = chip.get_line(IO_PIN)

# Request the GPIO line for output
line.request(consumer="gpio_test", type=gpiod.LINE_REQ_DIR_OUT)

BASE_URL = "https://fbc4oam2we.execute-api.us-east-2.amazonaws.com/prod"

########################## PERIPHERAL CONFIGURATION ##########################
#### UART OVER USB SERIAL TO ARDUINO ####
# This may be different on a different RPI
USB_PORT = "/dev/ttyACM0"  # Adjust this based on your device
BAUD_RATE = 115200  # Must match Arduino

# Open Serial Connection
try:
    ser = serial.Serial(USB_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow time for connection to stabilize
    print("Connected to Arduino over USB Serial!")
except serial.SerialException:
    print("ERROR: Could not open serial port. Check USB connection!")
    sys.exit()

###################################################################################



def get_next_job():
    """Fetch the next job from the queue."""
    endpoint = f"{BASE_URL}/jobs/next"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error fetching next job: {err}")
        return None

def send_job_completion(job_id, output_parameters):
    """Send job completion data to the server."""
    endpoint = f"{BASE_URL}/job_completion"
    data = {
        "job_id": job_id,
        "status": "completed",
        "output_parameters": output_parameters
    }
    try:
        response = requests.post(endpoint, json=data)
        response.raise_for_status()
        print("Job completion posted successfully.")
    except requests.exceptions.RequestException as err:
        print(f"Error posting job completion: {err}")

class JobGUI:
    """Class to manage the GUI for the job queue system."""
    def __init__(self, root):
        """Initialize the JobGUI class."""

        # Google code guidelines recommend fewer class variables
        # (I have 17, they recommend 7 or fewer)
        # However, I believe this is the most
        # efficient way to manage the GUI

        self.root = root
        self.root.title("Job Monitor")

        self.auto_run = tk.BooleanVar(value=True)

        self.auto_run_switch = ttk.Checkbutton(root, text="Auto-run Jobs",
                                               variable=self.auto_run,
                                               command=self.toggle_approve_deny_buttons)
        self.auto_run_switch.pack()

        self.job_id_label = ttk.Label(root, text="Current Job ID: ", font=("Arial", 14))
        self.job_id_label.pack()
        self.job_id_label.pack_forget()

        self.system_status_label = ttk.Label(root,
                                             text="System Status: Waiting for job...",
                                             font=("Arial", 14))
        self.system_status_label.pack()

        self.input_param_label = ttk.Label(root, text="Input parameters: ",
                                           font=("Arial", 14))
        self.input_param_label.pack()
        self.input_param_label.pack_forget()

        self.job_status = ttk.Label(root, text="Job Status: LED OFF",
                                    font=("Arial", 14))
        self.job_status.pack()
        self.job_status.pack_forget()

        self.approve_button = ttk.Button(root, text="Approve Job",
                                         command=self.run_job)
        self.approve_button.pack()
        self.approve_button.pack_forget()

        self.deny_button = ttk.Button(root, text="Deny Job",
                                      command=self.deny_job)
        self.deny_button.pack()
        self.deny_button.pack_forget()

        self.input_label = ttk.Label(root, text="Enter response:",
                                     font=("Arial", 14))
        self.input_entry = ttk.Entry(root, font=("Arial", 14))
        self.input_entry.bind("<Return>",
                              lambda event: self.submit_textbox_response())
        self.submit_button = ttk.Button(root, text="Submit",
                                        command=self.submit_textbox_response)

        self.input_label.pack_forget()
        self.input_entry.pack_forget()
        self.submit_button.pack_forget()

        self.job = None
        self.job_running_on_machine = False
        self.running = True
        self.output_text = None
        self.output_text_avail_semaphore = threading.Semaphore(0)
        self.check_for_jobs()

    def check_for_jobs(self):
        """Check for new jobs in the queue."""
        if self.running:
            job = get_next_job()
            if job:
                self.job = job
                self.job_id_label.config(
                    text=f"Current Job ID: {self.job.get('job_id', 'unknown')}")
                self.job_id_label.pack()
                self.input_param_label.config(
                    text=f"Input Params: {self.job.get('input_parameters', {})}")
                self.input_param_label.pack()
                if self.auto_run.get():
                    self.run_job()
                else:
                    self.system_status_label.config(
                        text="System Status: Job available. Approve or Deny?")
                    self.approve_button.pack()
                    self.deny_button.pack()
            else:
                self.root.after(5000, self.check_for_jobs)

    def toggle_approve_deny_buttons(self):
        """Toggle the visibility of approve and deny buttons."""
        if self.auto_run.get():
            self.approve_button.pack_forget()
            self.deny_button.pack_forget()

            # we also want the job to run automatically if we just
            # turned on auto-run and the job was already loaded into memory.
            self.run_job()
        elif self.job and not self.job_running_on_machine:
            self.approve_button.pack()
            self.deny_button.pack()

    def run_job(self):
        """Run the current job."""
        if not self.job:
            return

        self.approve_button.pack_forget()
        self.deny_button.pack_forget()

        job_input_parameters = self.job.get("input_parameters", {})
        self.system_status_label.config(text="System Status: Running job...")
        self.job_running_on_machine = True

        threading.Thread(target=self.run_spincoater,
                         args=(job_input_parameters,), daemon=True).start()

    def deny_job(self):
        """Deny the current job."""
        if self.job:
            send_job_completion(self.job["job_id"], {"info": "job_skipped"})
            self.system_status_label.config(
                text="System Status: Job Denied. Waiting for next job...")
            self.approve_button.pack_forget()
            self.deny_button.pack_forget()
            self.job_id_label.pack_forget()
            self.input_param_label.pack_forget()
            self.root.after(5000, self.check_for_jobs)

    def submit_textbox_response(self):
        """Submit the response from the textbox."""
        user_input = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        self.input_label.pack_forget()
        self.input_entry.pack_forget()
        self.submit_button.pack_forget()
        self.system_status_label.config(text="System Status: Text submitted...")
        self.output_text = user_input
        self.output_text_avail_semaphore.release()

    def submit_completed_response_to_server(self, output_parameters):
        """Submit the completed job response to the server."""
        if self.job:
            send_job_completion(self.job["job_id"], output_parameters)
            self.job = None
            self.job_id_label.pack_forget()
            self.job_id_label.config(text="Current Job ID: ")
            self.system_status_label.config(text="System Status: Waiting for job...")
            self.input_param_label.pack_forget()
            self.input_param_label.config(text="Input Parameters: ")
            self.job_status.pack_forget()
            self.job_status.config(text="Job Status:")
            self.job_running_on_machine = False
            self.toggle_approve_deny_buttons()
            self.root.after(5000, self.check_for_jobs)

    def stop(self):
        """Stop the GUI and release resources."""
        self.running = False
        line.release()

    def set_job_status_label(self, text):
        """Set the job status label text."""
        self.job_status.config(text=text)
        self.job_status.pack()

    def get_user_output_response(self):
        """Get the user output response."""
        self.input_label.pack()
        self.input_entry.pack()
        self.submit_button.pack()

        # we need to wait until the user has submitted a response...

        # this introduces a pylint warning, but it is necessary to
        # format the program in this way for better readability
        self.output_text_avail_semaphore.acquire()


    ##### ONLY EDIT THIS FUNCTION IF INTEGRATING A NEW TOOL ##################
    #### This is the function that will be edited to integrate new tools #####
    def run_led(self, job_input_parameters):
        """Run the LED job."""

        ### This is where you write the firmware code to run the job. ##
        line.set_value(1)  # Turn on GPIO
        self.set_job_status_label("Job Status: GPIO: ON")

        duration = job_input_parameters.get("time", 5)
        for i in range(duration, 0, -1):
            self.set_job_status_label(f"Job Status: GPIO: ON, Time remaining: {i} seconds")
            time.sleep(1)

        line.set_value(0)  # Turn off GPIO

        ### End of firmware code. ###

        ## Gather the user response [Optional]##
        self.set_job_status_label("Job Status: GPIO: OFF. Please type in response.")
        self.get_user_output_response()

        ## Submit the data back to the server ##
        final_output_parameters = {"response": self.output_text}
        self.submit_completed_response_to_server(final_output_parameters)

    def run_spincoater(self, job_input_parameters):
        """Run the spincoater job."""

        ### This is where you write the firmware code to run the job. ##
        duration = job_input_parameters.get("time", 5)
        command = f"LED:{duration}\n"
        print(f"Sending: {command.strip()}")
        ser.write(command.encode())  # Send data over USB Serial

        # Read response from Arduino
        while True:
            response = ser.readline().decode('utf-8').strip()
            if response:
                print(f"Arduino: {response}")
            else:
                break  # Stop reading when no more data

        ### End of firmware code. ###


        ## Gather the user response [Optional]##
        self.set_job_status_label("Job Status: GPIO: OFF. Please type in response.")

        self.get_user_output_response()

        ## Submit the data back to the server ##
        final_output_parameters = {"response": self.output_text}

        self.submit_completed_response_to_server(final_output_parameters)


    ###########################################################################



if __name__ == "__main__":
    root = tk.Tk()
    gui = JobGUI(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        gui.stop()
        ser.close()
        line.release()
        print("Exiting program")
