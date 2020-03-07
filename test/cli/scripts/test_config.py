from cli.scripts.config import Properties
import test
import unittest
import os
from pathlib import Path
from configparser import ExtendedInterpolation

class PropertiesTest(unittest.TestCase):

    def setUp(self):
        self.props = Properties('Config',CONFIG_DIR=test.RESOURCE_DIR, CONFIG_FILE=f'propertiestest.ini')

    def test_values(self):
        self.assertEqual(self.props.CONFIG_DIR, test.RESOURCE_DIR)
        self.assertEqual(self.props.CONFIG_FILE, os.path.abspath(test.RESOURCE_DIR + '/' + 'propertiestest.ini'))
        self.assertFalse(self.props.FAILED_ONCE)
        self.assertEqual(self.props._section, 'Config')
        self.assertIsNotNone(self.props._parser)

    def test_config_file_creation(self):
        self.assertTrue(Path(self.props.CONFIG_FILE).is_file())
        self.assertTrue(Path(self.props.CONFIG_FILE).exists())

    def test_section_created(self):
        self.assertTrue(self.props._parser.has_section('Config'))

    def test_update_option(self):
        key = 'my.prop'
        val = 'abc'
        val2 = 'def'
        self.assertFalse(self.props.has(key))
        self.props.set(key,val)
        self.assertTrue(self.props.has(key))
        self.assertEqual(self.props.get(key), val)
        self.props.set(key,val2)
        self.assertTrue(self.props.has(key))
        self.assertEqual(self.props.get(key), val2)

    def tearDown(self):
        os.remove(self.props.CONFIG_FILE)