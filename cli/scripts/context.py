import click

def is_debug():
    context = click.get_current_context(silent=True)
    if context is None:
        return False
    return context.obj['VERBOSE'] or False

def log(msg,error=False):
    # if click.get_current_context(silent=True) is not None:
    #     click.echo(msg,err=error)
    pass

def debug(msg):
    if is_debug():
        log(msg)