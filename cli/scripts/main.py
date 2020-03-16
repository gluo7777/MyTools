import click
import os
import sys
import platform
from cli.scripts.diagnostics.commands import commands as diagnostics
from cli.scripts.github.commands import commands as github
from cli.scripts.google.commands import commands as google
from cli.scripts.video.commands import commands as video

@click.group()
@click.option('--verbose', is_flag=True, default=False, help="Log extravaneous output")
@click.pass_context
def cli(context, verbose):
    if verbose:
        click.echo("Running in Verbose Mode")
    try:
        context.ensure_object(dict)
        context.obj['VERBOSE'] = verbose
        return 0
    except Exception as e:
        click.echo("Unable to initialize CLI context due to following error: %s" % e)
        return 1

def entry():
    cli.add_command(diagnostics)
    cli.add_command(github)
    cli.add_command(google)
    cli.add_command(video)
    cli()

if __name__ == "__main__":
    entry()