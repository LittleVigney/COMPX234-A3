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
        read_res = ""

        with self.ts_lock:
            if read_goal in self.ts_data:
                read_res = f"OK ({read_goal}, {self.ts_data[read_goal]} read)"
                self.update_states("Rt")
            else:
                read_res = f"ERR {read_goal} does not exist"
                self.update_states("Rf")
            
        return read_res
    
    def get(self, get_goal):
        get_res = ""

        with self.ts_lock:
            if get_goal in self.ts_data:
                get_res = f"OK ({get_goal}, {self.ts_data[get_goal]}) removed"
                self.update_states("Gt")
            else:
                get_res = f"ERR {get_goal} does not exist"
                self.update_states("Gf")
                
        return get_res
    
    def put(self, put_goal): # put_goal(tuple)
        put_res = ""
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