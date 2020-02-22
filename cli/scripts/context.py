import click

def is_debug():
    return click.get_current_context().obj['VERBOSE'] or False

def log(msg,error=False):
    click.echo(msg,err=error)

def debug(msg):
    if is_debug():
        click.echo(msg)