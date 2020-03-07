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

# TODO: add column padding
def _task_list_titles(*args,**kwargs):
    """
    index | title | id | last updated
    """
    i = 0
    yield 'Title'
    for task_list in client.get_task_lists(*args,**kwargs):
        yield task_list['title']

@commands.command(name='list', help='Show task lists')
def task_list():
    click.echo_via_pager(_task_list_titles())