import click

def is_debug():
    context = click.get_current_context(silent=True)
    if context is None:
        return False
    return context.obj['VERBOSE'] or False

def log(msg,*args,**kwargs):
    if click.get_current_context(silent=True) is not None:
        click.echo(msg,args,kwargs)

def debug(msg,*args,**kwargs):
    if is_debug():
        log(msg, args, kwargs)