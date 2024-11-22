import serial
import csv
import time

# Set the serial port and baud rate (same as Arduino)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Change the port to your device's port
time.sleep(2)  # Wait for Arduino to initialize

# Open a CSV file in write mode (this will create a new file)
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    try:
        while True:
            # Read a line of data from Arduino, decode it, and strip extra spaces
            data = ser.readline().decode('utf-8').strip()

            # Debugging: print the raw data received from Arduino
            print(f"Received Data: {data}")

            if data:
                # Write the data (sensor value) directly to the CSV file
                writer.writerow([data])  # Writing only the sensor value
                print(f"Data saved: {data}")
            else:
                print("No data received.")
    except KeyboardInterrupt:
        print("Data collection stopped.")
    finally:
        ser.close()
