import socket
import threading

count = 0
class ThreadedServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.shutdown(socket.)

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(10)
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        global count
        print(count)
        count += 1
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    response = (data.decode() + "akhil").encode()
                    print(data, end=" ")
                    client.send(response)
                else:
                    pass
            except OSError as e:
                client.close()
                return False


if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer("127.0.0.1", port_num).listen()

  def get_packets(self):
        print("Listening for packets....")
        message = {}
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    packet = pickle.loads(data)
                    conn.send("got it!".encode())
                    if self.total_packets == 0:
                        self.total_packets = packet.number_of_packets
                    sender_ip = packet.sender_ip_address
                    sender_mac = packet.sender_mac_address
                    if not self.file_name:
                        self.file_name = packet.payload["file_name"]
                        print(self.file_name)
                    if self.file_size == 0:
                        self.file_size = packet.payload["file_size"]
                    if not self.output_file_location:
                        self.output_file_location = os.path.join(self.destination_directory, self.file_name)
                    message[packet.packet_seq_number] = packet.payload["content"]
            except socket.error:
                print("Error Occurred")
                break

        for i in range(1, self.total_packets + 1):
            if message[i]:
                self.message.append(message[i])
        output_file = open(self.output_file_location, "wb")
        output_file.writelines(self.message)
        output_file.close()

        output_file_size = os.path.getsize(self.output_file_location)
        print("Expected file size (Bytes)", self.file_size, sep=" : ")
        print("Received file size (Bytes)", output_file_size, sep=" : ")

        print("Loss %", (self.file_size - output_file_size) * 100 / self.file_size, sep=" : ")
        conn.close()