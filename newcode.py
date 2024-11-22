import serial
import csv
import time

# Set the serial port and baud rate (same as Arduino)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Change the port to your device's port
time.sleep(2)  # Wait for Arduino to initialize

# Open a CSV file in write mode
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Sensor Value', 'Timestamp'])  # CSV header

    try:
        while True:
            # Read a line of data from Arduino, decode it, and strip extra spaces
            data = ser.readline().decode('utf-8').strip()

            if data:
                # Split the data into two parts based on space (or use another delimiter if needed)
                values = data.split()  # Assumes space separation or modify this as needed

                if len(values) == 2:
                    # Write sensor value and timestamp to CSV
                    writer.writerow(values)
                    print(f"Data saved: {values[0]}, {values[1]}")
                else:
                    print(f"Invalid data format: {data}")
    except KeyboardInterrupt:
        print("Data collection stopped.")
    finally:
        ser.close()
