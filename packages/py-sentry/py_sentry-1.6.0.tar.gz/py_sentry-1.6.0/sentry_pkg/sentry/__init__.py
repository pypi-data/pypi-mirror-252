"""
This module provides  provides a foundation for a service that will run
a task at a set interval.
"""

from .constants import (
    Config,
    SigHandler,
    LOG_LEVELS,
    COMMAND_KEY,
    CONFIG_FILE_KEY,
    CONFIG_SECTION_KEY,
    LOG_FILE_KEY,
    LOG_LEVEL_KEY,
    PID_FILE_KEY,
)
from .service import (
    IntervalService,
    read_config,
    required_options,
    required_positionals,
)

from .task import Task
