'''
key_maps.py:
Provides mapping between keyboard keys
and their callback functions
'''
# --- Libraries --- #
import sys
import string
from typing import List, NoReturn, Union, Dict, Callable

from .client import Client

# --- Functions --- #
def define_append_function(char: str, text_list: List[str]) -> None:
    '''
    Create a callback function that adds a character to the given list
    '''
    def append_char():
        '''
        Append a character to the specified list
        '''
        text_list.append(char)
        return
    
    return append_char

def delete_char(index: int, text_list: List[str]) -> None:
    '''
    Remove a character from the specified
    list at a given position
    '''
    if len(text_list) > 0:
        text_list.pop()

def disconnect_client(client: Client) -> NoReturn:
    '''
    Send a disconnection message to the server
    and exit the client application
    '''
    client.send_client_message(client.CLIENT_DISCONNECT_MESSAGE)
    sys.exit(0)

def send_message(text_list: List[str], client: Client) -> Union[None, NoReturn]:
    '''
    Send the message saved in the `text_list`
    to the server. Disconnects the client application
    if the disconnect message is sent
    '''
    message: str = ''.join(text_list)

    response: str = client.send_client_message(message)
    text_list.clear()
    
    if response == client.CLIENT_DISCONNECT_MESSAGE:
        sys.exit(0)
    
    return

def initialize_keymap(text_list: List[str], client: Client) -> Dict[str, Callable]:
    '''
    Initializes the mapping of the keyboard keys
    and their callback functions
    '''
    keymap: Dict[str, Callable] = {}

    # Map each key to a function that
    # adds the character to the chat box
    for char in string.printable:
        keymap[char] = define_append_function(char, text_list)
    
    
    # Add the <Enter> or <Return> - callback mappings
    enter_map: Dict[str, Callable] = dict.fromkeys(
        ['\n', '\x0a'], 
        lambda: send_message(text_list, client)
    )

    keymap.update(enter_map)
    
    # Add the <Backspace> - callback mappings
    backspace_map: Dict[str, Callable] = dict.fromkeys(
        ['\b', '\x08'],
        lambda: delete_char(0, text_list)
    )

    keymap.update(backspace_map)
    
    # Add the <Esc> - logout callback mapping
    keymap['\x1b'] = lambda: disconnect_client(client)

    return keymap