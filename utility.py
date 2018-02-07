import socket
import uuid


def get_sender_ip():
    return socket.gethostbyname(socket.getfqdn())


def get_sender_mac():
    mac_num = hex(uuid.getnode()).replace("0x", "").zfill(12)
    return ':'.join(mac_num[i: i + 2] for i in range(0, 11, 2))