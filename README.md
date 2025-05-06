### This is my assignment 3 for COMPX234.

#### server.py

##### TupleSpaceServer: server class

- **init**: constructor

  - ts_data: dictionary store all tuples of the server.

  - server_port: port number for server.

  - ts_state: state number for server

- **update_states**: update state of server according to the operation executed.
- **read**: read action.
- **get**: get action.
- **put**: put action.
- **cal_info**: calculate and update the state.
- **display_info**: print the server state.

##### handle_client: method for server to handle one client

##### start_server: start server and waiting for clients connection.



#### client.py

##### TupleSpaceClient: client class

- **init**: constructor
  - **request_data**: data clients will send to server
  - **origin_data**: original data clients loads from files.
  - **port**: server port
  - **filename**: file name which the client will load
  - **socket_addr**: address of server socket.

- **read_data**: load data from file and change original data to the protocol format.

##### start_client: start one client and send its requests to server.
