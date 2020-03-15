from cli.scripts.github.props import GitHubProperties
import unittest
import test

class GitHubPropertiesTest(test.DeleteResourceTest):

    def setUp(self):
        super().setUp()
        self.props = GitHubProperties()

    def test_default_props(self):
        self.assertIsNotNone(self.props.get(GitHubProperties.API_URL))
        self.assertIsNotNone(self.props.get(GitHubProperties.HEADER_ACCEPT))
        self.assertIsNotNone(self.props.get(GitHubProperties.HEADER_CONTENT_TYPE))
        self.assertGreater(int(self.props.get(GitHubProperties.TIMEOUT)), 0)

    def test_set_option(self):
        self.props.set(GitHubProperties.TIMEOUT, '10')
        self.assertTrue(self.props.has(GitHubProperties.TIMEOUT))