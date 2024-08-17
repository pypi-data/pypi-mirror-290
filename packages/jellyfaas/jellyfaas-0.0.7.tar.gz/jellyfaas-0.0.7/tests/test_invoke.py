import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
import sys
import os
import requests
from requests.models import Response
import coverage

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/jellyfaas')))

from jellyfaas import *

class MockResponse:
    def __init__(self):
        self.key = None
        self.value = None

class TestClientInvoke(unittest.TestCase):

    def setUp(self):
        # Mock the constructor to avoid making real API calls
        patch('jellyfaas.Client.__init__', lambda x, api_key: None).start()
        self.client = Client('test_api_key')
        self.client._api_key = 'test_api_key'
        self.client._token = 'test_token'
        self.client._token_expiry = 'test_expiry'
        self.client._url_endpoint = 'https://api.jellyfaas.com/invoke'
        self.client._requirements = {
            'requestType': 'GET'
        }
        self.client._params = {}
        self.client._body = {}
        self.client._response_type = None  # Assuming no response type transformation needed for this test

    @patch('requests.get')
    def test_invoke_get_success(self, mock_get):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 'success'}
        mock_get.return_value = mock_response
        
        result, response = self.client.invoke()
        self.assertEqual(response, {'result': 'success'})
        self.assertEqual(self.client._response, {'result': 'success'})

    @patch('requests.post')
    def test_invoke_post_success(self, mock_post):
        self.client._requirements['requestType'] = 'POST'
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 'success'}
        mock_post.return_value = mock_response

        result, response = self.client.invoke()
        self.assertEqual(response, {'result': 'success'})
        self.assertEqual(self.client._response, {'result': 'success'})

    @patch('requests.get')
    def test_invoke_get_http_error(self, mock_get):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError('404 Not Found')

        with self.assertRaises(InvocationException) as context:
            self.client.invoke()
        self.assertIn("HTTP error occurred", str(context.exception))

    @patch('requests.post')
    def test_invoke_post_http_error(self, mock_post):
        self.client._requirements['requestType'] = 'POST'
        mock_response = Mock(spec=Response)
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError('500 Internal Server Error')

        with self.assertRaises(InvocationException) as context:
            self.client.invoke()
        self.assertIn("HTTP error occurred", str(context.exception))

    def test_invoke_missing_requirements(self):
        self.client._url_endpoint = None  # Clear URL endpoint
        self.client._requirements = None  # Clear requirements

        with self.assertRaises(InvocationException) as context:
            self.client.invoke()
        self.assertIn("Error: Endpoint, token, and request requirements must be set", str(context.exception))

    def test_invoke_missing_token(self):
        self.client._token = None  # Clear token

        with self.assertRaises(InvocationException) as context:
            self.client.invoke()
        self.assertIn("Error: Endpoint, token, and request requirements must be set", str(context.exception))

    def test_invoke_missing_endpoint(self):
        self.client._url_endpoint = None  # Clear URL endpoint

        with self.assertRaises(InvocationException) as context:
            self.client.invoke()
        self.assertIn("Error: Endpoint, token, and request requirements must be set", str(context.exception))
    def test_invoke_missing_endpoint(self):
        self.client._url_endpoint = None  # Clear URL endpoint

        with self.assertRaises(InvocationException) as context:
            self.client.invoke()
        self.assertIn("Error: Endpoint, token, and request requirements must be set", str(context.exception))

    @patch('requests.get')
    def test_invoke_response_dict_to_class(self, mock_get):
        # Set the response type to a mock response class
        self.client._response_type = MockResponse

        # Mock the requests.get method to return a predefined JSON response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'test_key', 'value': 'test_value'}
        mock_get.return_value = mock_response
        
        result, response = self.client.invoke()

        # Assert that the response is an instance of MockResponse and values are set correctly
        self.assertIsInstance(self.client._response, MockResponse)
        self.assertEqual(self.client._response.key, 'test_key')
        self.assertEqual(self.client._response.value, 'test_value')

if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    unittest.TextTestRunner().run(unittest.makeSuite(TestClientInvoke))
    cov.stop()
    cov.save()
    cov.html_report(directory="coverage_html_report")
    print("Coverage report generated.")
