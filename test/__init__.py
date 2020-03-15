import os
import test
import unittest
from pathlib import Path
from shutil import rmtree
import cli.scripts.logger as logcfg

_TEST_DIR = os.path.abspath(test.__file__+'/..')
print(f'TEST_DIR={_TEST_DIR}')
RESOURCE_DIR = os.path.abspath(f'{_TEST_DIR}/resources')
print(f'RESOURCE_DIR={RESOURCE_DIR}')

class DeleteResourceTest(unittest.TestCase):
    def setUp(self):
        if Path(RESOURCE_DIR).exists():
            self.tearDown()
        os.makedirs(RESOURCE_DIR,exist_ok=False)

    def tearDown(self):
        logcfg._logger.close()
        rmtree(RESOURCE_DIR)