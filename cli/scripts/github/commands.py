import click
import cli.scripts.context as global_context

@click.group
def github():
    global_context.debug("Running github command...")
    pass

@github.command
def issues():
    pass