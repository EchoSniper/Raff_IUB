import serial
import csv
import time

# Set up the serial connection
arduino_port = '/dev/ttyUSB0'  # Adjust this based on your Raspberry Pi's port
baud_rate = 9600
output_file = 'temperature_data.csv'

# Initialize the serial connection
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to Arduino on {arduino_port}")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    exit()

# Open the CSV file for writing
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    try:
        print("Reading data from Arduino...")
        while True:
            # Read a line from the serial port
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Split the line into individual values
                try:
                    values = list(map(float, line.split(",")))  # Parse all values
                    writer.writerow(values)  # Write all values to the CSV file
                    file.flush()  # Ensure the data is immediately written to the file
                    print(f"Received data: {values}")
                except ValueError:
                    print(f"Invalid data received: {line}")
            time.sleep(1)  # Adjust delay if necessary
    except KeyboardInterrupt:
        print("\nStopping data logging.")
    finally:
        ser.close()
        print(f"Data saved to {output_file}.")
