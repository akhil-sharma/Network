from definitions import SECURITY_SERVER
import utility as util
import socket
import threading
from known_hosts import *


class ThreadedSecurityServer:
    def __init__(self, port=None, host=None):
        if host is None:
            self.host = SECURITY_SERVER[0]  # util.get_self_ip()
        else:
            self.host = host

        if port is None:
            self.port = SECURITY_SERVER[1]  # 9898
        else:
            self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.mac_address = util.get_self_mac()
        self.known_hosts = {}

    def listen(self):
        self.sock.listen(10)
        print("Listening for incoming security requests...")
        while True:
            client, address = self.sock.accept()
            client.settimeout(10)
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        # single thread per client
        temp = ""
        # print("Listening to client: ", client)
        while True:
                data = util.recv_msg(client)  # recognize the purpose of this data
                if not data:
                    break
                else:
                    information = eval(data)
                    # print(type(information))
                    information_length = len(information)

                    if information_length == 4:
                        identity = eval(retrieve_host(information).serialize())
                        for _, v in identity.items():
                            temp += v
                        temp = hash(temp)
                        self.known_hosts[identity["ip_address"]] = temp  # change to mac
                        util.send_msg(client, str(temp).encode())
                        self.print_known_hosts()
                    else:
                        answer = "False"
                        request = eval(data)
                        if self.known_hosts[request[0]] == int(request[1]):
                            answer = "True"
                        util.send_msg(client, answer.encode())

    def print_known_hosts(self):
        print(self.known_hosts)


if __name__ == "__main__":
    ThreadedSecurityServer().listen()
