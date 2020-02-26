import os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path
import cli.scripts.context as context

CONFIG_DIR = os.path.expanduser('~/mytool')
CONFIG_FILE = os.path.abspath(CONFIG_DIR + '/' + 'config.ini')

class Properties:

    FAILED_ONCE = False

    def __init__(self, section):
        self.section = section
        self.parser = ConfigParser(
            allow_no_value=True,
            comment_prefixes='#',
            strict=True,
            empty_lines_in_values=False,
            interpolation=ExtendedInterpolation()
        )

        if not os.path.exists(CONFIG_FILE) and not Properties.FAILED_ONCE:
            context.log(f"Creating config file at {CONFIG_FILE}")
            try:
                os.makedirs(CONFIG_DIR,exist_ok=True)
                open(CONFIG_FILE, 'w').close()
                self.parser.read(CONFIG_FILE)
            except Exception as e:
                context.log(f"Failed to create config file: {e}", error=True)
                Properties.FAILED_ONCE = True

        if not self.parser.has_section(self.section):
            self.parser.add_section(section)
            self.persist()
    
    def get(self, option:str, fallback=None) -> str:
        return self.parser.get(self.section, option, fallback=fallback)

    def set(self, option:str, value:str, persist=True):
        self.parser.set(self.section,option,value)
        if persist:
            context.debug('Persisting property {self.section}.{option}={value}')
            self.persist()
    
    def has(self, option):
        return self.parser.has_option(self.section, option)

    def set_if_missing(self, option, value, persist=True):
        if not self.has(option):
            self.set(option, value, persist)

    def persist(self):
        try:
            with open(CONFIG_FILE, mode='w') as fp:
                self.parser.write(fp)
        except Exception as e:
            context.log('Failed to persist properties: {e}', error=True)