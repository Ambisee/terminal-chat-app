'''
client.py :
Contains the interface and implementation for the Client class
'''
# --- Libraries --- #
import socket
import threading
from typing import Callable

from .base_socket import BaseSocket

# --- Client Class --- #
class Client(BaseSocket):
    '''
    Client class -
    Provides a wrapper for a client socket
    '''

    def __init__(self, host: str=BaseSocket.HOST, port: int=BaseSocket.PORT) -> None:
        '''
        Initialization
        '''
        self.client_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))


    def handle_incoming_message(self, callback: Callable[[str], None]) -> None:
        '''
        Listen for incoming packets from the server and call the callback function with the message
        '''
        while True:
            try:
                message = self.receive_message(self.client_socket)
                if message == self.CLIENT_DISCONNECT_MESSAGE:
                    self.client_socket.close()

                callback(message)
            except Exception:
                return


    def start_listening(self, callback: Callable[[str], None]) -> None:
        '''
        Start the process of listening for incoming messages and 
        process them with the callback function
        '''
        threading.Thread(target=self.handle_incoming_message, args=(callback,)).start()


    def send_username(self, username: str) -> str:
        '''
        Method for sending a username to be set for the client
        '''
        try:
            self.send_message(self.client_socket, username)
            response = self.receive_message(self.client_socket)

            return response
        except Exception:
            return self.ERROR_MESSAGE


    def send_client_message(self, message: str) -> str:
        '''
        Send messages to the server
        '''
        try:
            self.send_message(self.client_socket, message)
            
            if any(message in x for x in  [BaseSocket.CLIENT_DISCONNECT_MESSAGE]):
                self.close_socket()
                return message

            return message
        except:
            self.close_socket()
            return self.CLIENT_DISCONNECT_MESSAGE


    def close_socket(self) -> None:
        '''
        Close the client socket
        '''
        self.client_socket.close()
        return
