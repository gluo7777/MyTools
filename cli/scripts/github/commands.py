import click
import cli.scripts.context as global_context
from cli.scripts.github.props import GitHubProperties
from cli.scripts.github.client import Client

props = GitHubProperties()
client = Client(props)

@click.group
def github():
    global_context.debug("Running github command...")
    setup()
    pass

@github.command
def issues():
    pass

def setup():
    prompt_if_missing('Access Token', GitHubProperties.ACCESS_TOKEN)
    prompt_if_missing('Username', GitHubProperties.USER)

def prompt_if_missing(name,option,sensitive=False,confirm=False):
    if not props.has(option):
        value = click.prompt(f"{name} is not set. Please enter {name}",hide_input=sensitive,confirmation_prompt=confirm)
        props.set(option, value)