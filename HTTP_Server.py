import socket
import os
import mimetypes

def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")
    
    # Extract the requested file path
    try:
        request_line = request.splitlines()[0]
        file_path = request_line.split()[1]
    except IndexError:
        return
    
    if file_path == '/':
        file_path = 'index.html'
    else:
        file_path = file_path[1:]  # Remove leading '/'

    if os.path.exists(file_path) and not os.path.isdir(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
        content_type, _ = mimetypes.guess_type(file_path)
        response_headers = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n"
    else:
        content = b"<html><body><h1>404 Not Found</h1></body></html>"
        response_headers = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n"

    # Send headers and content
    client_socket.send(response_headers.encode('utf-8'))
    client_socket.send(content)
    client_socket.close()

def start_server(port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server started, listening on port {port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_request(client_socket)

if __name__ == "_main_":
    start_server()