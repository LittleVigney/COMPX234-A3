import socket

class TupleSpaceClient:
    def __init__(self, _filename, _port):
        self.request_data = list()
        self.port = _port
        self.filename = _filename
        self.socket_addr = ("localhost", self.port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def read_data(self):
        with open(self.filename, 'r') as f:
            line = f.readline()

            self.request_data.append(line)
        

    def start_client(self):
        self.read_data()

        self.client_socket.connect(self.socket_addr)
