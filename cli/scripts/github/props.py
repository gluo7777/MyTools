from cli.scripts.config import Properties
import unittest


class GitHubProperties(Properties):

    USER = 'user'
    ACCESS_TOKEN = 'access_token'
    API_URL = 'api_url'
    HEADER_ACCEPT = 'header.accept'
    HEADER_CONTENT_TYPE = 'header.content-type'
    TIMEOUT = 'request.timeout'

    def __init__(self):
        super().__init__('GitHub')
        self.set_if_missing(GitHubProperties.API_URL, 'https://api.github.com')
        self.set_if_missing(GitHubProperties.HEADER_ACCEPT,
                            'application/vnd.github.v3+json')
        self.set_if_missing(
            GitHubProperties.HEADER_CONTENT_TYPE, 'application/json')
        self.set_if_missing(GitHubProperties.TIMEOUT, '20')
