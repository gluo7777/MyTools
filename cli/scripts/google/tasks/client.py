from cli.scripts.google.client import Client as GoogleClient
from cli.scripts.google.tasks.properties import TaskProperties

class Client(GoogleClient):
    TASKS = GoogleClient.API + '/tasks/v1'
    def __init__(self, props: TaskProperties):
        super().__init__(props)