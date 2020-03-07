import re
from datetime import datetime, timezone
import logging
import os
import sys
from cli.scripts.config import Properties

class LoggerProperties(Properties):
    __DIR = 'directory'
    __MAIN_FILE = 'logfile'
    __ERROR_FILE = 'errorfile'
    
    def __init__(self):
        super().__init__('Logging')
        self.set_if_missing(self.__DIR, os.path.abspath(self.CONFIG_DIR + '/logging'))
        self.set_if_missing(self.__MAIN_FILE, 'main.log')
        self.set_if_missing(self.__ERROR_FILE, 'error.log')

class LoggerUtil:
    """
    Utility class that wraps around two custom loggers for general logging and error logging
    """

    def __init__(self, props: LoggerProperties):
        self._main = LoggerUtil.setup_logger("MAIN", self.props.get(self.props.__DIR), self.props.get(self.props.__MAIN_FILE))
        self._error = ("ERROR", self.props.get(self.props.__DIR), self.props.get(self.props.__ERROR_FILE))

        self.log = self._main.log
        self.info = self._main.info
        self.debug = self._main.debug
        self.warning = self._error.warning
        self.error = self._error.error

    @staticmethod
    def setup_logger(name, log_dir, file, level=logging.DEBUG):
        log_file = os.path.join(log_dir, file)

        if not os.path.exists(log_file):
            os.makedirs(log_dir, exist_ok=True)
            open(log_file, "w").close()

        formatter = logging.Formatter(
            "%(asctime)s:%(levelname)s:%(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")

        handler = logging.FileHandler(filename=log_file, encoding="utf-8")
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger