import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
import sys
import os
import requests
import coverage

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/jellyfaas')))

from jellyfaas import *

class TestClientLookup(unittest.TestCase):

    def setUp(self):
        # Mock the constructor to avoid making real API calls
        patch('jellyfaas.Client.__init__', lambda x, api_key: None).start()
        self.client = Client('test_api_key')
        self.client._api_key = 'test_api_key'
        self.client._token = 'test_token'  # Set the token directly for tests
        self.client._token_expiry = 'test_expiry'

    # Success
    @patch('jellyfaas.requests.get')
    def test_lookup_success(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'dns': 'http://example.com/function',
            'requirements': {'required_key': 'required_value'}
        }
        mock_get.return_value = mock_response

        result = self.client.lookup_function('test_query')
        self.assertIsNotNone(result)
        self.assertEqual(result._url_endpoint, 'http://example.com/function')
        self.assertEqual(result._requirements, {'required_key': 'required_value'})

        # Verify the request was made with the correct URL, headers, and parameters
        expected_url = 'https://api.jellyfaas.com/auth-service/v1/lookup'
        expected_headers = {'x-p48-apikey': 'test_api_key'}
        expected_params = {'id': 'test_query', 'version': '1', 'size': 's'}
        mock_get.assert_called_once_with(expected_url, headers=expected_headers, params=expected_params)

    # API key not set
    def test_lookup_no_api_key(self):
        self.client._api_key = None
        with self.assertRaises(FunctionLookupException) as context:
            self.client.lookup_function('test_query')
        self.assertEqual(str(context.exception), "API key/token is required")

    # HTTP Error 401
    @patch('jellyfaas.requests.get')
    def test_lookup_http_error_401(self, mock_get):
        error_response_mock = MagicMock()
        error_response_mock.raise_for_status.side_effect = requests.exceptions.HTTPError(response=error_response_mock)
        type(error_response_mock).status_code = 401
        mock_get.return_value = error_response_mock

        with self.assertRaises(FunctionLookupException) as context:
            self.client.lookup_function('test_query')
        self.assertIn("HTTP error occurred", str(context.exception))

    # HTTP Error 500
    @patch('jellyfaas.requests.get')
    def test_lookup_http_error_500(self, mock_get):
        error_response_mock = MagicMock()
        error_response_mock.raise_for_status.side_effect = requests.exceptions.HTTPError(response=error_response_mock)
        type(error_response_mock).status_code = 500
        mock_get.return_value = error_response_mock

        with self.assertRaises(FunctionLookupException) as context:
            self.client.lookup_function('test_query')
        self.assertIn("HTTP error occurred", str(context.exception))

    # Other exceptions
    @patch('jellyfaas.requests.get')
    def test_lookup_other_exception(self, mock_get):
        mock_get.side_effect = Exception('Test Exception')

        with self.assertRaises(FunctionLookupException) as context:
            self.client.lookup_function('test_query')
        self.assertIn("Other error occurred", str(context.exception))
        
if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    unittest.TextTestRunner().run(unittest.makeSuite(TestClientLookup))
    cov.stop()
    cov.save()
    cov.html_report(directory="coverage_html_report")
    print("Coverage report generated.")
