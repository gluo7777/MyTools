from cli.scripts.google.properties import GoogleProperties
import requests

# TODO: Create one parent client under scripts package
class Client():
    OAUTH2 = 'https://oauth2.googleapis.com'
    ACCOUNTS = 'https://accounts.google.com'
    API = 'https://www.googleapis.com'
    AUTH_URL = ACCOUNTS + '/o/oauth2/v2/auth'
    TOKEN_URL = OAUTH2 + '/token'
    REVOKE_URL = OAUTH2 + '/revoke'
    CONTENT_TYPE = 'application/x-www-form-urlencoded'
    REDIRECT = 'https://www.google.com'

    def __init__(self, props: GoogleProperties):
        self.props = props
        self._timeout = int(self.props.get(self.props.TIMEOUT))

    def _random_token(self):
        # TODO: make this random
        return 'lefoiiforji43joi3joi43jfoi3'

    def _authorization_header(self):
        return {'Authorization':f'Bearer {self.props.get(self.props.ACCESS_TOKEN)}'}

    def _application_x_www_form_urlencoded(self):
        return {'Content-Type':'application/x-www-form-urlencoded'}

    def _headers(self):
        headers = {}
        headers.update(self._authorization_header)
        return headers

    def _transform_scopes(self, scopes):
        return ','.join([ self.API + '/auth/' + scope for scope in scopes ])

    def consent_url(self, scopes) -> str:
        state_token = self._random_token()
        self.props.set(self.props.STATE_TOKEN, state_token)
        return  f'{self.AUTH_URL}'\
                + f'?access_type=offline'\
                + f'&client_id={self.props.get(self.props.CLIENT_ID)}'\
                + f'&redirect_uri={self.REDIRECT}'\
                + f'&response_type=code'\
                + f'&state={state_token}'\
                + f'&scope={self._transform_scopes(scopes)}'\
                + f'&include_granted_scopes=true'\
                + f'&prompt=consent'\

    def access_token(self, refresh:bool=False) -> str:
        response = requests.post(
            url=self.TOKEN_URL
            ,headers=self._application_x_www_form_urlencoded()
            ,data={
                'code': self.props.get(self.props.REFRESH_TOKEN) 
                        if refresh
                        else self.props.get(self.props.AUTHORIZATION_CODE)
                ,'client_id': self.props.get(self.props.CLIENT_ID)
                ,'client_secret': self.props.get(self.props.CLIENT_SECRET)
                ,'grant_type':  'refresh_token'
                                if refresh
                                else 'authorization_code'
                ,'redirect_uri': self.props.get(self.REDIRECT)
            }
            ,timeout=self._timeout
        )
        if response.ok:
            body = response.json()
            return {
                'access_token': body.access_token
                ,'refresh_token': body.refresh_token
            }
        else:
            raise ClientException(f'\nstatus={response.status_code}\nmessage={response.text}')

    def revoke_access(self):
        response = requests.post(
            url=self.REVOKE_URL
            ,headers=self._application_x_www_form_urlencoded()
            ,query={'token': self.props.get(self.props.ACCESS_TOKEN)}
            ,timeout=self._timeout
        )
        if not response.ok:
            body = response.json()
            raise ClientException(f'Failed to request access token: [{body.error}] {body.error_description}')

class ClientException(Exception):
    def __init__(self,msg:str='Error calling Google Cloud Services',*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg

    def __str__(self):
        return self.msg