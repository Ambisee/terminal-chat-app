'''
client_window.py :
Provides the interface to accomodate the Client class
'''
# --- Libraries --- #
import sys
import curses
from traceback import print_exc
from typing import Callable, Dict, List, Union
from curses import ascii
from curses.textpad import Textbox

from .client import Client
from .key_maps import initialize_keymap


# --- Functions --- #
def setup_colorpairs() -> None:
    '''
    Set up the color schemes for the text
    '''
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    return

def ask_address_window(stdscr: curses.window) -> Union[Client, int]:
    '''
    Initialize the window that asks the user for an address
    to connect to where the server lives
    '''
    def tb_function(x: int) -> int:
        '''
        Textbox callback function for handling window closing through the ESC key
        '''
        if x == ascii.ESC:
            print('Process exited with return value 0')
            sys.exit(0)

        return x

    display_text = 'Enter a host address HOST:PORT : '
    win = curses.newwin(1, 20, 0, len(display_text))
    tb = Textbox(win)

    win.nodelay(True)
    stdscr.clear()
    stdscr.addstr(display_text)
    stdscr.refresh()
    
    client = None

    while not client:
        warning_message = None
        tb.edit(tb_function)
        result = tb.gather().strip()

        try:
            host, address = result.split(':')
            client = Client(host, int(address))
        except ValueError as e:
            warning_message = 'Please enter a valid HOST:PORT address\n'
        except OSError as e:
            warning_message = 'OSError detected: {}\n'.format(e)
        except Exception as e:
            warning_message = 'An unknown error occured: {}\n'.format(e)
            client = None

        finally: 
            win.clear()
            win.refresh()
        
        stdscr.clear()
        if warning_message:
            stdscr.addstr(warning_message, curses.color_pair(3))
            win.mvwin(1, len(display_text))
        stdscr.addstr(display_text)
        stdscr.refresh()

    del tb
    del win

    return client

def ask_username(stdscr: curses.window, client: Client) -> Union[str, int]:
    '''
    Asks for the username that will be used within the chat room
    '''
    def tb_function(x: int) -> int:
        '''
        Textbox callback function for handling window closing through the ESC key
        '''
        if x == ascii.ESC:
            client.send_username(client.CLIENT_DISCONNECT_MESSAGE)
            client.close_socket()
            print('Process exited with return value 0')
            sys.exit(0)

        return x

    display_text = 'Enter a username : '
    win = curses.newwin(1, 20, 0, len(display_text))
    tb = Textbox(win)

    stdscr.clear()
    stdscr.addstr(display_text)
    stdscr.refresh()

    while True:
        tb.edit(tb_function)
        result: str = tb.gather().strip()

        try:
            if len(result) < 1:
                response = client.EMPTY_MESSAGE
            else:
                response = client.send_username(result)
        except:
            client.close_socket()
            return -1
        
        if response == client.USERNAME_EXISTS_MESSAGE:
            warning_message = 'The username entered has already been taken. Please use another username\n'
        elif response == client.EMPTY_MESSAGE:
            warning_message = 'Please enter a non-empty username.\n'
        elif response == client.ERROR_MESSAGE:
            warning_message = 'An unknown error has occured.\n'
        else:
            break
        
        win.clear()
        win.refresh()

        stdscr.clear()
        if warning_message:
            stdscr.addstr(warning_message, curses.color_pair(3))
            win.mvwin(1, len(display_text))
        stdscr.addstr(display_text)
        stdscr.refresh()

    del tb
    del win

    return client.PROCEED_MESSAGE

def chat_room(stdscr: curses.window, client: Client) -> int:
    '''
    Displays the chat room interface for the user
    '''
    PAD_MAXLINE: int = 10

    key: Union[None, str] = None
    current_text: List[str] = []
    textpad_chats: List[str] = ['<Interface>: You joined the room\n']
    current_pad_scroll: int = 0
    keymap: Dict[str, Callable[[], None]] = initialize_keymap(
        current_text,
        client
    )
    
    def receive_broadcast(message: str, message_list: List[str]) -> None:
        '''
        Append messages received from the server to the message list
        '''
        message_list.append(message + '\n')
    
    stdscr.nodelay(True)
    client.start_listening(lambda x: receive_broadcast(x, textpad_chats))

    while key != ascii.ESC:
        
        stdscr.clear()
        for i in range(current_pad_scroll, current_pad_scroll + min(PAD_MAXLINE, len(textpad_chats))):
            stdscr.addstr(textpad_chats[i])
        stdscr.addstr(PAD_MAXLINE + 2, 0, '<You>: ')
        stdscr.addstr(PAD_MAXLINE + 2, len('<You>: '), ''.join(current_text))
        stdscr.refresh()

        try:
            key = stdscr.getkey()
        except Exception: 
            key = None
        
        try:
            if key is None:
                continue
            if key == 'KEY_UP':
                if  current_pad_scroll > 0:
                    current_pad_scroll -= 1
            elif key == 'KEY_DOWN':
                if  current_pad_scroll + PAD_MAXLINE < len(textpad_chats):
                    current_pad_scroll += 1
            else:
                keymap[key]()
        except Exception:
            print_exc(1000)
            client.send_client_message(client.CLIENT_DISCONNECT_MESSAGE)

    return 0

def init_main_screen(stdscr: curses.window) -> int:
    '''
    Runs the main terminal window
    '''
    setup_colorpairs()

    connected_client: Union[Client, int] = ask_address_window(stdscr)
    if isinstance(connected_client, int): return -1

    try:
        username: Union[str, int] = ask_username(stdscr, connected_client)
        if isinstance(username, int): return -1

        exit_status: int = chat_room(stdscr, connected_client)
        return exit_status
    except Exception:
        print_exc()
        connected_client.send_client_message(connected_client.CLIENT_DISCONNECT_MESSAGE)
        return -1

def run_main() -> None:
    '''
    Provides wrapper for the curses window and outputs the exit status of the program
    '''
    exit_status = curses.wrapper(init_main_screen)
    print('Process exited with return value %d' % exit_status)
