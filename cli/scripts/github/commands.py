import click
import cli.scripts.context as global_context
from cli.scripts.github.props import GitHubProperties
from cli.scripts.github.client import Client
from cli.scripts.exceptions import exception_handler
from cli.scripts.github.exceptions import GitHubError,GitHubErrorHandler

props = GitHubProperties()
client = Client(props)
error_handler = GitHubErrorHandler(GitHubErrorHandler.standard_error).build()

def not_blank(ctx, param, value):
    if value is None or value == '':
        raise click.BadParameter('cannot be blank')
    else:
        return value

@click.group(name="github")
@exception_handler(target=GitHubError, handler=error_handler)
def commands():
    global_context.debug("Running github command...")
    prompt_if_missing('Username', GitHubProperties.USER)
    prompt_if_missing('Access Token', GitHubProperties.ACCESS_TOKEN, sensitive=True)
    pass

@commands.group(name='repo')
def repo():
    pass

def get_pretty_printed_repos():
    i = 0
    for repo in client.get_repositories():
        yield f"{str(i).zfill(4)} : {repo.get('name')} ({repo.get('id')})\n"
        i += 1

@repo.command(name='list')
@click.option('-c','--count', is_flag=True, type=int, help="Print number of repositories", default=False)
@click.option('-s','--sort', type=click.Choice(['created', 'updated', 'pushed', 'full_name'], case_sensitive=False))
@click.option('-d','--direction',type=click.Choice(['asc','desc'], case_sensitive=False))
@exception_handler(target=GitHubError, handler=error_handler)
def list_repos(count, sort, direction):
    if count:
        size = 0
        for repo in client.get_repositories():
            size += 1
        click.echo(f"Number of repositories = {size}.")
    else:
        click.clear()
        click.echo_via_pager(get_pretty_printed_repos())

@repo.command(name='create')
@click.option('-n','name', prompt=True, type=str,callback=not_blank)
@click.option('-d','--description', prompt=True, type=str, default='', show_default=False)
@click.option('-p','--private', is_flag=True, default=False)
@exception_handler(target=GitHubError, handler=error_handler)
def create_repo(name:str, description: str, private: bool):
    click.echo(f"Creating new repository {name}...")
    response = client.create_repository(name, description, private)
    click.echo(f"Successfully created repository {response['name']} ({response['id']})")
    click.echo(f"HTTPS: {response['https']}")
    click.echo(f"SSH: {response['ssh']}")
    click.echo(f"git clone {response['ssh']} .")

@repo.command(name='delete')
@click.option('-n','--name', prompt=True, type=str,callback=not_blank, confirmation_prompt=True)
@exception_handler(target=GitHubError, handler=error_handler)
def delete_repo(name: str):
    click.echo(f"Deleting repository {name}...")
    response = client.delete_repository(name)
    click.echo(f"Successfully deleted {name}")

@commands.command()
def issues():
    pass

def prompt_if_missing(name,option,sensitive=False,confirm=False):
    if not props.has(option):
        value = click.prompt(f"{name} is not set. Please enter {name}",hide_input=sensitive,confirmation_prompt=confirm)
        props.set(option, value)