import click
import cli.scripts.context as global_context
from cli.scripts.github.props import GitHubProperties
from cli.scripts.github.client import Client

props = GitHubProperties()
client = Client(props)

def not_blank(ctx, param, value):
    if value is None or value == '':
        raise click.BadParameter('cannot be blank')
    else:
        return value

@click.group(name="github")
def commands():
    global_context.debug("Running github command...")
    prompt_if_missing('Username', GitHubProperties.USER)
    prompt_if_missing('Access Token', GitHubProperties.ACCESS_TOKEN, sensitive=True)
    pass

@commands.group(name='repo')
def repo():
    pass

def _generate_output():
    for idx in range(50000):
        yield "Line %d\n" % idx

@repo.command(name='list')
def list_repos():
    click.clear()
    repos = client.get_repos()
    click.echo_via_pager(_generate_output())

@repo.command(name='create')
@click.option('-n','--name', prompt=True, type=str,callback=not_blank)
@click.option('-d','--description', prompt=True, type=str, default='', show_default=False)
@click.option('-p','--private', is_flag=True, default=False)
def create_repo(name: str, description: str, private: bool):
    global_context.log(f"Creating new {'private' if private else 'public'} repository '{name}'")
    response = client.create_repository(name, description, private)
    if response['success']:
        click.echo(f"Successfully created repository {response['name']} ({response['id']})")
        click.echo(f"HTTPS: {response['https']}")
        click.echo(f"SSH: {response['ssh']}")
        click.echo(f"git clone {response['ssh']} .")
    else:
        click.echo(f"Failed to create repository")
        click.echo(response['error'], err=True)
        click.echo(response['errors'], err=True)

@repo.command(name='delete')
@click.option('-n','--name', prompt=True, type=str,callback=not_blank, confirmation_prompt=True)
def delete_repo(name: str):
    click.echo(f"Deleting repository {name}...")
    response = client.delete_repository(name)
    if response['success']:
        click.echo(f"Successfully deleted {name}")
    else:
        click.echo(f"Failed to delete repository")
        click.echo(response['error'], err=True)
        click.echo(response['errors'], err=True)

@commands.command()
def issues():
    pass

def prompt_if_missing(name,option,sensitive=False,confirm=False):
    if not props.has(option):
        value = click.prompt(f"{name} is not set. Please enter {name}",hide_input=sensitive,confirmation_prompt=confirm)
        props.set(option, value)