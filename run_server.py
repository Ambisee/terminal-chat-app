'''
run_server.py : 
Driver code that runs the server on a specific port
'''
# --- Modules --- #
import sys

from terminal_chat_app.server import Server

# --- Main Function --- #
if __name__ == '__main__':
    arguments = sys.argv
    port = arguments[1].split(':') if len(arguments) > 1 else None
    
    try:
        if port:
            server = Server(port[0], int(port[1]))
        else:
            server = Server()

        server.start_server()
    except Exception as e:
        print('Usage: python run_server.py HOST:PORT')