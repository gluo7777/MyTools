from cli.scripts.google.client import Client as GoogleClient, refresh_token
from cli.scripts.google.tasks.properties import TaskProperties
from cli.scripts.client import Json
import requests

class Client(GoogleClient):

    MAX = 10

    def __init__(self, props: TaskProperties, paths:[str]=[]):
        paths_ = ['tasks','v1']
        paths_.extend(paths)
        super().__init__(props,paths=paths_)

    def _rel_to_cur_user(self, *paths: str) -> [str]:
        return super()._path('users','@me',*paths)

    @refresh_token()
    def get_task_lists(self):
        page_token = ''
        while page_token is not None:
            response = requests.get(
                url=self._rel_to_cur_user('lists')
                ,params={'maxResults':self.MAX,'pageToken':page_token}
                ,headers=self._authorization_header()
                ,timeout=self._timeout
            )
            with Json(response) as body:
                page_token = body.get('nextPageToken')
                for item in body.get('items', []):
                    yield item