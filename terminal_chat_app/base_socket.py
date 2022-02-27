'''
base.py :
Contains the interface and implementation for the Base class
'''
# --- Libraries --- #
import os
import socket
from typing import Union


# --- Class --- #
class BaseSocket:
    '''
    Base class - 
    Provide common socket operation
    '''
    HEADER: int = int(os.getenv('HEADER', 64))
    FORMAT: str = os.getenv('FORMAT', 'utf-8')
    HOST: str = os.getenv('HOST', socket.gethostbyname(socket.gethostname()))
    PORT: int = int(os.getenv('PORT', 8080))
    
    CLIENT_DISCONNECT_MESSAGE: str = os.getenv('CLIENT_DISCONNECT_MESSAGE', '!quit')
    USERNAME_EXISTS_MESSAGE: str = os.getenv('USERNAME_EXISTS_MESSAGE', 'Username exists')
    PROCEED_MESSAGE: str = os.getenv('PROCEED_MESSAGE', 'Proceed')
    EMPTY_MESSAGE: str = os.getenv('EMPTY_MESSAGE', 'Empty')
    ERROR_MESSAGE: str = os.getenv('ERROR_MESSAGE', 'Error encountered')

    def send_message(self, conn: socket.socket, message: str) -> None:
        '''
        Send encoded messages throught the socket
        '''
        message_length = str(len(message)).encode(self.FORMAT)
        message_length += b' ' * (self.HEADER - len(message_length))

        conn.send(message_length)
        conn.send(message.encode(self.FORMAT))

        return
    

    def receive_message(self, conn: socket.socket) -> str:
        '''
        Decode incoming messages
        '''
        message_length = conn.recv(self.HEADER).decode(self.FORMAT)
        message_length = int(message_length)

        message = conn.recv(message_length).decode(self.FORMAT)
        return message
