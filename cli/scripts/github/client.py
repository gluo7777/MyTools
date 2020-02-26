import pip._vendor.requests as requests
from cli.scripts.github.props import GitHubProperties
import cli.scripts.context as global_context


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
            ,url=self.props.get(GitHubProperties.API_URL + '/user/repos')
            ,auth={
                'username': GitHubProperties.USER
                ,'password': GitHubProperties.ACCESS_TOKEN
            }
            ,json={
                'name': name
                ,'description': description
                ,'private': is_private
                ,'homepage': 'https://github.com/' + GitHubProperties.USER + '/' + name
            }
            ,headers={
                'Accept': GitHubProperties.HEADER_ACCEPT
                ,'Content-Type': GitHubProperties.HEADER_CONTENT_TYPE
            }
            ,timeout=GitHubProperties.TIMEOUT
        )
        if response.status_code == 201:
            global_context.debug('Received 201 from /user/repos')
            return response.json()['html_url']
        else:
            global_context.log(f"Received response code {response.status_code} from GitHub API with message '{response.json()['message'] or 'null'}'.")
            return None