import click
import os
import sys

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
    if context['VERBOSE']:
        click.secho("Verbosity is enabled.", fg='green')
    click.echo("""Current Directory: %s\
        \nCurrent Directory: %s\
    """ % (
        os.path.abspath('.'),
        os.path.abspath('.')
    ))
    click.echo('Platform: %s' % os.name)
    click.echo('File System Encoding: %s' % sys.getdefaultencoding())