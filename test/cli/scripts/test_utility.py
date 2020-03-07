import unittest
from cli.scripts.utility import CLI
from unittest.mock import Mock,MagicMock,patch
import click
from cli.scripts.logging import LoggerUtil
from cli.scripts.config import Properties

class CLITest(unittest.TestCase):

    @patch('cli.scripts.utility.LoggerUtil')
    @patch('cli.scripts.utility.Properties')
    def setUp(self,props,logger):
        super().setUp()
        self.cli = CLI()
        self.props = self.cli.props
        self.logger = self.cli.logger

    def test_in_click_context(self):
        click.get_current_context = Mock(return_value=object())
        self.assertTrue(self.cli.in_click_context())
        click.get_current_context.assert_called_with(silent=True)

    def test_is_debug(self):
        class Context:
            obj = {'VERBOSE': True}
        click.get_current_context = Mock(return_value=Context())

        self.assertTrue(self.cli.is_debug())

        click.get_current_context.assert_called_with(silent=True)

        Context.obj['VERBOSE'] = False

        self.assertFalse(self.cli.is_debug())

    def test_log(self):
        click.echo = Mock()
        # both
        self.cli.log('hello')
        click.echo.assert_called_once_with('hello')
        self.logger.info.assert_called_once_with('hello')

    def test_when_not_click_context(self):
        click.echo = Mock()
        self.cli.in_click_context = Mock(return_value=False)
        self.cli.log('hello')
        click.echo.assert_not_called()

    def test_prompt_if_missing_true(self):
        click.prompt = Mock(return_value='william')
        self.props.has = Mock(return_value=False)
        
        self.cli.prompt_if_missing('Your Name','Name')

        self.props.has.assert_called_once_with('Name')
        click.prompt.assert_called_once_with('Your Name is not set. Please enter Your Name',hide_input=False,confirmation_prompt=False)
        self.props.set.assert_called_once_with('Name','william')

    def test_prompt_if_missing_false(self):
        click.prompt = Mock()
        self.props.has = Mock(return_value=True)
        
        self.cli.prompt_if_missing('Your Name','Name')

        click.prompt.assert_not_called()

    def test_not_blank(self):
        with self.assertRaises(click.BadParameter):
            self.cli.not_blank(None,None,None)
        with self.assertRaises(click.BadParameter):
            self.cli.not_blank(None,None,'')

    def tearDown(self):
        super().tearDown()