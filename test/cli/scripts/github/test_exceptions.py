from cli.scripts.github.exceptions import GitHubError,GitHubErrorHandler
import unittest

class GitHubErrorHandlerTest(unittest.TestCase):
    
    def test_handler_built_correctly(self):
        handler = GitHubErrorHandler(lambda msg: msg).build()
        self.assertTrue(callable(handler))
    
    def test_correct_output(self):
        def out_cb(msg):
            self.assertEqual(
                "Error Title\n\terror1\n\terror2\n\terror3"
                ,msg
            )
        handler = GitHubErrorHandler(out_cb).build()
        error = GitHubError(title='Error Title',errors=['error1','error2','error3'])
        output = handler(error)

if __name__ == "__main__":
    unittest.main(verbosity=2)