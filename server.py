import socket
import time
import threading

class TupleSpaceServer:
    def __init__(self):
        self.ts_data = dict()
        self.ts_lock = threading.Lock()
        self.ts_state = {
            "tuples_number": 0, # number of tuples in the tuple space
            "ave_tuple_size": 0, # average tuple size
            "ave_key_size": 0, # average key size
            "ave_value_size": 0, #  average value size
            "clients_number": 0, # total number of clients which have connected
            "op_number": 0, # total number of operations
            "R_number": 0, # total number of READs
            "G_number": 0, # total number of GETs
            "P_number": 0, # total number of PUTs
            "error_number": 0 # total number of errors
        }
    
    def update_states(self, op):
        match op:
            case "Rt":
                self.ts_state["R_number"] += 1
                self.ts_state["op_number"] += 1
            case "Rf":
                self.ts_state["error_number"] += 1
                self.ts_state["R_number"] += 1
                self.ts_state["op_number"] += 1
            case "Gt":
                self.ts_data["G_number"] += 1
                self.ts_data["op_number"] += 1
            case "Gf":
                self.ts_state["error_number"] += 1
                self.ts_data["G_number"] += 1
                self.ts_data["op_number"] += 1
            case "Pt":
                self.ts_state["P_number"] += 1
                self.ts_state["op_number"] += 1
                self.ts_data["tuples_number"] += 1
            case "Pf":
                self.ts_state["error_number"] += 1
                self.ts_state["P_number"] += 1
                self.ts_state["op_number"] += 1

    def read(self, read_goal):

        with self.ts_lock:
            if read_goal in self.ts_data:
                read_res = f"OK ({read_goal}, {self.ts_data[read_goal]} read)"
                self.update_states("Rt")
            else:
                read_res = f"ERR {read_goal} does not exist"
                self.update_states("Rf")
            
        return read_res
    
    def get(self, get_goal):

        with self.ts_lock:
            if get_goal in self.ts_data:
                get_res = f"OK ({get_goal}, {self.ts_data[get_goal]}) removed"
                self.update_states("Gt")
            else:
                get_res = f"ERR {get_goal} does not exist"
                self.update_states("Gf")

        return get_res
    
    def put(self, put_goal): # put_goal(tuple)
        put_goal_key = put_goal[0]
        put_goal_value = put_goal[1]

        with self.ts_lock:
            if put_goal_key in self.ts_data:
                put_res = f"ERR {put_goal_key} already exists"
                self.update_states("Pf")
            else:
                self.ts_data[put_goal_key] = put_goal_value
                put_res = f"OK ({put_goal_key}, {self.ts_data[put_goal_value]}) added"
                self.update_states("Pt")
            
        return put_res
    
    def cal_info(self):
        sum_key_size = 0
        sum_value_size = 0
        sum_tuple_size = 0
        for key, val in self.ts_state:
            sum_key_size += len(key)
            sum_value_size += len(val)
            sum_tuple_size += len(key) + len(val)

        self.ts_data["ave_key_size"] = sum_key_size / self.ts_data["tuples_number"]
        self.ts_data["ave_value_size"] = sum_value_size / self.ts_data["tuples_number"]
        self.ts_data["ave_tuple_size"] = sum_tuple_size / self.ts_data["tuples_number"]
        
    def display_info(self):
        time.sleep(10)

        self.cal_info()

        print(f"Number of tuples in the tuple space: {self.ts_data["tuples_number"]}")
        print(f"Average tuple size: {self.ts_data["ave_tuple_size"]}")
        print(f"Average key size: {self.ts_data["ave_key_size"]}")
        print(f"Average value size: {self.ts_data["ave_value_size"]}")
        print(f"Total number of clients: {self.ts_data["clients_number"]}")
        print(f"Total number of operations: {self.ts_data["op_number"]}")
        print(f"Total READs: {self.ts_data["R_number"]}")
        print(f"Total GETs: {self.ts_data["G_number"]}")
        print(f"Total PUTs: {self.ts_data["P_number"]}")
        print(f"How many errors: {self.ts_data["error_number"]}")

def start_server(client_port):
    my_tuplespace = TupleSpaceServer()

    host = "localhost"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Tuple space server is running and waiting for connection.")

    try:
        while True:
            server_socket.bind(host, client_port)

            server_socket.listen(10)

            client_socket, ip_addr = server_socket.accept()

            print(f"Client connected")

            my_tuplespace.ts_data["clients_number"] += 1

            while True:
                client_request = client_socket.recv(1024).decode('utf-8')

                # format of request from clients
                # NNN R k
                # NNN G k
                # NNN P k v

                rq_size = int(client_request[0 : 3])
                rq_op = client_request[4]
                
                if rq_op == "R" or rq_op == "G":
                    rqs = client_request.split(" ", 1)
                    rq_key = rqs[1]
                    ans = my_tuplespace.read(rq_key)
                elif rq_op == "P":
                    rq = client_request.split(' ', 2)
                    rq_key = rq[1]
                    rq_value = rq[2]
                    ans = my_tuplespace.put((rq_key, rq_value))
                
                client_socket.sendall(ans)

    finally:
        pass