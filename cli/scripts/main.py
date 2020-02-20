import click

@click.group()
@click.option('--verbose', is_flag=True, default=False, help="Log extravaneous output")
@click.pass_context
def root(context, verbose):
    try:
        context.ensure_object(dict)
    except Exception as e:
        click.echo("Unable to initialize CLI context due to following error: \n%s" % e)
    context.obj['VERBOSE'] = verbose

