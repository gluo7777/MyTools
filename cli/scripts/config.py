import os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

class Properties:

    CONFIG_DIR = os.path.expanduser('~/mytools')
    CONFIG_FILE = 'config.ini'
    FAILED_ONCE = False

    def __init__(self, section):
        self.CONFIG_FILE =  os.path.abspath(self.CONFIG_DIR + '/' + self.CONFIG_FILE)
        self._section = section
        self._parser = ConfigParser(
            allow_no_value=True,
            comment_prefixes='#',
            strict=True,
            empty_lines_in_values=False,
            interpolation=ExtendedInterpolation()
        )

        if not os.path.exists(self.CONFIG_FILE) and not self.FAILED_ONCE:
            try:
                os.makedirs(self.CONFIG_DIR,exist_ok=True)
                open(self.CONFIG_FILE, 'w').close()
            except Exception as e:
                self.FAILED_ONCE = True

        if not self.FAILED_ONCE:
            self._parser.read(self.CONFIG_FILE)

        if not self._parser.has_section(self._section):
            self._parser.add_section(self._section)
            self.persist()
    
    def get(self, option:str, fallback=None) -> str:
        return self._parser.get(self._section, option, fallback=fallback)

    def set(self, option:str, value:str, persist=True):
        self._parser.set(self._section,option,value)
        if persist:
            self.persist()
    
    def has(self, *options:str) -> bool:
        for option in options:
            if not self._parser.has_option(self._section, option):
                return False
        return True

    def set_if_missing(self, option:str, value:str, persist=True):
        if not self.has(option):
            self.set(option, value, persist)

    def persist(self):
        with open(self.CONFIG_FILE, mode='w') as fp:
            self._parser.write(fp)
