from sender import Sender
from receiver import Receiver


def main():
    # Create a Receiver object
    receiver = Receiver()
    receiver.get_port()

    # Create a Sender object
    sender = Sender()
    sender.receiver_port = receiver.receiver_port
    sender.get_user_data()

    sender.display_packets()

    receiver.receive_packets(tuple(sender.packet_list), sender.packet_size)


if __name__ == "__main__":
    main()
