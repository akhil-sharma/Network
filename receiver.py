class Receiver:

    def __init__(self):
        self.message = ""

    def receive_packets(self, packets):
        message = {}
        if len(packets):
            total_packets = packets[0].number_of_packets
            sender_ip = packets[0].sender_ip_address
            sender_mac = packets[0].sender_mac_address
            packet_type = packets[0].packet_type

            for i in range(total_packets):
                message[packets[i].packet_seq_number] = packets[i].payload

            for i in range(1, total_packets+1):
                self.message += message[i]

            print("\n", "<-Receiver->", "Message from ip: ", sender_ip, ", mac: ", sender_mac, ", type: ", packet_type,
                  end=" ")
            print(" --> ", self.message, "\n")



