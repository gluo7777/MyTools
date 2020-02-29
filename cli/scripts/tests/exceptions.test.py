import unittest
import cli.scripts.exceptions as exceptions

class ExceptionHandlerTest(unittest.TestCase):
    
    def test_default_handler(self):
        @exceptions.exception_handler()
        def some_function():
            raise FileNotFoundError()
        try:
            some_function()
            self.fail(f"Expected exception to be thrown")
        except:
            print('successfully thrown exception')

    def test_exception_handler_for_specific_exception(self):
        def file_not_found_error_handler(fileNotFoundError):
            self.assertEqual(FileNotFoundError, type(fileNotFoundError))
        @exceptions.exception_handler(target=FileNotFoundError,handler=file_not_found_error_handler)
        def some_function():
            raise FileNotFoundError()
        some_function()

if __name__ == "__main__":
    unittest.main(verbosity=2)