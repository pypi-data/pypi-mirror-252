import threading
import time
from typing import Optional

from colorama import Fore, Style

from . import Terminal


class Waiting:
    """A class to show a waiting message while some process is running."""

    def __init__(self, doing: str, timer: bool = True) -> None:
        """
        :param doing: The message to show.
        :param timer: Whether to show the elapsed time. Default: True.
        """
        self.doing = doing.strip().rstrip('...')
        self.timer = 0 if timer else None
        self.stated_time = time.perf_counter()
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def __enter__(self) -> 'Waiting':
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._stop()
        if exc_type is not None:
            s = f'\r{self.doing}... {Fore.RED}ERROR{Style.RESET_ALL}'
            if self.timer is not None:
                s += f' {Fore.WHITE}({self.timer:.1f}s){Style.RESET_ALL}'
            Terminal._updating_line = s
            print(s)
        else:
            s = f'\r{self.doing}... {Fore.GREEN}DONE{Style.RESET_ALL}'
            if self.timer is not None:
                s += f' {Fore.WHITE}({self.timer:.1f}s){Style.RESET_ALL}'
            Terminal._updating_line = s
            print(s)

    def _loop(self):
        while self._running:
            if self.timer is not None:
                self.timer = time.perf_counter() - self.stated_time
            s = f'\r{self.doing}...{Style.RESET_ALL}'
            if self.timer is not None:
                s += f'{Fore.WHITE}({self.timer:.1f}s){Style.RESET_ALL}'
            Terminal._updating_line = s
            print(s, end='')
            time.sleep(0.05)

    def _stop(self) -> None:
        Terminal._updating_line = ''
        self._running = False
        self._thread.join()

    def start(self) -> None:
        self._running = True
        self._thread.start()

    def done(self) -> None:
        self._stop()
        s = f'\r{self.doing}... {Fore.GREEN}DONE{Style.RESET_ALL}'
        if self.timer is not None:
            s += f' {Fore.WHITE}({self.timer:.1f}s){Style.RESET_ALL}'
        print(s)

    def error(self) -> None:
        self._stop()
        s = f'\r{self.doing}... {Fore.RED}ERROR{Style.RESET_ALL}'
        if self.timer is not None:
            s += f' {Fore.WHITE}({self.timer:.1f}s){Style.RESET_ALL}'
        print(s)
