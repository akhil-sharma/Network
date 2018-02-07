from definitions import ROOT_DIR
import os
import utility as util


class Receiver:

    def __init__(self):
        self.message = []
        self.ip_address = util.get_sender_ip()
        self.mac_address = util.get_sender_mac()
        self.file_name = ""
        self.file_size = 0
        self.total_packets = 0
        self.destination_directory = os.path.join(ROOT_DIR, "received_files")

    def receive_packets(self, packets):
        message = {}
        if len(packets):
            self.total_packets = packets[0].number_of_packets
            sender_ip = packets[0].sender_ip_address
            sender_mac = packets[0].sender_mac_address
            self.file_name = packets[0].payload["file_name"]
            self.file_size = packets[0].payload["file_size"]
            print("Destination directory: ", self.destination_directory)
            output_file_location = os.path.join(self.destination_directory, self.file_name)
            for i in range(self.total_packets):
                message[packets[i].packet_seq_number] = packets[i].payload["content"]

            for i in range(1, self.total_packets+1):
                if message[i]:
                    self.message.append(message[i])

            output_file = open(output_file_location, "wb")
            output_file.writelines(self.message)
            output_file.close()

            output_file_size = os.path.getsize(output_file_location)
            print("Expected file size (Bytes)", self.file_size, sep=" : ")
            print("Received file size (Bytes)", output_file_size, sep=" : ")

            print("Loss %", (self.file_size - output_file_size)*100/self.file_size, sep=" : ")