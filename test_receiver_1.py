from definitions import ROOT_DIR, SECURITY_SERVER
import os
import utility as util
import socket
import threading
from packet import retrieve_packet_members
from known_hosts import *
from struct import *


class ThreadedNode:
    def __init__(self, port=None, host=None):
        if host is None:
            self.host = util.get_self_ip()
        else:
            self.host = host

        if port is None:
            self.port = 9987
        else:
            self.port = port
        self.certificate = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.mac_address = util.get_self_mac()
        self.destination_directory = os.path.join(ROOT_DIR, "received_files")

    def get_security_certificate(self):
        username = input("username: ")
        password = input("password: ")
        request = KnownHosts(username, password, self.host, self.mac_address).serialize().encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SECURITY_SERVER[0], SECURITY_SERVER[1]))  # security server
        # Prefix each message with a 4-byte length (network byte order)
        msg = pack('>I', len(request)) + request
        sock.send(msg)
        self.certificate = util.recv_msg(sock).decode()
        print("\n" + self.certificate)
        sock.close()

    def listen(self):
        self.sock.listen(10)
        print("Listening for incoming packets...")
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
        packet_for_self = False
        print("Listening to client: ", address)
        security_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        security_sock.connect((SECURITY_SERVER[0], SECURITY_SERVER[1]))  # security server
        comm_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # forwarding the data
        while True:
            data = util.recv_msg(client)
            if not data:
                break
            else:
                packet = retrieve_packet_members(eval(data))
                sender_certificate = packet.certificate
                sender_ip = packet.sender_ip_address
                sender_mac = packet.sender_mac_address

                if authenticate_packet(security_sock, sender_ip, sender_certificate):
                    # packet is good
                    if total_packets == 0:
                        total_packets = packet.number_of_packets
                        print("Total packets: ", total_packets)
                    receiver_ip = packet.receiver_ip_address
                    if receiver_ip == self.host:
                        # packet for me!
                        packet_for_self = True
                        if not file_name:
                            file_name = packet.payload["file_name"]
                            print("filename: ", file_name)
                        if file_size == 0:
                            file_size = packet.payload["file_size"]
                        if not output_file_location:
                            output_file_location = os.path.join(self.destination_directory, file_name)
                        message_buffer[packet.packet_seq_number] = packet.payload["content"]

                    elif receiver_ip != self.host:
                        packet.sender_ip_address = self.host
                        packet.certificate = self.certificate
                        packet.display_packet_info()
                        try:
                            comm_sock.connect((packet.receiver_ip_address, 9987))
                        except socket.error as e:
                            print("error: e (already connected)")
                        forward_message(comm_sock, packet)

                else:
                    print("Packet Authentication failure details")
                    packet.display_packet_info()

        if packet_for_self:
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


def authenticate_packet(sock, sender_ip_address, certificate):
        print("Sending data!")
        request = str([sender_ip_address, certificate]).encode()
        print(request)
        # Prefix each message with a 4-byte length (network byte order)
        msg = pack('>I', len(request)) + request
        sock.send(msg)
        reply = util.recv_msg(sock).decode()
        return reply


def forward_message(sock, msg):
        util.send_msg(sock, msg.serialize().encode())


if __name__ == "__main__":
    node = ThreadedNode(host="192.168.56.3", port=9987)
    node.get_security_certificate()
    node.listen()
