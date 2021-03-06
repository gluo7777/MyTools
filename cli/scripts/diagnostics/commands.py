import click
import os
import platform
import sys
from cli.scripts.utility import CLI
from cli.scripts.config import Properties

props = Properties('Diagnostics')
cli = CLI()


@click.group(name="info")
@click.pass_context
def commands(context):
    cli.debug('Running info command')


@commands.command()
@click.pass_context
def system(context):
    cli.debug("Obtaining system diagnostics...")
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
