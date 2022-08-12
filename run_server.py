'''
run_server.py : 
Driver code that runs the server on a specific port
'''
# --- Modules --- #
import sys
from typing import List

from terminal_chat_app.server import Server

# --- Main Function --- #
if __name__ == '__main__':
    arguments: List = sys.argv
    if len(arguments) > 1:
        port: List[str] = arguments[1].split(':')
    else:
        port: List[str] = []
    
    try:
        if len(port) == 2:
            server = Server(port[0], int(port[1]))
        else:
            server = Server()

        server.start_server()
    except Exception as e:
        print('Usage: python run_server.py HOST:PORT')