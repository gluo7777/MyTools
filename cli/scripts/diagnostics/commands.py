import click
import os,platform,sys
from cli.scripts.context import is_debug
import cli.scripts.context as global_context
from cli.scripts.config import Properties

props = Properties('Diagnostics')

@click.group()
@click.pass_context
def info(context):
    global_context.debug('Running info command')

@info.command()
@click.pass_context
def system(context):
    global_context.debug("Obtaining system diagnostics...")
    path = os.path.abspath('.')
    ntpath = path
    posixpath = path
    # TODO: derive nt/posix path from the other
    click.echo(
        "Working Directory"
        f"\nWindows Path: {ntpath}"
        f"\nLinux Path: {posixpath}"
    )
    click.echo('Platform: %s' % os.name)
    click.echo("Operating System:"
        f"{platform.system()}.{platform.version()}"
        f".{platform.release()}.{platform.node()}"
        f".{platform.machine()}.{platform.processor()}")
    click.echo('File System Encoding: %s' % sys.getdefaultencoding())