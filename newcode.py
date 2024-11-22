import serial
import csv
import time
from datetime import datetime
import pywt  # PyWavelets library for wavelet transforms
import numpy as np

# Set the serial port and baud rate (same as Arduino)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Change the port to your device's port
time.sleep(2)  # Wait for Arduino to initialize

# Open a CSV file in write mode
with open('data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Sensor Value', 'Timestamp', 'Wavelet Coefficients'])  # CSV header

    try:
        while True:
            data = ser.readline().decode('utf-8').strip()  # Read a line of data from Arduino
            print(f"The Temperature is : {data}")

    except KeyboardInterrupt:
        print("Data collection stopped.")
    finally:
        ser.close()


