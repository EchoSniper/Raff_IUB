import socket

# HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IOT Distribution Line Monitoring System using Raspberry Pi</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #001f3f, #0074D9, #7FDBFF);
            font-family: Arial, sans-serif;
            color: #ffffff;
            overflow-x: hidden;
        }
        .container {
            display: flex;
            align-items: center;
            background-color: rgba(0, 0, 0, 0.6);
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
            width: 100%;
            max-width: 1000px;
            margin: 0;
            flex-direction: column;
            gap: 20px;
        }
        .icon-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        .icon {
            font-size: 6rem;
        }
        h1 {
            font-size: 3.5rem;
            margin-bottom: 15px;
        }
        h2 {
            font-size: 1.8rem;
            margin-bottom: 25px;
            color: #d1d1d1;
        }
        p {
            font-size: 1.5rem;
            margin-bottom: 25px;
        }
        .loading-bar-container {
            position: relative;
            width: 100%;
            background-color: #444;
            border-radius: 15px;
            overflow: hidden;
            height: 40px;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.7);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .loading-bar {
            width: 100%;
            height: 100%;
            background: linear-gradient(to right, #00bfff, #004f8d);
            animation: move-bar 4s linear infinite;
            border-radius: 15px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
        }
        .loading-text {
            margin-top: 10px; /* Added margin to move the text below the bar */
            color: #ffffff;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
        }
        @keyframes move-bar {
            0% {
                transform: translateX(-100%);
            }
            100% {
                transform: translateX(100%);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon-container">
            <div class="icon">ðŸš§</div>
            <div class="icon">ðŸ”§</div>
            <div class="icon">âš™ï¸</div>
        </div>
        <div class="content">
            <h1>IOT Distribution Line Monitoring System using Raspberry Pi</h1>
            <h2>Constructed by "IUB EEE GridGuardians"</h2>
            <p>Raafiu Ashiquzzaman Mahmood, Md. Roman Khan, Taremun Arefin, Salma Islam Mim</p>
        </div>
        <div class="loading-bar-container">
            <div class="loading-bar"></div>
        </div>
        <div class="loading-text">Please Wait, the Website is under construction</div>
    </div>
</body>
</html>
"""

# Server configuration
ip_address = "192.168.68.110"  # Replace with the local IP of the Raspberry Pi or PC
port = 12345  # Port to host the server

def start_server():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(5)  # Listen for up to 5 connections
    print(f"Server running at http://{ip_address}:{port}")

    while True:
        # Accept incoming connections
        client_socket, client_addr = server_socket.accept()
        print(f"Connection received from {client_addr}")

        # Read the request (for demonstration, ignoring the request content)
        request = client_socket.recv(1024).decode('utf-8')
        print(request)

        # Send HTTP response
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
        client_socket.sendall(response.encode('utf-8'))

        # Close the client connection
        client_socket.close()

# Start the server
start_server()
