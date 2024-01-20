"""
An implementation of a IntervalService Task that shows how a Task can be
configured.
"""

from typing import Any, Dict, List, Optional

import argparse
import logging

from sentry import Config, LOG_LEVEL_KEY

CONFIG_FILE_KEY = "config_file"
CONFIG_SECTION_KEY = "ini_section"
OPTION_ONE_KEY = "one"
OPTION_THE_OTHER_KEY = "other"

_DEFAULTS: Config = {
    CONFIG_FILE_KEY: "demo.ini",
    CONFIG_SECTION_KEY: "demo",
    LOG_LEVEL_KEY: "DEBUG",
    OPTION_ONE_KEY: "default_for_one",
}


class ConfigurableTask:
    """
    This class shows how a Task can be configured.
    """

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """
        self.__params: Optional[Dict[str, Any]] = None

    def create_argument_parser(self) -> argparse.ArgumentParser:
        """
        Creates and populates the argparse.ArgumentParser for this Task.
        """
        parser = argparse.ArgumentParser(
            description=f"Executes an instance of the {type(self).__name__} class"
        )
        parser.add_argument(
            "-a",
            f"--{OPTION_ONE_KEY}",
            dest="OPTION_ONE",
            help='An option that has a default that is "'
            + str(_DEFAULTS[CONFIG_FILE_KEY])
            + '"',
        )
        parser.add_argument(
            "-b",
            f"--{OPTION_THE_OTHER_KEY}",
            dest="OPTION_THE_OTHER",
            help="The other option, that does not have a default",
        )
        parser.add_argument(
            "-i",
            f"--{CONFIG_FILE_KEY}",
            dest="CONFIG_FILE",
            help="The path to the configuration file",
        )
        parser.add_argument(
            "-s",
            f"--{CONFIG_SECTION_KEY}",
            dest="CONFIG_SECTION",
            help="The section of the INI file to use for this execution",
        )
        return parser

    def execute(self):
        """
        Executes the responsibilities of this executable
        """
        if None is not self.__params:
            for key, value in self.__params.items():
                if None is value:
                    logging.info('Option "%s" has no value', key)
                else:
                    logging.warning('Option "%s" has value "%s"', key, value)

    def get_config_file_key(self) -> Optional[str]:
        """
        Returns the name of the config file to use, if any.
        """
        return CONFIG_FILE_KEY

    def get_config_section_key(self) -> Optional[str]:
        """
        Returns the section of the config file to use, if any.
        """
        return CONFIG_SECTION_KEY

    def get_defaults(self) -> Optional[Config]:
        """
        Returns a Config containing the default for every config item that has one.
        """
        return _DEFAULTS

    def get_envar_mapping(self) -> Dict[str, str]:
        """
        Return a dictionary that maps environmental variables onto option variables.
        """
        return {
            "CONFIG_CONFIG_FILE": "CONFIG_FILE",
            "CONFIG_CONFIG_SECTION": "CONFIG_SECTION",
            "CONFIG_OPTION_ONE": "OPTION_ONE",
            "CONFIG_OPTION_THE_OTHER": "OPTION_THE_OTHER",
        }

    def get_interval(self) -> Optional[float]:
        """
        Returns the number of seconds to wait between executions.
        """
        return -1

    def get_log_level_key(self) -> Optional[str]:
        """
        Returns the name of the log level to use, if any.
        """
        return LOG_LEVEL_KEY

    def get_param_names(self) -> List[str]:
        """
        Returns a List of the config items that should be included when building the parameters
        passed in to 'set_params'. If this in None, 'set_params' will not be called.
        """
        return [
            OPTION_ONE_KEY,
            OPTION_THE_OTHER_KEY,
        ]

    def set_params(self, params: Dict[str, Any]) -> Optional[str]:
        """
        Informs the Task of the new set of parameters it should use.

        Returns:
            None if the parameters values are valid, otherwise it is the reason why
            configuration failed.
        """
        if OPTION_ONE_KEY in params and "invalid" == params[OPTION_ONE_KEY]:
            return f'{OPTION_ONE_KEY} must not have the value "invalid"'
        self.__params = params
        logging.info("The new set of parameters has been set")
        return None

    def updated_configuration(self, _: Config) -> None:
        """
        Informs this instance of the contents of the current configuration file. This can be
        used to construct the return value of 'get_param_names'.
        """
        self.__params = None
        logging.info("The configuration been updated")
