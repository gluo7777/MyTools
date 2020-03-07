import click
import cli.scripts.google.tasks.commands as tasks
from cli.scripts.utility import CLI
from cli.scripts.google.properties import GoogleProperties
from cli.scripts.google.client import Client

props = GoogleProperties()
cli = CLI(props)
client = Client(props)

REQUIRED_KEYS = [
    ('Google API Client Id', props.CLIENT_ID, True, False)
    ,('Google API Client Secret',props.CLIENT_SECRET, True, False)
]

OAUTH2_SCOPES = [ 'tasks' ]

@click.group(name="google",help="Interacting with Google APIs")
def commands():
    for name,key,secret,confirm in REQUIRED_KEYS:
        cli.prompt_if_missing(name,key,secret,confirm)
    
@commands.command(name='set-up', help='Re-enter value for each property in config.ini')
def set_up():
    for name,key,secret,confirm in REQUIRED_KEYS:
        cli.override_property(name,key,secret,confirm)

@commands.command(name='oauth2', help='Set up oauth2 credentials')
@click.option('-s','--scopes', type=click.Choice(OAUTH2_SCOPES), help='Google API scopes to request authorization for',multiple=True,default=OAUTH2_SCOPES)
def oauth2(scopes):
    # User authorizes this app
    consent_url = client.consent_url(scopes)

    # Store authorization code
    click.echo(f'Paste this into your browser to authorize this tool\n\n{consent_url}\n')
    redirect_url = click.prompt('Now paste the url that appears after redirecting', type=str)
    authorization_code = client.extract_code_from_url(redirect_url)
    props.set(props.AUTHORIZATION_CODE, authorization_code)
    
    # Obtain access token
    response = client.access_token()
    props.set(props.ACCESS_TOKEN, response[props.ACCESS_TOKEN])
    props.set(props.REFRESH_TOKEN, response[props.REFRESH_TOKEN])
