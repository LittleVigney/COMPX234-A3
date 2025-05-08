import socket
import threading

class TupleSpaceClient:
    def __init__(self, _filename, _port):
        self.request_data = list()
        self.origin_data = list()
        self.port = _port
        self.filename = _filename
        self.socket_addr = ("localhost", self.port)

    def read_data(self):
        # open file and load data
        with open(self.filename, 'r') as f:
            while True:
                line = f.readline()

                # if loading finish
                if not line:
                    break
                
                self.origin_data.append(line)
                
                # get k and v from original data
                v = ""
                lines = line.split()

                op = lines[0]
                if op == "READ":
                    k = lines[1]
                elif op == "GET":
                    k = lines[1]
                elif op == "PUT":
                    k = lines[1]
                    vbegin = len(k) + len("PUT") + 2
                    v = line[vbegin : ]

                # calculate size of request
                size_num = 7
                size_num += len(k)
                if op == "PUT":
                    size_num += 1 + len(v)
                size = f"{size_num:03d}"

                # add request in form of protocol to request_data
                rq_info = size + " " + op[0] + " " + k
                if op == "PUT":
                    rq_info += " " + v

                # if k and v is longer than 970
                if len(k) + len(v) + 1 > 999:
                    rq_info = "LONG REQUEST"

                self.request_data.append(rq_info)
        
def start_client(_filename, _port):
        # create a new client and connect with server
        my_client = TupleSpaceClient(_filename, _port)

        my_client.read_data()

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect(my_client.socket_addr)

        # send request to server
        ct = 0
        for every_rq in my_client.request_data:
            # if k and v is longer than 970, output an error message
            if every_rq == "LONG REQUEST":
                print("Request is too long.")
                continue
            
            # send request to server
            client_socket.sendall(every_rq.encode('utf-8'))

            # get response from server
            res = client_socket.recv(4096)

            res = res[4 : ]
            # print result of request
            print(my_client.origin_data[ct] + ": " + res.decode('utf-8'))

            ct += 1

if __name__ == "__main__":
    my_clients = list()

    for i in range(1, 11):
        filename = "client_" + str(i) + ".txt"
        client_thread = threading.Thread(target=start_client, args=(filename, 51234))
        client_thread.start()
        
        my_clients.append(client_thread)

    for client in my_clients:
        client.join()
        
    print("All tasks finished.")
