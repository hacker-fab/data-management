import serial
import time

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
    exit()

while True:
    try:
        duration = input("\n Enter LED duration (seconds): ")
        if not duration.isdigit():
            print("Invalid input! Please enter a number.")
            continue

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

    except KeyboardInterrupt:
        print("\n Exiting...")
        ser.close()
        break
