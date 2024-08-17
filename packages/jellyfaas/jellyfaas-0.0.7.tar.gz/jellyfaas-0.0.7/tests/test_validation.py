import unittest
from unittest.mock import patch
import json
import os
import sys
import coverage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Add the src directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/jellyfaas')))

from jellyfaas import *

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def get_test_cases():
    test_data = load_json('tests/schema.json')
    test_cases = []

    for test in test_data['tests']:
        schema = test['schema']

        for i, case in enumerate(test['cases']):
            test_cases.append((
                test["name"],
                i,
                schema,
                case['input'],
                case['expected_result']
            ))

    return test_cases

class TestClientValidate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_cases = get_test_cases()
        logging.info("Loaded test cases from schema.")

    def setUp(self):
        # Mock the constructor to avoid making real API calls
        patch('jellyfaas.Client.__init__', lambda x, api_key: None).start()
        self.client = Client('test_api_key')
        self.client._api_key = 'test_api_key'
        self.client._token = 'test_token'
        self.client._token_expiry = 'test_expiry'
    
    def test_json_schema_validation(self):
        for name, case_index, schema, input_data, expected_result in self.test_cases:
            logging.info(f"\nTest: {name} - Case: {case_index}\n")
            logging.info(f"Input schema: {json.dumps(schema['requirements'].get('inputSchema', {}), indent=2)}")
            logging.info(f"Input data: {json.dumps(input_data, indent=2)}")
            logging.info(f"Expected result: {expected_result}")

            self.client._requirements = {"inputSchema": schema.get("requirements", {}).get("inputSchema", {})}

            try:
                input_schema = self.client._requirements.get("inputSchema", {})
                valid, message = self.client._Client__validate(schema=input_schema, data=input_data)
                
                if not valid:
                    logging.error(f"Validation failed for input: {json.dumps(input_data, indent=2)}")
                    logging.error(f"Validation message: {message}")
                    if expected_result == 'invalid':
                        logging.info("Test case passed as expected failure occurred.")
                    else:
                        logging.error("Test case failed. Expected success but validation failed.")
                        self.fail(f"Expected success but validation failed. Message: {message}")
                else:
                    if expected_result == 'valid':
                        logging.info("Test case passed as expected.")
                    else:
                        logging.error("Test case failed. Expected failure but validation succeeded.")
                        self.fail("Expected failure but validation succeeded.")
                    
            except Exception as e:
                logging.error("Exception occurred during validation")
                logging.exception(e)
                if expected_result == "invalid":
                    logging.info("Test case passed as expected failure occurred due to exception.")
                else:
                    logging.error("Test case failed. Expected success but exception occurred.")
                    self.fail(f"Expected success but exception occurred: {str(e)}")

if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()
    unittest.TextTestRunner().run(unittest.makeSuite(TestClientValidate))
    cov.stop()
    cov.save()
    cov.html_report(directory="coverage_html_report")
    print("Coverage report generated.")
