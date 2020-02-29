import pip._vendor.requests as requests
from cli.scripts.github.props import GitHubProperties
import cli.scripts.context as global_context
import json

# https://github.com/github/gitignore

class Client():
    def __init__(self, props: GitHubProperties):
        self.props = props
        pass

    def issues(self):
        pass

    def create_repository(self, name: str, description: str, is_private=True) -> str:
        response = requests.request(
            method='POST'
            ,url=self.props.get(GitHubProperties.API_URL) + '/user/repos'
            ,auth=(
                self.props.get(GitHubProperties.USER)
                ,self.props.get(GitHubProperties.ACCESS_TOKEN)
            )
            ,data=json.dumps({
                'name': name
                ,'description': description
                ,'private': is_private
                ,'homepage': 'https://github.com/' + self.props.get(GitHubProperties.USER) + '/' + name
            })
            ,headers={
                'Accept': self.props.get(GitHubProperties.HEADER_ACCEPT)
                ,'Content-Type': self.props.get(GitHubProperties.HEADER_CONTENT_TYPE)
            }
            ,timeout=int(self.props.get(GitHubProperties.TIMEOUT))
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
        response = requests.request(
            method='DELETE'
            ,url=self.props.get(GitHubProperties.API_URL) 
                + '/repos/' 
                + self.props.get(GitHubProperties.USER)
                + '/' + name
            ,auth=(
                self.props.get(GitHubProperties.USER)
                ,self.props.get(GitHubProperties.ACCESS_TOKEN)
            )
            ,headers={
                'Accept': self.props.get(GitHubProperties.HEADER_ACCEPT)
                ,'Content-Type': self.props.get(GitHubProperties.HEADER_CONTENT_TYPE)
            }
            ,timeout=int(self.props.get(GitHubProperties.TIMEOUT))
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