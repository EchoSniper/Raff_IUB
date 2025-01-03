import serial
import socket
import threading
import json
import time

# Serial communication setup
arduino_port = '/dev/ttyUSB0'  # Replace with your port
baud_rate = 9600
sensor_data = {
    "Phase_A_Voltage": 0.0,
    "Phase_A_Current": 0.0,
    "Phase_B_Voltage": 0.0,
    "Phase_B_Current": 0.0,
    "Phase_C_Voltage": 0.0,
    "Phase_C_Current": 0.0,
    "Ground_Current": 0.0  # Added Ground Current for future use
}

# HTML content remains the same...

# Web server configuration
ip_address = "192.168.68.110"  # Listen on all interfaces
port = 2010

def read_serial_data():
    """Continuously read data from the Arduino and update the global sensor_data dictionary."""
    global sensor_data
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print("Connected to Arduino...")
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Received data: {line}")  # For debugging, to see what data is coming in
                
                # Skip lines containing 'Time' or any other non-numeric data
                if 'Time' in line or not line.replace('.', '', 1).isdigit() and not ',' in line:
                    print(f"Skipping invalid line: {line}")
                    continue  # Skip non-numeric lines
                
                try:
                    # Attempt to convert the line to float values
                    values = list(map(float, line.split(",")))
                    
                    if len(values) >= 7:  # Expecting 7 values now (Ground Current, Phase C, B, A currents, and Phase C, B, A voltages)
                        sensor_data["Ground_Current"] = values[0]  # Ground Current
                        sensor_data["Phase_C_Current"] = values[1]
                        sensor_data["Phase_B_Current"] = values[2]
                        sensor_data["Phase_A_Current"] = values[3]
                        sensor_data["Phase_C_Voltage"] = values[4]
                        sensor_data["Phase_B_Voltage"] = values[5]
                        sensor_data["Phase_A_Voltage"] = values[6]
                    else:
                        print(f"Invalid data format: {line}")
                except ValueError as e:
                    print(f"Error processing data: {e} for line: {line}")
    except Exception as e:
        print(f"Failed to connect to Arduino: {e}")

def handle_client(client_socket):
    """Handles the HTTP requests from clients."""
    request = client_socket.recv(1024).decode("utf-8")
    if request.startswith('GET /data'):
        # Return the first 6 values (Phase A, B, C voltages and currents)
        response = json.dumps({
            "Phase_A_Voltage": sensor_data["Phase_A_Voltage"],
            "Phase_A_Current": sensor_data["Phase_A_Current"],
            "Phase_B_Voltage": sensor_data["Phase_B_Voltage"],
            "Phase_B_Current": sensor_data["Phase_B_Current"],
            "Phase_C_Voltage": sensor_data["Phase_C_Voltage"],
            "Phase_C_Current": sensor_data["Phase_C_Current"]
        })
        client_socket.sendall(
            f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{response}".encode('utf-8')
        )
    else:
        client_socket.sendall(
            f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}".encode('utf-8')
        )
    client_socket.close()

def start_web_server():
    """Starts the web server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_address, port))
    server.listen(5)
    print(f"Server running on {ip_address}:{port}...")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    # Start serial data reading in a separate thread
    threading.Thread(target=read_serial_data, daemon=True).start()
    # Start the web server
    start_web_server()
