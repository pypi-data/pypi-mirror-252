import os
from typing import Optional, Union

from colorama import Fore, Back, Style

from .cursor import Cursor
from .getchar import getchar


class Terminal:
    """Main terminarty class."""
    _instance = None
    _updating_line = ''

    INPUT_STYLE = f'{Fore.YELLOW}>{Style.RESET_ALL} '

    def __init__(self) -> None:
        if Terminal._instance is not None:
            raise RuntimeError('Only one instance of Terminal is allowed')
        Terminal._instance = self

    @staticmethod
    def clear() -> None:
        """Clears entire terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def bell() -> None:
        """Makes an audible noise."""
        print('\a', end='')

    @staticmethod
    def save_screen() -> None:
        """Save current terminal screen state. Can be restored with ``Terminal.restore_screen()``."""
        print('\033[?47h', end='')

    @staticmethod
    def restore_screen() -> None:
        """Restores current terminal screen state. Can be saved with ``Terminal.save_screen()``."""
        print('\033[?47l', end='')

    @staticmethod
    def input(text: str, clear: bool) -> str:
        """
        Gets input from the user. Just like built in ``input()`` function just with more style.

        :param text: Text to display before input.
        :param clear: If ``True`` clears the screen before and after displaying the text.
        :return: User input.

        :Example:
        >>> x = Terminal.input('Enter your name: ', clear=True)
        Enter your name:
        >>> x
        'John'
        """
        if clear:
            Terminal.clear()
        print(text)
        inp = input(Terminal.INPUT_STYLE)
        if clear:
            Terminal.clear()
        return inp

    @staticmethod
    def getchar() -> bytes:
        """Gets a single character from standard input. Does not echo to the screen."""
        return getchar()

    @staticmethod
    def print(*args, sep: Optional[str] = ' ') -> None:
        """
        Used for printing text, when progress bar or waiting is running.

        :param args: Arguments to print.
        :param sep: Separator between arguments.
        :Example:
        >>> Terminal.print('Hello', 'world')
        Hello world
        >>> Terminal.print('Hello', 'world', sep='-')
        Hello-world
        >>> Terminal.print('Hello', 'world', sep='-', end='!')
        Hello-world!
        """
        if not Terminal._updating_line:
            print(*args, sep=sep)
        else:
            string = '\r' + sep.join(list(map(str, args)))
            end = f'{" " * (len(Terminal._updating_line) - len(string))}\n'
            print(string, end=end)
            print(Terminal._updating_line, end='')

    @staticmethod
    def select(text: str, choices: list[str], *, index: bool = False) -> str:
        """
        Asks user to select one of the choices from the list.
        User can move up and down with arrows and select with Enter.

        :param text: Text to display before choices.
        :param choices: List of choices.
        :param index: If ``True`` returns index of the selected choice instead of the choice itself.
        :return: Selected choice.
        """
        selected = 0
        Terminal.clear()
        Cursor.setpos(1, 1)
        while True:
            print(text)
            for i, choice in enumerate(choices):
                print(f'{Back.LIGHTBLACK_EX if i == selected else Back.BLACK}',
                      f'{choice}',
                      f'{Style.RESET_ALL}',
                      sep='')
            char1 = Terminal.getchar()
            if char1 == b'\r':
                break
            elif char1 == b'\x03':
                raise KeyboardInterrupt
            elif char1 == b'\x1b':
                char2, char3 = Terminal.getchar(), Terminal.getchar()
                if char2 == b'[' and char3 in b'A\x1b':
                    selected -= 1
                    if selected < 0:
                        selected = len(choices) - 1
                elif char2 == b'[' and char3 in b'B\x1b':
                    selected += 1
                    if selected == len(choices):
                        selected = 0
                Cursor.setpos(1, 1)
                continue
            elif char1 != b'\xe0':
                Cursor.setpos(1, 1)
                continue
            char2 = Terminal.getchar()
            if char2 == b'H':
                selected -= 1
                if selected < 0:
                    selected = len(choices) - 1
            elif char2 == b'P':
                selected += 1
                if selected == len(choices):
                    selected = 0
            Cursor.setpos(1, 1)
        Terminal.clear()
        return selected if index else choices[selected]
