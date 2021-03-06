import test
from cli.scripts.google.client import Client, GoogleException
import unittest.mock as m
from cli.scripts.google.properties import GoogleProperties


class ClientTest(test.DeleteResourceTest):
    def setUp(self):
        super().setUp()
        self.props = GoogleProperties()
        self.props.get = m.Mock(return_value='10')
        self.client = Client(self.props)

    def test__authorization_header(self):
        self.props.get = m.Mock(return_value='abcd')
        self.assertEqual(self.client._authorization_header()
                         ['Authorization'], 'Bearer abcd')
        self.props.get.assert_called_once_with(GoogleProperties.ACCESS_TOKEN)

    def test__application_x_www_form_urlencoded(self):
        self.assertEqual(self.client._application_x_www_form_urlencoded()[
                         'Content-Type'], 'application/x-www-form-urlencoded')

    def test__transform_scopes(self):
        self.client.API = 'www.google.com'
        full_scopes = self.client._transform_scopes(['test', 'tasks', 'email'])
        self.assertEqual(
            "www.google.com/auth/test,www.google.com/auth/tasks,www.google.com/auth/email", full_scopes
        )

    def test_consent_url(self):
        self.client._transform_scopes = m.Mock(
            return_value='www.google.com/auth/test')
        self.client._random_token = m.Mock(return_value='abcd')
        self.client.props.get = m.Mock(return_value='clientid')

        url = self.client.consent_url(['test'])
        self.assertEqual(f'{self.client.AUTH_URL}'
                         + f'?access_type=offline'
                         + f'&client_id=clientid'
                         + f'&redirect_uri={self.client.REDIRECT}'
                         + f'&response_type=code'
                         + f'&state=abcd'
                         + f'&scope=www.google.com/auth/test'
                         + f'&include_granted_scopes=true'
                         + f'&prompt=consent', url
                         )

        self.client._transform_scopes.assert_called_once_with(['test'])
        self.client.props.get.assert_called_once_with(
            GoogleProperties.CLIENT_ID)

    def test_extract_code_from_url(self):
        code = self.client.extract_code_from_url(
            r'https://www.google.com/?state=lefoiiforji43joi3joi43jfoi3&code=4/xQHwVU_ANFz94g-SOSmU-JqVdYEc2L1uUp5fF0BUMn1YFXxyTLz3-nTxoEe30dm0bulZO6bMO4c-C7GfeZ5WGXk&scope=https://www.googleapis.com/auth/tasks')
        self.assertEqual(
            code, r'4/xQHwVU_ANFz94g-SOSmU-JqVdYEc2L1uUp5fF0BUMn1YFXxyTLz3-nTxoEe30dm0bulZO6bMO4c-C7GfeZ5WGXk')

    def tearDown(self):
        super().tearDown()
