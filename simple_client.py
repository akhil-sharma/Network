import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9999))

b = "infinity"
count = 0
while True:
    client_socket.send(b.encode())
    data = client_socket.recv(512)

    if data:
        print(data)

    if data == "infinity":
        client_socket.close()
    count += 1
    if count > 10:
        client_socket.close()