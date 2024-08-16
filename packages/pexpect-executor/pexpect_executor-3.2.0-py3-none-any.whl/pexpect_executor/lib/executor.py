#!/usr/bin/env python3

# Standard libraries
from errno import ENOENT
from getpass import getuser
from os import chdir, environ
from time import sleep
from typing import List, Optional

# Components
from ..engines.engine import Engine
from ..package.bundle import Bundle
from ..prints.colors import Colors
from ..system.platform import Platform

# Executor
class Executor:

    # Constants
    KEY_UP: str = '\033[A'
    KEY_DOWN: str = '\033[B'
    KEY_LEFT: str = '\033[D'
    KEY_RIGHT: str = '\033[C'
    KEY_ENTER: str = '\r'
    KEY_SPACE: str = ' '

    # Delays
    DELAY_INIT: float = 1.0
    DELAY_PRESS: float = 0.5
    DELAY_PROMPT: float = 1.0

    # Labels
    LABEL_HOST: str = 'preview'
    LABEL_TOOL: str = 'executor'

    # Members
    __delay_init: float
    __delay_press: float
    __delay_prompt: float
    __engine: Optional[Engine]
    __host: str = environ[Bundle.ENV_HOST] if Bundle.ENV_HOST in environ else LABEL_HOST
    __masks: List[str] = []
    __tool: str = environ[Bundle.ENV_TOOL] if Bundle.ENV_TOOL in environ else LABEL_TOOL

    # Constructor, pylint: disable=too-many-arguments
    def __init__(
        self,
        command: str = '',
        delay_init: float = DELAY_INIT,
        delay_press: float = DELAY_PRESS,
        delay_prompt: float = DELAY_PROMPT,
        hold_prompt: bool = False,
        workdir: str = '',
    ) -> None:

        # Prepare delays
        self.__delay_init = float(delay_init)
        self.__delay_press = float(delay_press)
        self.__delay_prompt = float(delay_prompt)

        # Prepare workdir
        if workdir:
            self.__prompt(f'cd {workdir}', hold_prompt=hold_prompt)
            chdir(workdir)

        # Prepare members
        self.__engine = None

        # Prepare command
        self.__prompt(command, hold_prompt=hold_prompt)
        if command:

            # Spawn command
            self.__engine = Engine(command)

            # Delay executor initialization
            if self.__delay_init > 0.0:
                Executor.sleep(self.__delay_init)
                self.read()

    # Configure
    @staticmethod
    def configure(
        host: str = LABEL_HOST,
        tool: str = LABEL_TOOL,
        masks: Optional[List[str]] = None,
        strips: Optional[List[str]] = None,
    ) -> None:

        # Prepare host
        Executor.__host = host

        # Deprecate strips
        if strips: # pragma: no cover
            raise SystemError('Parameter "strips" is deprecated, use "masks" instead')

        # Prepare masks
        if masks:
            Executor.__masks = masks
        else:
            Executor.__masks = []

        # Prepare tool
        Executor.__tool = tool

        # Prepare colors
        Colors.prepare()

    # Control key, pylint: disable=no-self-use
    def __control_key(self, key: str) -> bytes:

        # Acquire key value
        key = key.lower()
        try:
            value = ord(key)
        except TypeError:
            value = 0

        # Handle alphabetical key
        if 97 <= value <= 122:
            value = value - ord('a') + 1
            return bytes([value])

        # List specific keys
        mappings = {
            '@': 0,
            '`': 0,
            '[': 27,
            '{': 27,
            '\\': 28,
            '|': 28,
            ']': 29,
            '}': 29,
            '^': 30,
            '~': 30,
            '_': 31,
            '?': 127
        }

        # Handle specific keys
        if key in mappings:
            return bytes([mappings[key]])

        # Unknown fallback
        return bytes()

    # Prompt
    def __prompt(self, command: str, hold_prompt: bool = False) -> None:

        # Display prompt
        print(
            f'{Colors.GREEN_THIN}{getuser()}{Colors.RESET}'
            f'@{Colors.RED_THIN}{self.__host}{Colors.RESET}'
            f':{Colors.YELLOW_THIN}~/{self.__tool}{Colors.RESET}$ ', end='')
        Platform.flush()

        # Delay prompt
        Executor.sleep(self.__delay_prompt)

        # Display command
        if command:
            print(f'{command} ', end='')
            Platform.flush()
            Executor.sleep(self.__delay_prompt)
            print(' ')
            Platform.flush()

        # Return prompt
        elif not hold_prompt:
            print(' ')
            Platform.flush()

    # Press
    def press(self, key: str, control: bool = False) -> 'Executor':

        # Execution check
        if not self.__engine:
            return self

        # Delay press
        Executor.sleep(self.__delay_press)

        # Press Ctrl+key
        if control:
            self.__engine.send(self.__control_key(key))

        # Press key
        else:
            self.__engine.send(key)

        # Result
        return self

    # Read
    def read(self) -> 'Executor':

        # Execution check
        if not self.__engine:
            return self

        # Read stream
        self.__engine.read(Executor.__masks)

        # Result
        return self

    # Wait
    def wait(self, delay: float) -> 'Executor':

        # Delay execution
        Executor.sleep(delay)

        # Result
        return self

    # Finish
    def finish(self, force: bool = False) -> int:

        # Execution check
        if not self.__engine:
            return ENOENT

        # Read and wait execution
        if not force:
            try:
                while self.__engine.isalive():
                    self.read()
            except KeyboardInterrupt:
                pass

        # Terminate process
        self.__engine.terminate(force=force)

        # Result
        return self.__engine.status()

    # Sleep
    @staticmethod
    def sleep(delay: float) -> None:

        # Delay execution
        sleep(delay)
