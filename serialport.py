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
            data = ser.readline().decode('utf-8').strip()  # Read a line of data from Arduino
            if data:
                sensor_value, timestamp = data.split(',')
                writer.writerow([sensor_value, timestamp])  # Write data to CSV file
                print(f"Data saved: {sensor_value}, {timestamp}")
    except KeyboardInterrupt:
        print("Data collection stopped.")
    finally:
        ser.close()
