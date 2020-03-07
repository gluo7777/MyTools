import click
from cli.scripts.config import Properties
from cli.scripts.logging import LoggerUtil

class CLI():

    def __init__(self, props: Properties = None):
        super().__init__()
        self.props = props if props is not None else Properties('General')
        self.logger = LoggerUtil()

    def is_debug(self):
        context = click.get_current_context(silent=True)
        if context is None:
            return False
        return context.obj['VERBOSE'] or False

    def log(self, msg: str,stdout=True,file=True):
        if stdout:
            click.echo(msg)
        if file:
            self.logger.info(msg)
    
    def error(self, msg: str,stderr=True,file=True):
        if stderr:
            click.echo(msg, err=True)
        if file:
            self.logger.error(msg)

    def debug(self, msg:str, stdout=True, file=True):
        if not self.is_debug():
            return
        if stdout:
            click.echo(msg)
        if file:
            self.logger.debug(msg)

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