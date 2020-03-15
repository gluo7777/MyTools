import test
import unittest
import os
from cli.scripts.logger import LoggerUtil, LoggerProperties
from logging import Logger

class LoggerUtilTest(test.DeleteResourceTest):

    def setUp(self):
        super().setUp()
        LoggerProperties.CONFIG_FILE = 'loggerproperties.ini'
        self.props = LoggerProperties()
        self.logger = LoggerUtil(self.props)
        
    def test_properties(self):
        for k,v in {
            'directory': os.path.abspath(LoggerProperties.CONFIG_DIR + '/logging')
            ,'log_file': 'main.log'
            ,'error_file': 'error.log'
        }.items():
            self.assertEqual(v,self.props.get(k))

    def test_init_log_handles(self):
        for handle in ['log','info','debug','warning','error']: 
            handle_value = self.logger.__dict__[handle]
            self.assertIsNotNone(handle_value)

    def test_main_log_file_created_when_info(self):
        self.logger.info('hello world')
        self.assertTrue(os.path.exists(os.path.abspath(LoggerProperties.CONFIG_DIR + '/logging' + '/main.log')))

    def test_main_log_file_created_when_debug(self):
        self.logger.debug('hello world')
        self.assertTrue(os.path.exists(os.path.abspath(LoggerProperties.CONFIG_DIR + '/logging' + '/main.log')))

    def test_error_log_file_created_when_error(self):
        self.logger.error('hello world')
        self.assertTrue(os.path.exists(os.path.abspath(LoggerProperties.CONFIG_DIR + '/logging' + '/error.log')))

    def test_error_log_file_created_when_warning(self):
        self.logger.warning('hello world')
        self.assertTrue(os.path.exists(os.path.abspath(LoggerProperties.CONFIG_DIR + '/logging' + '/error.log')))

    def tearDown(self):
        self.logger.close()
        return super().tearDown()