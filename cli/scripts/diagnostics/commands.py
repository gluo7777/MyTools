import click
import os,platform,sys

@click.group()
@click.pass_context
def info(context):
    pass

@info.command()
@click.pass_context
def system(context):
    if context.obj['VERBOSE']:
        click.secho("Obtaining system diagnostics...", fg='green')
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