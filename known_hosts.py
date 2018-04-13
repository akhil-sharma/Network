

def retrieve_host(holder):
    return KnownHosts(holder['username'], holder['password'], holder['ip_address'], holder['mac_address'])


class KnownHosts:
    def __init__(self, username, password, ip_address, mac_address):
        self.username = username
        self.password = password
        self.mac_address = mac_address
        self.ip_address = ip_address

    def serialize(self):
        return str({'username': self.username, 'password': self.password,
                    'ip_address': self.ip_address, 'mac_address': self.mac_address})

