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

            v = ""
            lines = line.split()
            op = lines[0]
            if op == "READ":
                k = line[5 : ]
            elif op == "GET":
                k = line[4 : ]
            elif op == "PUT":
                k = lines[1]
                vbegin = len(k) + 4
                v = line[vbegin : ]
            
            size_num = 7
            size_num += len(k)
            if op == "PUT":
                size_num += 1 + len(v)
            size = f"{size_num:03d}"
            
            # 如果请求长度大于999

            rq_info = size + " " + k
            if op == "PUT":
                rq_info += " " + v
            
            self.request_data.append(rq_info)
        
        f.close()
        

def start_client(self, _filename, _port):
        my_client = TupleSpaceClient(_filename, _port)

        my_client.read_data()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.connect(self.socket_addr)   

        for every_rq in my_client.request_data:
            client_socket.send(every_rq.encode())

            res = client_socket.recv(4096)

            print(every_rq + " " + res.decode('utf-8'))
            