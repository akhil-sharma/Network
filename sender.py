import math
import socket
import uuid
from packet import Packet


def get_sender_ip():
    return socket.gethostbyname(socket.getfqdn())


def get_sender_mac():
    mac_num = hex(uuid.getnode()).replace("0x", "").zfill(12)
    return ':'.join(mac_num[i: i + 2] for i in range(0, 11, 2))


class Sender:
    def __init__(self):
        self.ip_address = get_sender_ip()
        self.mac_address = get_sender_mac()
        self.user_data = ""
        self.characters_per_packet = 10
        self.packet_list = []
        self.number_of_packets = 0

    def generate_packets(self):
        self.number_of_packets = math.ceil(len(self.user_data) / self.characters_per_packet)
        for i in range(0, self.number_of_packets):
            self.packet_list.append(
                Packet(self.ip_address, self.mac_address, i + 1, self.number_of_packets,
                       self.user_data[i * self.characters_per_packet:self.characters_per_packet * (i + 1)]))

    def get_user_data(self):
        self.user_data = input("Enter the data to be sent: ")
        while not self.user_data.strip():
            self.user_data = input("EmptyStringError: Please enter a valid string: ")
        self.generate_packets()
        #return tuple(self.packet_list)

    def display_packets(self):
        for i in range(0, self.number_of_packets):
            self.packet_list[i].display_packet_info()

    def destroy_packets(self):
        for _ in range(0, self.number_of_packets):
            del self.packet_list[0]
