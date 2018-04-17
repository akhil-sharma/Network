import socket
import uuid
from struct import *


def get_self_ip():
    return socket.gethostbyname(socket.getfqdn())


def get_self_mac():
    mac_num = hex(uuid.getnode()).replace("0x", "").zfill(12)
    return ':'.join(mac_num[i: i + 2] for i in range(0, 11, 2))


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msg_len = recv_all(sock, 4)
    if not raw_msg_len:
        return None
    msg_len = unpack('>I', raw_msg_len)[0]
    # Read the message data
    return recv_all(sock, msg_len)


def recv_all(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = pack('>I', len(msg)) + msg
    sock.send(msg)


def send_object(packet_list, receiver_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((receiver_ip, port))
    for packet in packet_list:
        send_msg(sock, packet.serialize().encode())