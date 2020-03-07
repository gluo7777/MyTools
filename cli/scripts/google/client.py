from cli.scripts.google.properties import GoogleProperties
import requests
import re
import cli.scripts.client as client

# TODO: Create one parent client under scripts package
class Client(client.Client):
    OAUTH2 = 'https://oauth2.googleapis.com'
    ACCOUNTS = 'https://accounts.google.com'
    API = 'https://www.googleapis.com'
    AUTH_URL = ACCOUNTS + '/o/oauth2/v2/auth'
    TOKEN_URL = OAUTH2 + '/token'
    REVOKE_URL = OAUTH2 + '/revoke'
    CONTENT_TYPE = 'application/x-www-form-urlencoded'
    REDIRECT = 'https://www.google.com'

    def __init__(self, props: GoogleProperties):
        super().__init__(props)

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

    CODE_PATTERN = re.compile(r'.*code=(\d\/\w+)&.*')

    def extract_code_from_url(self, url:str) -> str:
        result = self.CODE_PATTERN.match(url)
        if result and result.group(1):
            return result.group(1)
        else:
            raise GoogleException('Failed to extract code from url')

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
                ,'redirect_uri': self.REDIRECT
            }
            ,timeout=self._timeout
        )
        if response.ok:
            with client.Json(response) as body:
                return {
                    'access_token': body.get('access_token')
                    ,'refresh_token': body.get('refresh_token')
                }
        else:
            raise GoogleException(f'\nstatus={response.status_code}\nmessage={response.text}')

    def revoke_access(self):
        response = requests.post(
            url=self.REVOKE_URL
            ,headers=self._application_x_www_form_urlencoded()
            ,query={'token': self.props.get(self.props.ACCESS_TOKEN)}
            ,timeout=self._timeout
        )
        with client.Json(response) as body:
            if not response.ok:
                raise GoogleException(f"Failed to request access token:\n{body}")

class GoogleException(client.ClientException):
    def __init__(self, msg='Error calling Google Services', *args, **kwargs):
        super().__init__(msg=msg, *args, **kwargs)