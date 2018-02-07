from sender import Sender
from receiver import Receiver


def main():
    # Create a Sender object
    sender = Sender()
    # Create a Receiver object
    receiver = Receiver()

    sender.get_user_data()
    sender.display_packets()

    receiver.receive_packets(tuple(sender.packet_list))


if __name__ == "__main__":
    main()
