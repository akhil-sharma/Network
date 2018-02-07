class Packet:
    MES = "message"
    ACK = "acknowledge"

    def __init__(self, sender_ip_address, sender_mac_address, packet_seq_number, number_of_packets, payload,
                 receiver_ip_address="", receiver_mac_address="", certificate="", packet_type="message"):
        self.sender_ip_address = sender_ip_address
        self.sender_mac_address = sender_mac_address
        self.packet_seq_number = packet_seq_number
        self.number_of_packets = number_of_packets
        self.payload = payload
        self.receiver_ip_address = receiver_ip_address
        self.receiver_mac_address = receiver_mac_address
        self.certificate = certificate
        self.packet_type = packet_type

    def display_packet_info(self):
        print("{0:15s} {1:17s} {2:3d} {3:3d}".format(self.sender_ip_address,
              self.sender_mac_address, self.packet_seq_number, self.number_of_packets), end=" ")
        print(self.payload["file_size"], self.payload["file_name"], self.payload["content"])


# write a modular program which transfers or makes communication across heterogeneuos networks
# use the out of problem number 4