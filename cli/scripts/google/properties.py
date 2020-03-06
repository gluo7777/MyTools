from cli.scripts.config import Properties

class GoogleProperties(Properties):
    SECTION = "Google"
    CLIENT_ID = "client_id"
    CLIENT_SECRET = "client_secret"
    API_KEY = "api_key"
    AUTHORIZATION_CODE = "authorization_code"
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"
    STATE_TOKEN = "state_token"
    TIMEOUT = "client_timeout"

    def __init__(self):
        super().__init__(self.SECTION)
        self.set_if_missing(self.TIMEOUT, '10')