import socket
import time
import threading

class TupleSpaceServer:
    def __init__(self):
        self.ts_data = dict()
        self.ts_lock = threading.Lock()
        self.ts_state = {
            "tuples_number": 0,
            "ave_tuple_size": 0,
            "ave_key_size": 0,
            "ave_value_size": 0,
            "clients_number": 0,
            "op_number": 0,
            "R_number": 0,
            "G_number": 0,
            "P_number": 0,
            "error_number": 0
        }