import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
import sys
import os
import requests
import coverage

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/jellyfaas')))

from jellyfaas import *

class TestClientSetRequest(unittest.TestCase):

    def setUp(self):
        # Mock the constructor to avoid making real API calls
        patch('jellyfaas.Client.__init__', lambda x, api_key: None).start()
        self.client = Client('test_api_key')
        self.client._api_key = 'test_api_key'
        self.client._token = 'test_token'
        self.client._token_expiry = 'test_expiry'
        self.client._requirements = {
            'inputSchema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'required': True},
                    'age': {'type': 'integer'},
                    'tags': {'type': 'array', 'items': {'type': 'string'}}
                }
            }
        }

    # Success with dictionary
    def test_set_request_with_dict(self):
        request_body = {
            'name': 'John Doe',
            'age': 30,
            'tags': ['developer', 'python']
        }
        result = self.client.set_request(query_params={'param': 'value'}, request_body_instance=request_body)
        self.assertEqual(self.client._params, {'param': 'value'})
        self.assertEqual(self.client._body, request_body)

    # Success with class instance
    def test_set_request_with_class_instance(self):
        class RequestBody:
            def __init__(self):
                self.name = 'Jane Doe'
                self.age = 25
                self.tags = ['designer', 'javascript']

        request_body_instance = RequestBody()
        result = self.client.set_request(query_params={'param': 'value'}, request_body_instance=request_body_instance)
        self.assertEqual(self.client._params, {'param': 'value'})
        self.assertEqual(self.client._body, {
            'name': 'Jane Doe',
            'age': 25,
            'tags': ['designer', 'javascript']
        })

    # Failure when request_body_instance is None
    def test_set_request_with_none(self):
        with self.assertRaises(SetRequestException) as context:
            self.client.set_request(query_params={'param': 'value'}, request_body_instance=None)
        self.assertEqual(str(context.exception), "Error: request_body_instance is required")

    # Success when request_body_instance is None but so is requirements inputSchema
    def test_set_request_with_none(self):
        old_req = self.client._requirements # save for future tests
        self.client._requirements = {}
        self.client.set_request(query_params={'param': 'value'}, request_body_instance=None)
        self.assertEqual(self.client._params, {'param': 'value'})
        self.assertEqual(self.client._body, {})
        self.client._requirements = old_req
        

    # Failure when request_body_instance is not a dict or class instance
    def test_set_request_with_invalid_type(self):
        with self.assertRaises(SetRequestException) as context:
            self.client.set_request(query_params={'param': 'value'}, request_body_instance=object())
        self.assertEqual(str(context.exception), "Error: The provided request_body_instance is neither a dictionary nor a class instance.")

    # Failure when validation fails
    def test_set_request_with_invalid_data(self):
        request_body = {
            'name': 'John Doe',
            # Missing 'age' field, which is required
        }
        with self.assertRaises(SetRequestException) as context:
            self.client.set_request(query_params={'param': 'value'}, request_body_instance=request_body)
        self.assertTrue("Validation error" in str(context.exception))

if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    unittest.TextTestRunner().run(unittest.makeSuite(TestClientSetRequest))
    cov.stop()
    cov.save()
    cov.html_report(directory="coverage_html_report")
    print("Coverage report generated.")
