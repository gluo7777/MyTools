from cli.scripts.config import Properties
import requests

class Client:

    TIMEOUT = 'timeout'
    DEFAULT_TIMEOUT = 10

    def __init__(self, props: Properties):
        super().__init__()
        self.props = props
        self.base = 'http://localhost'
        self.props.set_if_missing(self.TIMEOUT, str(self.DEFAULT_TIMEOUT))
        self._timeout = int(self.props.get(self.TIMEOUT))

    def _path(self,*paths: str) -> str:
        return self.base + "/" + "/".join(paths)

class ClientException(Exception):
    def __init__(self,msg:str='Error calling API',*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = msg

    def __str__(self):
        return self.msg

class Json(object):
    def __init__(self, response: requests.Response):
        super().__init__()
        self.response = response

    def __enter__(self) -> dict:
        try:
            return self.response.json()
        except:
            return {}

    def __exit__(self, exception_type, exception_value, traceback):
        pass
