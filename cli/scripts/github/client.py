import pip._vendor.requests as requests
from cli.scripts.github.props import GitHubProperties
from cli.scripts.github.exceptions import GitHubError
import cli.scripts.context as global_context
import json
from typing import List,Tuple

# https://github.com/github/gitignore

class Client():
    def __init__(self, props: GitHubProperties):
        self.props = props

    def __path(self,*paths: str) -> str:
        return self.props.get(GitHubProperties.API_URL) + "/" + "/".join(paths)

    def __auth(self) -> Tuple[str,str]:
        return (self.props.get(GitHubProperties.USER),self.props.get(GitHubProperties.ACCESS_TOKEN))

    def __headers(self, *other_headers: List[Tuple[str,str]]) -> dict:
        headers = {
            'Accept': self.props.get(GitHubProperties.HEADER_ACCEPT)
            ,'Content-Type': self.props.get(GitHubProperties.HEADER_CONTENT_TYPE)
        }
        for name,value in other_headers:
            headers[name] = value
        return headers

    def __timeout(self) -> int:
        return int(self.props.get(GitHubProperties.TIMEOUT))

    def __user(self) -> str:
        return self.props.get(GitHubProperties.USER)

    def __get_body(self, response: requests.Response) -> dict:
        body = {}
        try:
            body = response.json()
        except:
            pass
        return {} if body is None else body

    def __process_response(self, response: requests.Response, successful_status_code: int = 200) -> dict:
        if not response:
            raise GitHubError()
        body = self.__get_body(response)
        if response.status_code != successful_status_code:
            if type(body) != dict:
                raise GitHubError()
            title = body.get('error','Error calling GitHub API')
            errors = [error.get('message') for error in body.get('errors',[])]
            raise GitHubError(title=title,errors=errors)
        else:
            return body

    def issues(self):
        pass

    def get_repositories(self) -> List[dict]:
        next_page = self.__path('users',self.__user(),'repos')
        while next_page:
            response = requests.get(
                url=next_page
                ,auth=self.__auth()
                ,headers=self.__headers(
                    ('User-Agent',self.__user())
                )
                ,timeout=self.__timeout()
            )
            body = self.__process_response(response)
            for repo in body:
                yield repo
            next_page = response.links.get('next',{}).get('url')

    def create_repository(self, name: str, description: str, is_private=True) -> dict:
        response = requests.post(
            url=self.__path('user','repos')
            ,auth=self.__auth()
            ,data=json.dumps({
                'name': name
                ,'description': description
                ,'private': is_private
                ,'homepage': '/'.join(['https://github.com/',self.__user(),name])
            })
            ,headers=self.__headers()
            ,timeout=self.__timeout()
        )
        body = self.__process_response(response, 201)
        return {
            'id': body.get('id')
            ,'name': body.get('name')
            ,'owner': body.get('owner.login')
            ,'https': body.get('html_url')
            ,'ssh': body.get('ssh_url')
        }

    def delete_repository(self, name: str) -> None:
        response = requests.delete(
            url=self.__path('repos',self.__user(),name)
            ,auth=self.__auth()
            ,headers=self.__headers()
            ,timeout=self.__timeout()
        )
        self.__process_response(response, 204)