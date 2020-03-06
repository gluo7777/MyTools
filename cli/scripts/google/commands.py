import click
import cli.scripts.google.tasks.commands as tasks
from cli.scripts.cli import CLI
from cli.scripts.google.properties import GoogleProperties
from cli.scripts.google.client import Client,ClientException

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
@commmands.option('-s','--scopes', type=click.Choice(OAUTH2_SCOPES), help='Google API scopes to request authorization for',default=OAUTH2_SCOPES)
def oauth2(scopes):
    # User authorizes this app
    consent_url = client.consent_url(scopes)
    click.echo(f'Consent URL\nPaste this into your browser to authorize this tool\n{consent_url}')
    # Store authorization code
    authorization_code = click.prompt('Now enter the authorization code that appears in the url', type=str)
    props.set(props.AUTHORIZATION_CODE, authorization_code)
    # Obtain access token
    response = client.access_token()
    props.set(props.ACCESS_TOKEN, response['access_token'])
    props.set(props.REFRESH_TOKEN, response['refresh_token'])
