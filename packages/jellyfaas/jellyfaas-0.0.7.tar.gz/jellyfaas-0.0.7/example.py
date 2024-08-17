import os, json
from jellyfaas import *
import logging
from typing import Any, Dict, Type, List


# To see debug logs from the SDK
logging.basicConfig(level=logging.DEBUG)

# Define request class
class IbanRequest():
    ibans:       List[str]  = None

# Define response class
class Data:
    valid:        List[str] = None
    invalid:      List[str] = None
    validCount:   int       = None
    invalidCount: int       = None
    total:        int       = None

class IbanResponse:
    data:         Data      = Data()
    spanId:       str       = None

# Retrieve the API key from environment variable
api_key = os.getenv("JELLYFAAS_API_KEY")

if api_key is None:
    raise ValueError("API key is not set in environment variables")

# Input body as class
body = IbanRequest()
body.ibans = [
            "PT50000201231234567890154",
            "GR1601101250000000012300695",
            "invalidIbanTest"
        ]

# Create a JellyFAAS client and try to invoke a function
try:
    client = Client(api_key)
    response: IbanResponse
    
    client._version = "4" # NOTE: This will be replaced with a proper "set_version" function.
                          # It is currently being used for testing, as older versions of "ibanvalidation" are outdated.

    client, response = client \
        .lookup_function("ibanvalidation") \
        .set_request({}, body) \
        .set_response(IbanResponse) \
        .invoke()
    
    print(response)              # <__main__.IbanResponse object at ...>
    print(response.data.valid)   # ['PT50000201231234567890154', 'GR1601101250000000012300695']
    print(response.data.invalid) # ['invalidIbanTest']


except JellyFaasException as e:
    print(e)
