import math
import os
from definitions import ROOT_DIR, SECURITY_SERVER
from packet import Packet
import utility as util
import socket
from struct import *
from known_hosts import KnownHosts


def get_receiver_address():
    receiver_address = input("Enter receiver's address (192.168.178.3, 9987): ")
    if not receiver_address:
        return "192.168.56.3", 9987
    else:
        address = receiver_address.split(",")
        return address[0], int(address[1])


class Sender:
    def __init__(self):
        self.ip_address = "192.168.56.1"  # util.get_self_ip()
        self.mac_address = util.get_self_mac()
        self.user_data = ""
        self.filename = ""
        self.file_size = 0
        self.characters_per_packet = 10
        self.packet_list = []
        self.number_of_packets = 0
        self.certificate = ""

    def get_security_certificate(self):
        username = input("username: ")
        password = input("password: ")
        request = KnownHosts(username, password, self.ip_address, self.mac_address).serialize().encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SECURITY_SERVER[0], SECURITY_SERVER[1]))  # security server
        # Prefix each message with a 4-byte length (network byte order)
        msg = pack('>I', len(request)) + request
        sock.send(msg)
        self.certificate = util.recv_msg(sock).decode()
        print("\n" + self.certificate)
        sock.close()

    def generate_packets(self, receiver_ip):
        self.number_of_packets = int(math.ceil(len(self.user_data) / int(self.characters_per_packet)))
        for i in range(0, self.number_of_packets):
            pack = self.user_data[i * self.characters_per_packet:
                                  self.characters_per_packet * (i + 1)]
            self.packet_list.append(
                Packet(self.ip_address, self.mac_address, i + 1, self.number_of_packets,
                       {"file_name": self.filename, "file_size": self.file_size, "content": pack}
                       , receiver_ip, self.certificate))

    def get_user_data(self, receiver_ip):
        chars_per_pack = input("Enter the size of a packet(10 characters): ").strip()
        if chars_per_pack and int(chars_per_pack):
            self.characters_per_packet = int(chars_per_pack)

        location = input("Enter the location of the file (Project_root): ")
        if not location.strip():
            location = ROOT_DIR

        file_name = input("Enter the file name(sender.py): ")
        while not file_name.strip():
            file_name = "sender.py"

        file_home = os.path.join(location, file_name)
        self.filename = file_name
        self.user_data = open(file_home, "rb").read()
        self.file_size = os.path.getsize(file_home)
        print("File Size: ", self.file_size, " bytes")
        self.generate_packets(receiver_ip)

    def display_packets(self):
        for i in range(0, self.number_of_packets):
            self.packet_list[i].display_packet_info()


if __name__ == "__main__":
    s = Sender()
    s.get_security_certificate()
    receiver_ip_address, receiver_port = get_receiver_address()
    s.get_user_data(receiver_ip_address)
    # # Now, we have a packet list
    #  util.send_object(s.packet_list, receiver_ip_address, receiver_port)
    util.send_object(s.packet_list, "192.168.56.2", 9999)
