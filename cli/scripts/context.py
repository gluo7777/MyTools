import click

def is_debug():
    return click.get_current_context().obj['VERBOSE'] or False