from definitions import ROOT_DIR
import os
import utility as util
import socket
import threading
from packet import retrieve_packet_members


class ThreadedHost:
    def __init__(self, port=None, host=None):
        if host is None:
            self.host = util.get_self_ip()
        else:
            self.host = host
        if port is None:
            self.port = 9999
        else:
            self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.mac_address = util.get_self_mac()
        self.destination_directory = os.path.join(ROOT_DIR, "received_files")

    def listen(self):
        self.sock.listen(5)
        print("Listening to packets...")
        while True:
            client, address = self.sock.accept()
            client.settimeout(10)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        # single thread per client
        message_buffer = {}
        message = []
        total_packets = 0
        file_name = ""
        file_size = 0
        output_file_location = ""
        print("Listening to client: ", address)
        while True:
                data = util.recv_msg(client)
                if not data:
                    break
                else:
                    packet = retrieve_packet_members(eval(data))
                    if total_packets == 0:
                        total_packets = packet.number_of_packets
                        print("Total packets: ", total_packets)
                    sender_ip = packet.sender_ip_address
                    sender_mac = packet.sender_mac_address
                    if not file_name:
                        file_name = packet.payload["file_name"]
                        print("filename: ", file_name)
                    if file_size == 0:
                        file_size = packet.payload["file_size"]
                    if not output_file_location:
                        output_file_location = os.path.join(self.destination_directory, file_name)
                    message_buffer[packet.packet_seq_number] = packet.payload["content"]

        for i in range(1, total_packets + 1):
            if message_buffer[i]:
                message.append(message_buffer[i])
        output_file = open(output_file_location, "wb")
        output_file.writelines(message)
        output_file.close()

        output_file_size = os.path.getsize(output_file_location)
        print("Expected file size (Bytes)", file_size, sep=" : ")
        print("Received file size (Bytes)", output_file_size, sep=" : ")

        print("Loss %", (file_size - output_file_size) * 100 / file_size, sep=" : ")

        client.shutdown(socket.SHUT_RDWR)
        client.close()


if __name__ == "__main__":
    while True:
        port_num = input("Port number: ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    #9999
    ThreadedHost(port_num, "127.0.0.1").listen()