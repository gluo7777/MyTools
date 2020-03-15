import click
from cli.scripts.google.tasks.client import Client
from cli.scripts.google.tasks.properties import TaskProperties
from cli.scripts.utility import CLI

props = TaskProperties()
client = Client(props)
cli = CLI(props)

@click.group(name="tasks")
def commands():
    pass

def _task_list_titles(*args,**kwargs):
    """
    # | title |  last updated | id |
    """
    lens = [4,20,30,60]
    i = 0
    yield cli.column_padding(['#','Title','Last Updated','Id'],lens,orientation=CLI.CENTER) + '\n'
    for task_list in client.get_task_lists(*args,**kwargs):
        i += 1
        yield cli.column_padding(
            [
                i
                ,task_list.get('title')
                ,task_list.get('updated')
                ,task_list.get('id')
            ]
            ,lens
            ,orientation=CLI.CENTER
        ) + '\n'

def _task_titles(*args,**kwargs):
    """
    # | title | due |
    """
    lens = [4,20,30]
    i = 0
    yield cli.column_padding(['#','Title','Due'],lens,orientation=CLI.CENTER) + '\n'
    for task_list in client.get_tasks(*args,**kwargs):
        i += 1
        yield cli.column_padding(
            [
                i
                ,task_list.get('title')
                ,task_list.get('due')
            ]
            ,lens
            ,orientation=CLI.CENTER
        ) + '\n'

@commands.command(name='list', help='Show task lists')
def task_list():
    click.echo_via_pager(_task_list_titles())

@commands.command(name='get', help='Get 0 or more tasks')
@click.argument('list title')
def get_tasks(list_title:str):
    click.echo(_task_titles(list_title))