import click
import cli.scripts.context as global_context
from cli.scripts.github.props import GitHubProperties
from cli.scripts.github.client import Client

props = GitHubProperties()
client = Client(props)

@click.group()
def github():
    global_context.debug("Running github command...")
    setup()
    pass

@github.command(name='create-repo')
def create_repo():
    name = click.prompt("Name")
    description = click.prompt('Description',default='')
    is_private = click.prompt('Private (true/false)', type=bool, default='false')
    global_context.log(f"Creating new {'private' if is_private else 'public'} repository '{name}'")
    repo_url = client.create_repository(name, description, is_private)
    if repo_url is not None:
        global_context.log(f"Successfully created repository {repo_url}")
    else:
        global_context.log(f"Failed to create repository")

@github.command()
def issues():
    pass

def setup():
    prompt_if_missing('Username', GitHubProperties.USER)
    prompt_if_missing('Access Token', GitHubProperties.ACCESS_TOKEN, sensitive=True)

def prompt_if_missing(name,option,sensitive=False,confirm=False):
    if not props.has(option):
        value = click.prompt(f"{name} is not set. Please enter {name}",hide_input=sensitive,confirmation_prompt=confirm)
        props.set(option, value)