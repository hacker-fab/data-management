"""
This module contains the GUI for the job queue system.
"""

import uuid
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

########################## EDIT HERE: PERIPHERAL CONFIGURATION ##########################
#### INSTRUCTIONS: ######
### Add whatever code you need here to inintialize your peripherals so that they can begin to accept jobs. ###

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

#########################################################################################


def get_next_job():
    """Fetch the next job from the queue."""
    endpoint = f"{BASE_URL}/jobs/next"
    params = {"machine": JOB_NAME}
    try:
        response = requests.get(endpoint, params=params)
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
    def __init__(self, root, job_function):
        """Initialize the JobGUI class."""

        # Google code guidelines recommend fewer class variables
        # (I have 17+, they recommend 7 or fewer)
        # However, I believe this is the most
        # efficient way to manage the GUI

        self.root = root
        self.job_function = job_function  # Store the function pointer
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


        # create GUI elements for manually entering job parameters based on JOB_PARAM_TEMPLATE
        self.job_param_entries = {}
        for param_name, param_value in JOB_PARAM_TEMPLATE.items():
            label = ttk.Label(root, text=f"{param_name}:")
            label.pack()
            label.pack_forget()
            entry = ttk.Entry(root) 
            entry.insert(0, str(param_value))
            entry.pack()
            entry.pack_forget()
            self.job_param_entries[param_name] = {"label" : label, "entry" : entry}


        self.create_new_job_button = ttk.Button(root, text="Create New Job",
                                        command=self.create_new_job)
        
        self.create_new_job_button.pack()

        self.create_new_job_submit = ttk.Button(root, text="Submit New Job",
                                        command=self.submit_new_job)
        
        self.create_new_job_submit.pack()
        self.create_new_job_submit.pack_forget()


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

        # Use the function pointer to run the job
        threading.Thread(target=self.job_function,
                         args=(self, job_input_parameters,), daemon=True).start()

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

    def create_new_job(self):
        """Handles the button click to bring up the option to create a new job."""
        self.system_status_label.config(text="System Status: Enter new job parameters...")

        # Show the job parameter entries
        for entry in self.job_param_entries.values():
            entry["label"].pack()
            entry["entry"].pack()

        self.create_new_job_button.pack_forget()
        self.create_new_job_submit.pack()

    def submit_new_job(self):
        """Submit the new job after the user has entered the parameters."""
        self.system_status_label.config(text="System Status: Submitting new job...")

        # Hide the job parameter entries
        for entry in self.job_param_entries.values():
            entry["label"].pack_forget()
            entry["entry"].pack_forget()

        self.create_new_job_button.pack()
        self.create_new_job_submit.pack_forget()

        # Get the job parameters from the entries
        job_input_parameters = {}
        for param_name, entry in self.job_param_entries.items():
            job_input_parameters[param_name] = entry["entry"].get()

        # Submit the job to the server
        endpoint = f"{BASE_URL}/jobs"
        data = {
            "machine": JOB_NAME,
            "input_parameters": job_input_parameters
        }

        print("Submitting job:", data)

        try:
            response = requests.post(endpoint, json=data)
            response.raise_for_status()
            print("Job posted successfully.")
            self.system_status_label.config(text="System Status: Job submitted.")
        except requests.exceptions.RequestException as err:
            print(f"Error posting job: {err}")
            self.system_status_label.config(text="System Status: Error submitting. Now running job locally.")
            
            self.job = {"input_parameters": job_input_parameters, "machine": JOB_NAME, "status": "In Progress", "timestamp": 0, "output_parameters": {}, "priority": "1", "job_id": str(uuid.uuid4()) + "-local"}
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


    ########################## EDIT HERE: PERIPHERAL CONFIGURATION ##########################
    ##### INSTRUCTIONS #######

    ### Write a function in this locaiton that will run the job. ###
    ### This function will be called when the job is approved. ###
    ### The function will be passed the job input parameters. ###

    ### to get started, copy the run_led function and edit it to run your job. ###
    ### only edit the code in between FIRMWARE START and FIRMWARE END ###
    ### This is where you will write the code to run your job. ###

    ### If you want the user to type in a response, leave the following two lines for gathering the response. ###
    ### If you don't want the user to type in a response, remove the two lines. ###

    #### This is the function that will be edited to integrate new tools #####
    def run_led(self, job_input_parameters):
        """Run the LED job."""

        ### FIRMWARE START: This is where you write the firmware code to run the job. ##
        line.set_value(1)  # Turn on GPIO
        self.set_job_status_label("Job Status: GPIO: ON")

        duration = job_input_parameters.get("time", 5)
        for i in range(duration, 0, -1):
            self.set_job_status_label(f"Job Status: GPIO: ON, Time remaining: {i} seconds")
            time.sleep(1)

        line.set_value(0)  # Turn off GPIO

        ### FIRMWARE END ###

        ## Gather the user response [Optional, you can remove]##
        self.set_job_status_label("Job Status: GPIO: OFF. Please type in response.")
        self.get_user_output_response()

        ## Submit the data back to the server ##
        final_output_parameters = {"response": self.output_text}
        self.submit_completed_response_to_server(final_output_parameters)

    def run_spincoater(self, job_input_parameters):
        """Run the spincoater job."""

        print("Job input parameters:", job_input_parameters)

        ### This is where you write the firmware code to run the job. ##
        rpm = job_input_parameters.get("rpm", 1000)
        duration = job_input_parameters.get("time", 5)

        # Send RPM command
        rpm_command = f"RPM:{rpm}\n"
        print(f"Sending: {rpm_command.strip()}")
        ser.write(rpm_command.encode())
        time.sleep(0.5)  # Small delay to ensure command is processed

        # Send Time command
        time_command = f"TIME:{duration}\n"
        print(f"Sending: {time_command.strip()}")
        ser.write(time_command.encode())
        time.sleep(0.5)  # Small delay to ensure command is processed

        # Turn on the compressor and give it time to stabilize
        line.set_value(1)  # Turn on GPIO
        print("Compressor turned on.")
        time.sleep(2)  # Allow time for the compressor to stabilize

        # Send Start command
        start_command = "START\n"
        print(f"Sending: {start_command.strip()}")
        ser.write(start_command.encode())

        run_result = "JOB FAILED"

        # Read response from Arduino
        while True:
            response = ser.readline().decode('utf-8').strip()
            if response:
                print(f"Arduino: {response}")
                if ("**SPIN JOB COMPLETED SUCCESSFULLY**" in response):
                    run_result = "JOB COMPLETED"
            else:
                break  # Stop reading when no more data

        # Turn off the compressor
        line.set_value(0)  # Turn off GPIO
        print("Compressor turned off.")

        ### End of firmware code. ###

        ## Submit the data back to the server ##
        final_output_parameters = {"response": run_result}

        self.submit_completed_response_to_server(final_output_parameters)


    ##########################################################################################


########################## EDIT HERE: JOB OBJECT FORMAT ######################################
#### INSTRUCTIONS: ####
### In this section, to integrate a new tool, you must create three new variables ###
### These will be used to know which function to call when the job is run. ###
### The variables are: ###
### 1. JOB_PARAM_TEMPLATE: This is the template for the job parameters. ###
###    It should be a dictionary with the same keys as the job parameters. ###
###    The values should be the default values for the job parameters. ###
### 2. JOB_NAME: This is the name of the job. ###
###    It should be the same as the name of the job in the server. ###
###    It will be used to identify which jobs to fetch from the server###
### 3. JOB_FUNCTION: This is the function that will be called to run the job. ###
###    It should be the function that you wrote to run the job. ###

#### It is imperative that the job object format matches the server's object format ####

#### SPINCOATER JOB ####
SPINCOATER_JOB_PARAM_TEMPLATE = { "time": 12, "rpm": 1100 }
SPINCOATER_JOB_NAME = "spincoater"
SPINCOATER_FUNCTION = JobGUI.run_spincoater


#### LED JOB ####
LED_JOB_PARAM_TEMPLATE = { "time": 5 }
LED_JOB_NAME = "led"
LED_FUNCTION = JobGUI.run_led


### Edit the following variables to match the job type you are integrating ###
JOB_PARAM_TEMPLATE = SPINCOATER_JOB_PARAM_TEMPLATE
JOB_NAME = SPINCOATER_JOB_NAME
JOB_FUNCTION = SPINCOATER_FUNCTION

###########################################################################################


if __name__ == "__main__":
    root = tk.Tk()
    gui = JobGUI(root, JOB_FUNCTION)  # Pass JOB_FUNCTION to the GUI
    try:
        root.mainloop()
    except KeyboardInterrupt:
        gui.stop()
        ser.close()
        line.release()
        print("Exiting program")
