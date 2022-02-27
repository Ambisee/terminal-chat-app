'''
test_client.py :
Runs a test client without the use of the curses module
'''
# --- Libraries --- #
import sys
import time
import socket
import threading

from terminal_chat_app.base_socket import BaseSocket
from terminal_chat_app.client import Client

# --- Functions --- #
def create_client():
    client = Client('192.168.56.1', 8080)
    return client


# --- Main function --- #
if __name__ == '__main__':
    client = create_client()
    client.send_client_message('John')

    time.sleep(1)
    client.send_client_message('Hello World')

    time.sleep(1)
    client.send_client_message('hello')

    input()

    client.send_client_message('!quit')
