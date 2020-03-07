from cli.scripts.config import Properties
import test
import unittest
import os

class PropertiesTest(unittest.TestCase):

    def setUp(self):
        self.props = Properties('Config',CONFIG_DIR=test.RESOURCE_DIR)

    def test_fields_not_null(self):
        for k,v in self.props.__dict__.items():
            if not str(k).startswith('__'):
                self.assertIsNotNone(v,f'{k} is None')

    def tearDown(self):
        os.remove(self.props.CONFIG_FILE)