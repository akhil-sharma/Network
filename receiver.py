from definitions import ROOT_DIR
import os
import utility as util
import socket
import threading
from struct import *
from packet import Packet, retrieve_packet_members


def recv_all(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


class ThreadedReceiver:

    def __init__(self, port, host=None):
        self.message = []
        if host is None:
            self.host = util.get_sender_ip()
        else:
            self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.mac_address = list(util.get_sender_mac())
        self.file_name = ""
        self.file_size = 0
        self.total_packets = 0
        self.destination_directory = os.path.join(ROOT_DIR, "received_files")
        self.output_file_location = ""

    def reset(self):
        self.message = []
        self.file_name = ""
        self.file_size = 0
        self.total_packets = 0
        self.output_file_location = ""

    def listen(self):
        self.sock.listen(5)
        print("Listening to packets...")
        while True:
            client, address = self.sock.accept()
            client.settimeout(10)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        # single thread per client
        self.reset()
        message = {}
        print("Listening to client: ", address)
        while True:
                data = self.recv_msg(client)
                if not data:
                    break
                else:
                    packet = retrieve_packet_members(eval(data))
                    if self.total_packets == 0:
                        self.total_packets = packet.number_of_packets
                    sender_ip = packet.sender_ip_address
                    sender_mac = packet.sender_mac_address
                    if not self.file_name:
                        self.file_name = packet.payload["file_name"]
                        print("filename: ", self.file_name)
                    if self.file_size == 0:
                        self.file_size = packet.payload["file_size"]
                    if not self.output_file_location:
                        self.output_file_location = os.path.join(self.destination_directory, self.file_name)
                    message[packet.packet_seq_number] = packet.payload["content"]

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

        client.shutdown(socket.SHUT_RDWR)
        client.close()

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msg_len = recv_all(sock, 4)
        if not raw_msg_len:
            return None
        msg_len = unpack('>I', raw_msg_len)[0]
        # Read the message data
        return recv_all(sock, msg_len)

    def verify_packet(self, packet):
        pass


if __name__ == "__main__":
    while True:
        port_num = input("Port number: ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass
    #9999
    ThreadedReceiver(port_num, "127.0.0.1").listen()

