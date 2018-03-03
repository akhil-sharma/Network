import math
import os
from definitions import ROOT_DIR
from packet import Packet
import utility as util
import socket
from struct import *


class Sender:
    def __init__(self):
        self.ip_address = util.get_sender_ip()
        self.mac_address = util.get_sender_mac()
        self.receiver_ip_address = util.get_sender_ip()
        self.receiver_port = 9999
        self.user_data = ""
        self.filename = ""
        self.file_size = 0
        self.characters_per_packet = 10
        self.packet_list = []
        self.number_of_packets = 0
        self.certificate = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_security_certificate(self):
        username = input("username: ")
        password = input("password: ")
        request = (username + " " + password + " " + self.ip_address + " " + self.mac_address).encode()
        self.sock.connect(("127.0.0.1", 9898))  # security server
        # Prefix each message with a 4-byte length (network byte order)
        msg = pack('>I', len(request)) + request
        self.sock.send(msg)
        self.certificate = self.sock.recv(1024)
        print("\n" + self.certificate)

    def generate_packets(self):
        self.number_of_packets = int(math.ceil(len(self.user_data) / int(self.characters_per_packet)))
        for i in range(0, self.number_of_packets):
            pack = self.user_data[i * self.characters_per_packet:
                                  self.characters_per_packet * (i + 1)]
            self.packet_list.append(
                Packet(self.ip_address, self.mac_address, i + 1, self.number_of_packets,
                       {"file_name": self.filename, "file_size": self.file_size, "content": pack}
                       , self.receiver_ip_address, self.certificate))

    def get_user_data(self):
        chars_per_pack = input("Enter the size of a packet(10 characters): ").strip()
        if chars_per_pack and int(chars_per_pack):
            self.characters_per_packet = int(chars_per_pack)

        location = input("Enter the location of the file (Project_root): ")
        if not location.strip():
            location = ROOT_DIR

        file_name = input("Enter the file name(sender.py): ")
        while not file_name.strip():
            file_name = "sender.py"

        receiver_port = input("Enter port number(9999): ").strip()
        while receiver_port and int(receiver_port):
            self.receiver_port = int(receiver_port)

        file_home = os.path.join(location, file_name)
        self.filename = file_name
        self.user_data = open(file_home, "rb").read()
        self.file_size = os.path.getsize(file_home)
        print("File Size: ", self.file_size, " bytes")
        self.generate_packets()

    def display_packets(self):
        for i in range(0, self.number_of_packets):
            self.packet_list[i].display_packet_info()

    def send_object(self, packet_list):
        self.sock.connect(("127.0.0.1", self.receiver_port))
        for packet in packet_list:
            self.send_msg(packet.serialize().encode())

    def send_msg(self, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = pack('>I', len(msg)) + msg
        self.sock.sendall(msg)


if __name__ == "__main__":
    s = Sender()
    s.get_user_data()
    # Now, we have a packet list
    s.send_object(s.packet_list)

