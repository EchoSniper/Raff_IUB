#This code is CHATGPT Oritentated, modification isn't brought yet. 
#This code will be used for Data Acquisition  into a CSV File for further analysis 
import serial
import csv
import time

# Set the serial port and baud rate (same as Arduino)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Change to your device's port (e.g., 'COM3' on Windows)
time.sleep(2)  # Wait for Arduino to initialize

# Open a CSV file in write mode (this will create a new file)
with open('temperature_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write a header to the CSV file
    writer.writerow(['Temperature (Celsius)'])  # Column header
    
    try:
        while True:
            # Read a line of data from Arduino, decode it, and strip extra spaces
            data = ser.readline().decode('utf-8').strip()

            # Debugging: print the raw data received from Arduino
            print(f"Raw Data: '{data}'")

            if data:
                try:
                    # Store the data (temperature value) in a variable
                    temperature_value = float(data)  # Convert to float
                    print(f"Temperature Value: {temperature_value} Â°C")  # Print the temperature value

                    # Write the temperature value to the CSV file
                    writer.writerow([temperature_value])  # Write only the temperature value
                    print(f"Data saved: {temperature_value} Â°C")

                    # Debug: Ensure data is being flushed after writing
                    file.flush()
                except ValueError:
                    print(f"Invalid temperature value received: {data}")
            else:
                print("No data received.")
            
            # Optional: delay between readings (if needed)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Data collection stopped.")
    finally:
        ser.close()
        print("Serial connection closed.")

