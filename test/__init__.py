import os
import test

_TEST_DIR = os.path.abspath(test.__file__+'/..')
print(f'TEST_DIR={_TEST_DIR}')
RESOURCE_DIR = os.path.abspath(f'{_TEST_DIR}/resources')
print(f'RESOURCE_DIR={RESOURCE_DIR}')