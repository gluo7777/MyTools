import pip._vendor.requests as requests
from cli.scripts.github.props import GitHubProperties
import cli.scripts.context as global_context
import json
from typing import List

# https://github.com/github/gitignore

class Client():
    def __init__(self, props: GitHubProperties):
        self.props = props

    def path(self,base=self.props.get(GitHubProperties.API_URL), *paths: List[str]):
        return base + "/" + "/".join(paths)

    def auth(self):
        return (self.props.get(GitHubProperties.USER),self.props.get(GitHubProperties.ACCESS_TOKEN))

    def headers(self):
        return {
            'Accept': self.props.get(GitHubProperties.HEADER_ACCEPT)
            ,'Content-Type': self.props.get(GitHubProperties.HEADER_CONTENT_TYPE)
        }

    def timeout(self):
        return int(self.props.get(GitHubProperties.TIMEOUT))

    def user(self):
        return self.props.get(GitHubProperties.USER)

    def issues(self):
        pass

    def create_repository(self, name: str, description: str, is_private=True) -> str:
        response = requests.post(
            url=self.path('user','repos')
            ,auth=self.auth()
            ,data=json.dumps({
                'name': name
                ,'description': description
                ,'private': is_private
                ,'homepage': self.path(base='https://github.com/',paths=[self.props.get(GitHubProperties.USER),name])
            })
            ,headers=self.headers()
            ,timeout=self.timeout()
        )
        body = {}
        try:
            body = response.json()
        except:
            pass
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
        body = {}
        try:
            body = response.json()
        except:
            pass
        return {
            'success': response.status_code == 204
            ,'error': body.get('message')
            ,'errors': ','.join([error.get('message') for error in body.get('errors')]) if body.get('errors') else None
        }