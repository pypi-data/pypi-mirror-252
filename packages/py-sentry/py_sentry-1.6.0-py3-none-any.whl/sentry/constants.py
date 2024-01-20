"""
This file contains constants used by this package
"""

from typing import Any, Callable, Dict, TypeAlias, Union
from types import FrameType

import logging
from signal import Handlers

Config = Dict[str, Union[bool, int, str, None]]

SigHandler: TypeAlias = Union[
    Callable[[int, FrameType | None], Any], int, Handlers, None
]

LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}

COMMAND_KEY = "command"
CONFIG_FILE_KEY = "ini_file"
CONFIG_SECTION_KEY = "ini_section"
LOG_FILE_KEY = "log_file"
LOG_LEVEL_KEY = "log_level"
PID_FILE_KEY = "pid_file"
