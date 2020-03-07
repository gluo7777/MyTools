import click
from cli.scripts.github.props import GitHubProperties
from cli.scripts.github.client import Client
from cli.scripts.exceptions import exception_handler
from cli.scripts.github.exceptions import GitHubError,GitHubErrorHandler
from cli.scripts.utility import CLI

cli = CLI()
props = GitHubProperties()
client = Client(props)
error_handler = GitHubErrorHandler(GitHubErrorHandler.standard_error).build()

@click.group(name="github")
@exception_handler(target=GitHubError, handler=error_handler)
def commands():
    cli.debug("Running github command...")
    cli.prompt_if_missing('Username', GitHubProperties.USER)
    cli.prompt_if_missing('Access Token', GitHubProperties.ACCESS_TOKEN, sensitive=True)
    pass

@commands.group(name='repo')
def repo():
    pass

def get_pretty_printed_repos(*args):
    i = 1
    for repo in client.get_repositories(*args):
        yield f"{str(i).zfill(4)} : {repo.get('name')} ({repo.get('id')})\n"
        i += 1

@repo.command(name='list')
@click.option('-c','--count', is_flag=True, type=int, help="Print number of repositories", default=False)
@click.option('-s','--sort', type=click.Choice(['created', 'updated', 'pushed', 'full_name'], case_sensitive=False))
@click.option('-d','--direction',type=click.Choice(['asc','desc'], case_sensitive=False))
@exception_handler(target=GitHubError, handler=error_handler)
def list_repos(count, sort, direction):
    if count:
        click.echo(f"Number of repositories = {client.get_repositories_size(sort,direction)}.")
    else:
        click.clear()
        click.echo_via_pager(get_pretty_printed_repos(sort,direction))

@repo.command(name='create')
@click.option('-n','name', prompt=True, type=str,callback=cli.not_blank)
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
@click.option('-n','--name', prompt=True, type=str,callback=cli.not_blank, confirmation_prompt=True)
@exception_handler(target=GitHubError, handler=error_handler)
def delete_repo(name: str):
    click.echo(f"Deleting repository {name}...")
    response = client.delete_repository(name)
    click.echo(f"Successfully deleted {name}")

@commands.command()
def issues():
    pass