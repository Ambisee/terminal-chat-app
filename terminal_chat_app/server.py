'''
server.py :
Contains the interface and implementation for the Server class
'''
# --- Libraries --- #
import socket
import threading
from traceback import format_exc
import traceback
from typing import Dict, List, Set, Union

from dotenv import load_dotenv

from .base_socket import BaseSocket

# --- Server Class --- #
class Server(BaseSocket):
    '''
    Server class -
    Provides a wrapper for the server socket
    '''
    def __init__(self, host: str=BaseSocket.HOST, port: int=BaseSocket.PORT) -> None:
        '''
        Initialization
        '''
        self.server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_address = (host, port)
        self.addresses: Dict[socket.socket, str] = {}
        self.existing_usernames: Set[str] = set()
        self.server_up = True

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_server(self) -> None:
        '''
        Starting the server to listen to incoming connections on the host machine
        '''
        self.server_socket.settimeout(0.25)
        self.server_socket.bind(self.host_address)
        self.server_socket.listen()

        print('[START] Server listening at %s:%d' % self.host_address)
        self.accept_client_connection()


    def accept_client_connection(self) -> None:
        '''
        Handles incoming client connections.
        Run in an infinite loop on the Main thread.
        '''
        try:
            while self.server_up:
                try:
                    conn, addr = self.server_socket.accept()
                    print('[NEW CONNECTION] %s:%d has connected' % addr)
                    self.addresses[conn] = addr
                except ConnectionResetError:
                    print('[WARNING] Server closed. Incoming connection handler stopped')
                    return
                except socket.timeout:
                    continue

                threading.Thread(target=self.handle_client, args=(conn,)).start()

        except KeyboardInterrupt:
            self.server_up = False
            print('[WARNING] Server closed. KeyboardInterrupt exception detected')
            self.server_socket.close()
            return


    def handle_client(self, conn: socket.socket) -> None:
        '''
        Handles incoming client packets
        '''
        name = self.handle_username_assignment(conn)
        
        if name == self.CLIENT_DISCONNECT_MESSAGE:
            print('[INFO] %s:%d disconnecting...' % self.addresses[conn])
            del self.addresses[conn]
            conn.close()
            return
        
        self.existing_usernames.add(name)
        self.broadcast('<Server>: %s connected' % name)

        while self.server_up:
            try:
                msg = self.receive_message(conn)
            except ConnectionResetError or ConnectionAbortedError as e:
                print('[ERROR] %s encoutered by %s:%d - e' % (type(e).__name__, *self.addresses[conn], e))
                msg = self.CLIENT_DISCONNECT_MESSAGE
            except BlockingIOError as e:
                continue
            except Exception as e:
                print('[ERROR] Unknown error occured: %s' % e)
                msg = self.CLIENT_DISCONNECT_MESSAGE
            
            if msg == self.CLIENT_DISCONNECT_MESSAGE:
                print('[INFO] %s:%d disconnecting...' % self.addresses[conn])

                self.existing_usernames.remove(name)
                del self.addresses[conn]
                
                if len(self.addresses) > 0: self.broadcast(f'<Server>: {name} disconnected from the server')
                conn.close()

                break
            
            print('[MESSAGE] <%s>: %s' % (name, msg))
            self.broadcast('<%s>: %s' % (name, msg))

        return


    def handle_username_assignment(self, conn: socket.socket) -> str:
        '''
        Handle the assignment of a new user's username assignment
        '''
        name = self.receive_message(conn)
        
        # If the check returns None, proceed to return the name to the client handler
        while (check := self.check_username_validity(name)):
            self.send_message(conn, check)
            name = self.receive_message(conn)
        
        self.send_message(conn, name)
        return name


    def check_username_validity(self, username: str) -> Union[str, None]:
        '''
        Check if the username has been used or not
        '''
        # Check if the username has been used, return None if it has not
        if username in self.existing_usernames:
            return self.USERNAME_EXISTS_MESSAGE

        return None
        

    def broadcast(self, message:str) -> None:
        '''
        Send a message to all connected clients
        '''
        for client in self.addresses.keys():
            self.send_message(client, message)
        
        return
