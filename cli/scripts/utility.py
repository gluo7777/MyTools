import click
from cli.scripts.config import Properties

class CLI():
    def __init__(self, props: Properties):
        super().__init__()
        self.props = props

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