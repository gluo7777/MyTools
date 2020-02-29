import pip._vendor.requests as requests
from cli.scripts.github.props import GitHubProperties
import cli.scripts.context as global_context
import json
from typing import List
from typing import Tuple

# https://github.com/github/gitignore

class Client():
    def __init__(self, props: GitHubProperties):
        self.props = props

    def path(self,*paths: str):
        return self.props.get(GitHubProperties.API_URL) + "/" + "/".join(paths)

    def auth(self):
        return (self.props.get(GitHubProperties.USER),self.props.get(GitHubProperties.ACCESS_TOKEN))

    def headers(self, *other_headers: List[Tuple[str,str]]):
        headers = {
            'Accept': self.props.get(GitHubProperties.HEADER_ACCEPT)
            ,'Content-Type': self.props.get(GitHubProperties.HEADER_CONTENT_TYPE)
        }
        for name,value in other_headers:
            headers[name] = value
        return headers

    def timeout(self):
        return int(self.props.get(GitHubProperties.TIMEOUT))

    def user(self):
        return self.props.get(GitHubProperties.USER)

    def issues(self):
        pass

    def get_body(self, response: requests.Response):
        body = {}
        try:
            body = response.json()
        except:
            pass
        return {} if body is None else body

    def get_repositories(self, *args):
        response = requests.get(
            url=self.path('users',self.user(),'repos')
            ,auth=self.auth()
            ,headers=self.headers(
                ('User-Agent',self.user())
            )
            ,timeout=self.timeout()
        )
        body = self.get_body(response)
        if response.status_code != 200:
            return {
                'error': body.get('message','Failed to retrieve repositories')
                ,'errors': ','.join([error.get('message') for error in body.get('errors')]) if body.get('errors') else None
            }
        for repo in body:
            yield repo

    def create_repository(self, name: str, description: str, is_private=True) -> str:
        response = requests.post(
            url=self.path('user','repos')
            ,auth=self.auth()
            ,data=json.dumps({
                'name': name
                ,'description': description
                ,'private': is_private
                ,'homepage': '/'.join(['https://github.com/',self.user(),name])
            })
            ,headers=self.headers()
            ,timeout=self.timeout()
        )
        body = self.get_body(response)
        return {
            'success': response.status_code == 201
            ,'id': body.get('id')
            ,'name': body.get('name')
            ,'owner': body.get('owner.login')
            ,'https': body.get('html_url')
            ,'ssh': body.get('ssh_url')
            ,'error': body.get('message')
            ,'errors': ','.join([error.get('message') for error in body.get('errors')]) if body.get('errors') else None
        }

    def delete_repository(self, name: str):
        response = requests.delete(
            url=self.path('repos',self.user(),name)
            ,auth=self.auth()
            ,headers=self.headers()
            ,timeout=self.timeout()
        )
        body = self.get_body(response)
        return {
            'success': response.status_code == 204
            ,'error': body.get('message')
            ,'errors': ','.join([error.get('message') for error in body.get('errors')]) if body.get('errors') else None
        }