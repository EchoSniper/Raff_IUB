import serial
import time

# Set the serial port and baud rate (same as Arduino)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Change the port to your device's port
time.sleep(2)  # Wait for Arduino to initialize

try:
    while True:
        # Read a line of data from Arduino, decode it, and strip extra spaces
        data = ser.readline().decode('utf-8').strip()
        
        # Print the received data
        if data:
            print(f"Received: {data}")
        else:
            print("No data received.")
except KeyboardInterrupt:
    print("Data collection stopped.")
finally:
    ser.close()
