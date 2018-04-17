def retrieve_packet_members(holder):
    return Packet(holder['sender_ip_address'], holder['sender_mac_address'], holder['packet_seq_number'],
                  holder['number_of_packets'], holder['payload'], holder['receiver_ip_address'],
                  holder['certificate'], holder['packet_type'])


class Packet:

    def __init__(self, sender_ip_address, sender_mac_address, packet_seq_number, number_of_packets,
                 payload, receiver_ip_address, certificate, packet_type="MESSAGE"):
        self.sender_ip_address = sender_ip_address
        self.sender_mac_address = sender_mac_address
        self.packet_seq_number = packet_seq_number
        self.number_of_packets = number_of_packets
        self.payload = payload
        self.receiver_ip_address = receiver_ip_address
        self.certificate = certificate
        self.packet_type = packet_type
        self.path = []

    def display_packet_info(self):
        print("{0:15s} {1:17s} {2:3d} {3:3d}".format(self.sender_ip_address,
                                                     self.sender_mac_address, self.packet_seq_number,
                                                     self.number_of_packets), end=" ")
        print(self.payload["file_size"], self.payload["file_name"], self.payload["content"])

    def display_packet_path(self):
        for i in range(0, len(self.path)):
            if i == (len(self.path) - 1):
                print(self.path[i])
            else:
                print(self.path[i] + "->", end=" ")

    def serialize(self):
        return str({'sender_ip_address': self.sender_ip_address, 'sender_mac_address': self.sender_mac_address,
                    'packet_seq_number': self.packet_seq_number, 'number_of_packets': self.number_of_packets,
                    'payload': self.payload,
                    'receiver_ip_address': self.receiver_ip_address, 'certificate': self.certificate,
                    'packet_type': self.packet_type})

