import click
import os
import sys
import platform

@click.group()
@click.option('--verbose', is_flag=True, default=False, help="Log extravaneous output")
@click.pass_context
def root(context, verbose):
    try:
        context.ensure_object(dict)
    except Exception as e:
        click.echo("Unable to initialize CLI context due to following error: \n%s" % e)
    context.obj['VERBOSE'] = verbose

@root.command('info')
@click.pass_context
def info(context):
    if context.obj['VERBOSE']:
        click.secho("Verbosity is enabled.", fg='green')
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