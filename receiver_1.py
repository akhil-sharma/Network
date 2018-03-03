import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9999))

b = "receiver"
count = 0
while True:
    try:
        client_socket.send(b.encode())
        data = client_socket.recv(512)
    except OSError:
        print("error")

    if data:
        print(data, count)

    count += 1
    if count > 10:
        break

client_socket.shutdown(socket.SHUT_RDWR)
client_socket.close()
