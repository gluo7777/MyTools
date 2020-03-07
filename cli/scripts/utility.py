import click
from cli.scripts.config import Properties
import cli.scripts.logger as logcfg

class CLI():

    def __init__(self, props: Properties = None):
        super().__init__()
        self.props = props if props is not None else Properties('General')
        self.logger_ = logcfg.logger()

    def in_click_context(self):
        context = click.get_current_context(silent=True)
        return context is not None

    def is_debug(self):
        context = click.get_current_context(silent=True)
        if self.in_click_context():
            return context.obj['VERBOSE'] or False
        return False

    def log(self, msg: str,stdout=True,file=True):
        if stdout and self.in_click_context():
            click.echo(msg)
        if file:
            self.logger_.info(msg)
    
    def error(self, msg: str,stderr=True,file=True):
        if stderr and self.in_click_context():
            click.echo(msg, err=True)
        if file:
            self.logger_.error(msg)

    def debug(self, msg:str, stdout=True, file=True):
        if not self.is_debug():
            return
        if stdout:
            click.echo(msg)
        if file:
            self.logger_.debug(msg)

    def prompt_if_missing(self,name:str,option:str,sensitive:bool=False,confirm:bool=False):
        if not self.props.has(option):
            value = click.prompt(f"{name} is not set. Please enter {name}",hide_input=sensitive,confirmation_prompt=confirm)
            self.props.set(option, value)

    def override_property(self, name:str, option:str,sensitive:bool=False,confirm:bool=False):
        value = click.prompt(f"Please enter {name}",hide_input=sensitive,confirmation_prompt=confirm)
        self.props.set(option,value)

    def not_blank(self, ctx, param, value):
        if value is None or value == '':
            raise click.BadParameter('cannot be blank')
        else:
            return value

    LEFT = 'left'
    RIGHT = 'right'
    CENTER = 'center'

    def column_padding(self, columns, col_lens, orientation: str = LEFT, filler: str = ' ', sep: str = '|', border: bool = True):
        line = []
        assert len(columns) == len(col_lens)
        for i in range(0, len(columns)):
            pad_len = max(len(columns[i]),col_lens[i])
            if orientation == self.LEFT:
                line.append(columns[i].ljust(pad_len, filler))
            elif orientation == self.RIGHT:
                line.append(columns[i].rjust(pad_len, filler))
            else:
                line.append(columns[i].center(pad_len, filler))
        if border:
            line.insert(0,'')
            line.append('')
        return sep.join(line)