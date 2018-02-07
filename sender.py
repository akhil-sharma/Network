import math
import os
from definitions import ROOT_DIR
from packet import Packet
import utility as util


class Sender:
    def __init__(self):
        self.ip_address = util.get_sender_ip()
        self.mac_address = util.get_sender_mac()
        self.user_data = ""
        self.filename = ""
        self.file_size = 0
        self.characters_per_packet = 10
        self.packet_list = []
        self.number_of_packets = 0

    def generate_packets(self):
        self.number_of_packets = int(math.ceil(len(self.user_data) / int(self.characters_per_packet)))
        for i in range(0, self.number_of_packets):
            pack = self.user_data[i * self.characters_per_packet:
                                  int(self.characters_per_packet) * (i + 1)]
            self.packet_list.append(
                Packet(self.ip_address, self.mac_address, i + 1, self.number_of_packets,
                       {"file_name": self.filename, "file_size": self.file_size, "content": pack}))

    def get_user_data(self):
        chars_per_pack = input("Enter the size of a packet(10): ").strip()
        if chars_per_pack and int(chars_per_pack):
            self.characters_per_packet = int(chars_per_pack)

        location = input("Enter the location of the file (Project_root): ")
        while not location.strip():
            location = ROOT_DIR

        file_name = input("Enter the file name(sender.py): ")
        while not file_name.strip():
            file_name = "sender.py"

        file_home = os.path.join(location, file_name)
        print(file_home)
        self.filename = file_name
        self.user_data = open(file_home, "rb").read()
        self.file_size = os.path.getsize(file_home)
        print("File Size: ", self.file_size, " bytes")
        self.generate_packets()

    def display_packets(self):
        for i in range(0, self.number_of_packets):
            self.packet_list[i].display_packet_info()


if __name__ == "__main__":
    s = Sender()
    s.get_user_data()
    s.display_packets()
