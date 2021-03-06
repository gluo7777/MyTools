from typing import List
from typing import Callable
import click
import unittest


class GitHubError(Exception):
    def __init__(self, title: str = 'Error calling GitHub API', errors: List[str] = [], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.errors = errors


class GitHubErrorHandler():
    def __init__(self, out_cb: Callable):
        super().__init__()
        self.out_cb = out_cb

    def build(self):
        def error_handler(error: GitHubError):
            title = error.title if error.title is not None else 'Error making request against Github API'
            errors = '\n'.join(['\t' + error for error in error.errors])
            msg = f"{title}\n{errors}"
            self.out_cb(msg)
        return error_handler

    @staticmethod
    def standard_error(msg: str) -> None:
        click.echo(msg, err=True)
