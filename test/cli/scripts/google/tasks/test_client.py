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