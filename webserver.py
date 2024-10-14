import socket
import sys
import os

s = socket.socket()
port = 27333
if len(sys.argv) >= 2:
    port = int(sys.argv[1])
connection = ('', port)
content_type = "text/plain"
content = " "
s.bind(connection)
s.listen()
while True:
    new_conn = s.accept()
    print(new_conn)
    new_socket = new_conn[0]

    data = b""
    while b'\r\n\r\n' not in data:
        data += new_socket.recv(40)
        decoded = data.decode()
        print(decoded, end="")
        if decoded[:3] == "GET":
            request = decoded.split()
            print(" ")
            print(request[1])
            print(request[2])
            file_name = request[1].split("/")[-1]
            print(file_name)
            file_path = os.path.splitext(file_name)[1]
            if file_path == ".txt":
                content_type = "text/play"
            elif file_path == ".html":
                content_type = "text/html"
            try:
                with open(file_name, "rb") as fp:
                    content = fp.read()  # Read entire file
            except:
                # File not found or other error
                message = "HTTP/1.1 404 Not Found\r\nContent-Type: " + content_type + "\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found"""

    if message == None:
        message = "HTTP/1.1 200 OK\r\nContent-Type: " + content_type + "\r\nContent-Length: 6\r\nConnection: close\r\n\r\n"""
        message += content
    new_socket.sendall(message.encode())
    new_socket.close()