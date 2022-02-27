# Terminal Chat App

This is a chatting application that works on your local network. Built in Python with the help of the `curses` library and the built-in `sockets` python library,
this repository consists of both the server and client side modules.


### Server
To run the server:
1. Go to the directory that contains the files from the repository (i.e. path\to\the\terminal-chat-app).
2. Run the terminal from the current directory.
3. Input either:
   -  `python run_server.py` to run the server with the default settings (default HOST and PORT number: from ENVIRONMENT variables or program's default), OR
   -  `python run_server.py HOST:PORT` to run the server on the specified address 
      (i.e. `python run_server.py 192.168.56.1:8000` to run the server on `192.168.56.1` and port number `8000`)

### Client
To run the client:
1. Go to the directory that contains the files from the repository (i.e. path\to\the\terminal-chat-app).
2. Run the terminal from the current directory.
3. Input `python run_client.py`.
4. The program will ask you for an address where the server is listening. Enter an address with the format `HOST:PORT` (i.e. `192.168.56.1:8000`).
5. If there is no server listening on the address, the program will ask the user again for another address.
