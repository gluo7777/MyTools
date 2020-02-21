import click
import os
import sys
import platform
import cli.scripts.diagnostics.commands as diagnostics

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

cli.add_command(diagnostics.info)
cli()