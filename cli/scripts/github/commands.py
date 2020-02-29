import click
import cli.scripts.context as global_context
from cli.scripts.github.props import GitHubProperties
from cli.scripts.github.client import Client

props = GitHubProperties()
client = Client(props)

@click.group(name="github")
def commands():
    global_context.debug("Running github command...")
    setup()
    pass

@commands.command(name='create-repo')
@click.option('-n','--name', prompt=True, type=str)
@click.option('-d','--description', prompt=True, type=str, default='', show_default=False)
@click.option('-p','--private', is_flag=True, default=False)
def create_repo(name: str, description: str, private: bool):
    global_context.log(f"Creating new {'private' if private else 'public'} repository '{name}'")
    response = client.create_repository(name, description, private)
    if response['success']:
        click.echo(f"Successfully created repository {response['name']}")
        click.echo(f"HTTPS: {response['https']}")
        click.echo(f"SSH: {response['ssh']}")
        click.echo(f"git clone {response['ssh']} .")
    else:
        click.echo(f"Failed to create repository")
        click.echo(response['error'], err=True)
        click.echo(response['errors'], err=True)

@commands.command()
def issues():
    pass

def prompt_if_null(name:str,in_type:str,val,default=None):
    """Values that are required but not passed"""
    if val is not None:
        return val
    else:
        return click.prompt(text=name,type=in_type,default=default)

def setup():
    prompt_if_missing('Username', GitHubProperties.USER)
    prompt_if_missing('Access Token', GitHubProperties.ACCESS_TOKEN, sensitive=True)

def prompt_if_missing(name,option,sensitive=False,confirm=False):
    if not props.has(option):
        value = click.prompt(f"{name} is not set. Please enter {name}",hide_input=sensitive,confirmation_prompt=confirm)
        props.set(option, value)