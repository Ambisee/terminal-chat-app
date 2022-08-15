'''
utils.py :
Defines some utility functions
'''
# --- Libraries --- #
import curses
from typing import Dict, List

# --- Functions --- #
def init_header_color_map(username: str) -> Dict[str, int]:
    '''
    Intializes the mappings between chat headers
    and their corresponding font colors     
    '''
    return {
        '<Interface>': curses.color_pair(2),
        '<Server>': curses.color_pair(1),
        f'<{username}>': curses.color_pair(3)
    }

def render_text(
    stdscr: curses.window,
    textpad_chats: List[str],
    start: int,
    end: int,
    padding: int,
    current_text: List[str],
    header_color_map: Dict[str, int]
) -> None:
    '''
    Render the `textpad_chats` onto the curses window and
    display the input bar
    '''
    stdscr.clear()
    
    for i in range(start, end):
        line = textpad_chats[i]
        header = line[:line.index('>') + 1]

        color = header_color_map.get(header, None)
        
        if color is None:
            stdscr.addstr(line)
        else:
            stdscr.addstr(line, color)
    
    stdscr.addstr(padding + 2, 0, '<You>: ')
    stdscr.addstr(padding + 2, len('<You>: '), ''.join(current_text))
    
    stdscr.refresh()

def receive_broadcast(message: str, message_list: List[str]) -> None:
        '''
        Append messages received from the server to the message list
        '''
        message_list.append(message + '\n')