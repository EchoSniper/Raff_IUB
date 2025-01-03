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
    "Phase_C_Current": 0.0
}

# HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Distribution Line Monitoring System</title>
    <style>
        /* Your CSS content as provided earlier */
    </style>
</head>
<body>
    <div class="container">
        <!-- Your HTML content as provided earlier -->
    </div>
    <script>
        /* Your JavaScript content as provided earlier */
    </script>
</body>
</html>
"""

# Web server configuration
ip_address = "192.168.68.110"  # Replace with your desired IP
port = 2010

def read_serial_data():
    """Continuously read data from the Arduino and update the global sensor_data dictionary."""
    global sensor_data
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        print("Connected to Arduino...")
        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
                if not line:
                    continue
                
                print(f"Received data: {line}")  # Debug log
                
                # Parse data only if it has 6 comma-separated values
                if line.count(',') == 5:
                    values = list(map(float, line.split(',')))
                    sensor_data.update({
                        "Phase_A_Voltage": values[5],
                        "Phase_A_Current": values[4],
                        "Phase_B_Voltage": values[3],
                        "Phase_B_Current": values[2],
                        "Phase_C_Voltage": values[1],
                        "Phase_C_Current": values[0],
                    })
                else:
                    print(f"Invalid data format: {line}")
            except (ValueError, IndexError) as e:
                print(f"Error parsing data: {e}")
    except serial.SerialException as e:
        print(f"Failed to connect to Arduino: {e}")

def handle_client(client_socket):
    """Handles HTTP requests from clients."""
    try:
        request = client_socket.recv(1024).decode("utf-8")
        if request.startswith('GET /data'):
            response = json.dumps(sensor_data)
            client_socket.sendall(
                f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{response}".encode('utf-8')
            )
        else:
            client_socket.sendall(
                f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}".encode('utf-8')
            )
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_web_server():
    """Starts the web server."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip_address, port))
        server.listen(5)
        print(f"Server running on {ip_address}:{port}...")
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    # Start serial data reading in a separate thread
    threading.Thread(target=read_serial_data, daemon=True).start()
    # Start the web server
    start_web_server()
