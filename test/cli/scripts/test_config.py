from cli.scripts.config import Properties
import test
import unittest

class PropertiesTest(unittest.TestCase):

    def setUp(self):
        self.props = Properties
        self.props.CONFIG_DIR = test.RESOURCE_DIR

    def tearDown(self):
        pass