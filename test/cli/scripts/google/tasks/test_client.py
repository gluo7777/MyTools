import test
from cli.scripts.google.tasks.client import Client
from cli.scripts.google.tasks.properties import TaskProperties
import unittest.mock as mock

class ClientTest(test.DeleteResourceTest):

    def setUp(self):
        super().setUp()
        self.props = TaskProperties()
        self.client = Client(self.props)

    def test_base_url(self):
        self.assertEqual(
            'https://www.googleapis.com/tasks/v1'
            ,self.client.base
        )
    
    def test__rel_to_cur_user(self):
        self.assertEqual(
            'https://www.googleapis.com/tasks/v1/users/@me/tasks'
            ,self.client._rel_to_cur_user('tasks')
        )

    def test__rel_to_cur_user_multiple(self):
        self.assertEqual(
            'https://www.googleapis.com/tasks/v1/users/@me/tasks/12345/title'
            ,self.client._rel_to_cur_user('tasks','12345','title')
        )