import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
import sys
import os, requests
import coverage

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/jellyfaas')))

from jellyfaas import *

class TestClientInit(unittest.TestCase):

    # Success
    @patch('jellyfaas.requests.get')
    def test_init_success(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'token': 'test_token',
            'expiry': 'test_expiry'
        }
        mock_get.return_value = mock_response

        client = Client('test_api_key').set_debug_mode(True)
        self.assertEqual(client._api_key, 'test_api_key')
        self.assertEqual(client._token, 'test_token')
        self.assertEqual(client._token_expiry, 'test_expiry')
        self.assertEqual(client._do_debug, True)

    # HTTP Error 401
    @patch('jellyfaas.requests.get')
    def test_invalid_api_key(self, mock_get):
        error_response_mock = MagicMock()
        type(error_response_mock).status_code = PropertyMock(return_value=401)
        error_response_mock.raise_for_status.side_effect = requests.exceptions.HTTPError(response=error_response_mock)
        
        mock_get.return_value = error_response_mock

        with self.assertLogs(level='ERROR') as log:
            with self.assertRaises(AuthenticationFailedException):
                client = Client('invalid_api_key')
            self.assertIn('401 Client Error: Invalid API key', log.output[0])

    # HTTP Error 404
    @patch('jellyfaas.requests.get')
    def test_auth_not_found_error(self, mock_get):
        error_response_mock = MagicMock()
        type(error_response_mock).status_code = PropertyMock(return_value=404)
        error_response_mock.raise_for_status.side_effect = requests.exceptions.HTTPError(response=error_response_mock)
        
        mock_get.return_value = error_response_mock

        with self.assertLogs(level='ERROR') as log:
            with self.assertRaises(AuthenticationFailedException):
                client = Client('invalid_api_key')
            self.assertIn('HTTP error occurred:', log.output[0])

    # HTTP Error 500
    @patch('jellyfaas.requests.get')
    def test_auth_internal_server_error(self, mock_get):
        error_response_mock = MagicMock()
        type(error_response_mock).status_code = PropertyMock(return_value=500)
        error_response_mock.raise_for_status.side_effect = requests.exceptions.HTTPError(response=error_response_mock)
        
        mock_get.return_value = error_response_mock

        with self.assertLogs(level='ERROR') as log:
            with self.assertRaises(AuthenticationFailedException):
                client = Client('invalid_api_key')
            self.assertIn('HTTP error occurred:', log.output[0])

    # Request non-HTTP error
    @patch('jellyfaas.requests.get')
    def test_request_error(self, mock_get):
        error_response_mock = MagicMock()
        error_response_mock.raise_for_status.side_effect = requests.exceptions.ConnectionError()

        mock_get.return_value = error_response_mock

        with self.assertLogs(level='ERROR') as log:
            with self.assertRaises(AuthenticationFailedException):
                client = Client('invalid_api_key')
            self.assertIn('Other error occurred:', log.output[0])


if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    unittest.TextTestRunner().run(unittest.makeSuite(TestClientInit))
    cov.stop()
    cov.save()
    cov.html_report(directory="coverage_html_report")
    print("Done.")
