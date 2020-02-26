from cli.scripts.github.props import GitHubProperties
import unittest

class GitHubPropertiesTest(unittest.TestCase):

    def setUp(self):
        self.props = GitHubProperties()

    def test_default_props(self):
        self.assertIsNotNone(self.props.get(GitHubProperties.API_URL))
        self.assertIsNotNone(self.props.get(GitHubProperties.HEADER_ACCEPT))
        self.assertIsNotNone(self.props.get(GitHubProperties.HEADER_CONTENT_TYPE))
        self.assertGreater(int(self.props.get(GitHubProperties.TIMEOUT)), 0)

def suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(testCaseClass=GitHubPropertiesTest)

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())