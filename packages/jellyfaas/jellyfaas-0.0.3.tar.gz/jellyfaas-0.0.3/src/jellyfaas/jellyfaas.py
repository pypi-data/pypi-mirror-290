import requests
import logging
from typing import Any, Dict, Type

logger = logging.getLogger(__name__)

class Client:
    """
    A client for interacting with the JellyFAAS API. It is not recommended to access attributes of this class directly; instead, use "public" class functions as per the documentation.

    Attributes:
        _api_key (str): The API key used for authentication.
        _token (str): The authentication token.
        _token_expiry (str): The expiration time for the token.
        _version (str): The version of the function to lookup.
        _size (str): The size of the function to lookup.
        _response (Any): The response from the invoked function.
        _response_type (Any): The type of the response for transformation.
    """

    # Member "consts"
    AUTH_ENDPOINT:   str = "https://api.jellyfaas.com/auth-service/v1"
    LOOKUP_ENDPOINT: str = "https://api.jellyfaas.com/auth-service/v1/lookup"
    P48_HEADER:      str = "x-p48-apikey"

    # Member variables
    _api_key: str = None
    _token: str = None
    _token_expiry: str = None
    _version: str = "1"
    _size: str = "s"
    _response = None
    _response_type = None
    _do_debug = False

    def __init__(self, api_key: str) -> None:      
        """
        Initializes and authenticates the Client with the provided API key.

        Args:
            api_key (str): The API key for JellyFAAS.

        Raises:
            AuthenticationFailedException: If authentication fails.
        """
        self.__auth(api_key)  # Fetch authorization token

    def __auth(self, api_key=None):
        """
        Authenticate the client with the JellyFAAS API using the provided API key.

        Args:
            api_key (str): The API key for JellyFAAS.

        Raises:
            AuthenticationFailedException: If authentication fails.
        """
        try:
            self.debug(f"Starting __auth method with api_key={api_key}")
            
            self.debug("Setting auth token")
            auth_response = requests.get(self.AUTH_ENDPOINT + "/validate", headers={self.P48_HEADER: api_key})
            
            self.debug(f"Received response: {auth_response.status_code}")
            auth_response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
            
            response_json = auth_response.json()  # Dumping the response as a JSON string
            self.debug(f"Response JSON: {response_json}")

            self._api_key = api_key
            self._token = response_json["token"]
            self._token_expiry = response_json["expiry"]

            self.debug("Successfully set auth token")

        except requests.exceptions.HTTPError as http_err:
            if auth_response.status_code == 401:
                error_message = "401 Client Error: Invalid API key"
                logger.error(error_message)
                raise AuthenticationFailedException(error_message)
            else:
                error_message = f"HTTP error occurred: {http_err}"
                logger.error(error_message)
                raise AuthenticationFailedException(error_message)
        except Exception as err:
            error_message = f"Other error occurred: {err}"
            logger.error(error_message)
            raise AuthenticationFailedException(error_message)
        finally:
            self.debug("Finished __auth method")

    def lookup_function(self, function_id: str) -> 'Client':
        """
        Lookup a function by its ID.

        Args:
            function_id (str): The ID of the function to look up.

        Returns:
            Client: The current client instance.

        Raises:
            FunctionLookupException: If the function lookup fails.
        """
        self.debug(f"Starting lookup_function method with function_id={function_id}")

        if self._api_key is None:
            error_message = "API key/token is required"
            logger.error(error_message)
            raise FunctionLookupException(error_message)

        query_params = {
            "id": function_id,
            "version": self._version,
            "size": self._size
        }

        try:
            lookup_response = requests.get(
                self.LOOKUP_ENDPOINT,
                headers={self.P48_HEADER: self._api_key},
                params=query_params
            )
            
            self.debug(f"Received response: {lookup_response.status_code}")
            lookup_response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
            dns_response = lookup_response.json()  # Parse the response as a JSON string
            self.debug(f"Response JSON: {dns_response}")

            self._lookup_request = function_id
            self._url_endpoint = dns_response.get("dns")
            self._requirements = dns_response.get("requirements")

            if not self._requirements:
                error_message = "Error: No requirements found"
                logger.error(error_message)
                raise FunctionLookupException(error_message)

            self.debug("Successfully looked up function")
            return self

        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
            logger.error(error_message)
            raise FunctionLookupException(error_message)
        except Exception as err:
            error_message = f"Other error occurred: {err}"
            logger.error(error_message)
            raise FunctionLookupException(f"Other error occurred: {err}")

    def set_request(self, query_params={}, request_body_instance=None):
        """
        Set the request parameters and body for invoking a function.

        Args:
            query_params (dict): Query parameters for the request.
            request_body_instance (dict or Any): JSON body for the request.

        Returns:
            Client: The current client instance.

        Raises:
            SetRequestException: If setting the request parameters or body fails.
        """
        self.debug(f"Starting set_request method with query_params={query_params}, request_body_instance={request_body_instance}")
        
        if request_body_instance is None:
            if self._requirements.get("inputSchema", None) != None:
                error_message = "Error: request_body_instance is required"
                logger.error(error_message)
                raise SetRequestException(error_message)   
        elif isinstance(request_body_instance, dict):
            request_body_dict = request_body_instance
        elif hasattr(request_body_instance, '__dict__'):
            try:
                request_body_dict = request_body_instance.__dict__
            except AttributeError:
                error_message = "Error: The provided request_body_instance does not have a __dict__ attribute"
                logger.error(error_message)
                raise SetRequestException(error_message)
        else:
            error_message = "Error: The provided request_body_instance is neither a dictionary nor a class instance."
            logger.error(error_message)
            raise SetRequestException(error_message)
        
        input_schema = self._requirements.get("inputSchema", None)
        if input_schema:
            try:
                valid, message = self.__validate(schema=input_schema, data=request_body_dict)
                if not valid:
                    error_message = f"Validation error: {message}"
                    logger.error(error_message)
                    raise ValueError(error_message)
                self.debug("Request body validation successful")
            except ValueError as e:
                error_message = f"Validation error: {e}"
                logger.error(error_message)
                raise SetRequestException(e)
        
        self._params = query_params
        self._body = request_body_dict if (not request_body_instance is None) else {}

        self.debug("Successfully set request")
        return self

    def invoke(self):
        """
        Invoke the function with the set parameters and body.

        Returns:
            tuple: A tuple of the client instance and the response JSON if successful, otherwise raises an exception.

        Raises:
            InvocationException: If invoking the function fails.
        """
        self.debug("Starting invoke method")

        if not self._url_endpoint or not self._token or not self._requirements:
            error_message = "Error: Endpoint, token, and request requirements must be set"
            logger.error(error_message)
            raise InvocationException(error_message)

        try:
            request_type = self._requirements["requestType"]

            headers = {"p48wt": self._token}
            data = self._body if request_type == 'POST' else None
            self.debug(f"Invoking with headers={headers}, data={data}, params={self._params}")
            if request_type == 'GET':
                invoke_response = requests.get(self._url_endpoint, headers=headers, params=self._params)
            elif request_type == 'POST':
                invoke_response = requests.post(self._url_endpoint, headers=headers, params=self._params, json=data)
            else:
                error_message = f"Unsupported request type: {request_type}"
                logger.error(error_message)
                raise InvocationException(error_message)

            self.debug(f"Received response: {invoke_response.status_code}")
            invoke_response.raise_for_status()  # This will raise an error for 4xx/5xx status codes

            response_json = invoke_response.json()  # Parse the response as a JSON string
            self.debug(f"Response JSON: {response_json}")
            self._response = response_json
            
            if self._response_type is not None:
                try:
                    self._response = self.__dict_to_class(self._response_type, self._response)
                except Exception as e:
                    error_message = f"Error converting response to class: {e}"
                    logger.error(error_message)
                    raise InvocationException(error_message)

            self.debug("Successfully invoked function")
            return self, self._response

        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
            logger.error(error_message)
            raise InvocationException(error_message)
        except Exception as err:
            error_message = f"Other error occurred: {err}"
            logger.error(error_message)
            raise InvocationException(error_message)

    def debug(self, msg):
        """
        Log a debug message.

        Args:
            msg (str): The message to log.
        """
        if self._do_debug: logger.debug(msg)

    def set_debug_mode(self, do_debug: bool):
        if do_debug == True or do_debug == False:
            self._do_debug = do_debug
            return self
        else:
            raise JellyFaasException("Invalid `set_debug_mode` parameter. Must be True|False")

    def __validate(self, schema, data):
        """
        Validate the given data against the provided schema.

        Args:
            schema (dict): The schema to validate against.
            data (dict): The data to validate.

        Returns:
            tuple: A tuple containing a boolean indicating success and a message.

        Raises:
            ValueError: If validation fails.
        """
        def __validate_property(prop_schema, value, path):
            if prop_schema.get('required', False) and value is None:
                return False, f"Property '{path}' is required but missing or null."

            expected_type = prop_schema.get('type')
            if expected_type:
                if expected_type == 'string' and not isinstance(value, str):
                    return False, f"Property '{path}' should be of type '{expected_type}'."
                elif expected_type == 'integer' and not isinstance(value, int):
                    return False, f"Property '{path}' should be of type '{expected_type}'."
                elif expected_type == 'array' and not isinstance(value, list):
                    return False, f"Property '{path}' should be of type '{expected_type}'."
            return True, None

        def __validate_array(array_schema, data, path):
            if not isinstance(data, list):
                return False, f"Data at '{path}' should be an array."
            
            item_schema = array_schema.get('items', {})
            for index, item in enumerate(data):
                valid, message = __validate_property(item_schema, item, f"{path}[{index}]")
                if not valid:
                    return valid, message
                if item_schema.get('type') == 'object' and isinstance(item, dict):
                    valid, message = __validate_schema(item_schema, item, f"{path}[{index}]")
                    if not valid:
                        return valid, message
                elif item_schema.get('type') == 'array':
                    valid, message = __validate_array(item_schema, item, f"{path}[{index}]")
                    if not valid:
                        return valid, message
            return True, None

        def __validate_schema(schema, data, path=''):
            if schema == None:
                return True, None

            if 'type' not in schema:
                return False, "Schema is missing 'type' key"
            
            if schema['type'] == 'object':
                if not isinstance(data, dict):
                    return False, f"Data at '{path}' should be an object."

                properties = schema.get('properties', {})
                for prop, prop_schema in properties.items():
                    value = data.get(prop)
                    valid, message = __validate_property(prop_schema, value, path + '.' + prop)
                    if not valid:
                        return valid, message
                    if prop_schema.get('type') == 'object' and isinstance(value, dict):
                        valid, message = __validate_schema(prop_schema, value, path + '.' + prop)
                        if not valid:
                            return valid, message
                    elif prop_schema.get('type') == 'array':
                        valid, message = __validate_array(prop_schema, value, path + '.' + prop)
                        if not valid:
                            return valid, message

                required_properties = [prop for prop, prop_schema in properties.items() if prop_schema.get('required', False)]
                missing_properties = [prop for prop in required_properties if prop not in data]
                if missing_properties:
                    return False, f"Missing required properties: {', '.join(missing_properties)}."

            elif schema['type'] == 'array':
                valid, message = __validate_array(schema, data, path)
                if not valid:
                    return valid, message

            return True, None
        
        return __validate_schema(schema, data)

    def set_response(self, type: Any) -> 'Client':
        """
        Set the response type for transforming the response JSON.

        Args:
            type (Any): The class type to transform the response into.

        Returns:
            Client: The current client instance.
        """
        self.debug(f"Starting set_response method with type={type}")
        self._response_type = type
        self.debug("Successfully set response type")
        return self

    def __dict_to_class(self, cls: Type, data: Dict[str, Any]) -> Any:
        """
        Convert a dictionary to an instance of the given class.

        Args:
            cls (Type): The class to instantiate.
            data (Dict[str, Any]): The dictionary to convert.

        Returns:
            Any: An instance of the specified class.

        Raises:
            InvocationException: If converting the dictionary to a class instance fails.
        """
        self.debug(f"Starting __dict_to_class method with cls={cls}, data={data}")
        
        if not hasattr(cls, '__init__'):
            error_message = f"The provided class '{cls.__name__}' does not have an __init__ method."
            logger.error(error_message)
            raise InvocationException(error_message)

        instance = cls()

        if not hasattr(instance, '__dict__'):
            error_message = f"Error: The class '{cls.__name__}' does not have instance attributes."
            logger.error(error_message)
            raise InvocationException(error_message)
        
        for key, value in data.items():
            if hasattr(instance, key):
                attr = getattr(instance, key)
                if isinstance(value, dict):
                    if hasattr(attr, '__dict__'):
                        setattr(instance, key, self.__dict_to_class(type(attr), value))
                    else:
                        setattr(instance, key, value)
                elif isinstance(value, list):
                    if hasattr(attr, '__dict__'):
                        item_class = type(attr)
                        setattr(instance, key, [self.__dict_to_class(item_class, item_data) for item_data in value])
                    else:
                        setattr(instance, key, value)
                else:
                    setattr(instance, key, value)
            else:
                self.debug(f"Warning: The attribute '{key}' is not present in the class '{cls.__name__}'.")

        self.debug(f"Successfully created instance of {cls.__name__} from dict")
        return instance

class JellyFaasException(Exception):
    """
    Base class for exceptions in the JellyFaas library.
    """
    pass

class AuthenticationFailedException(JellyFaasException):
    """
    Raised when authentication fails.
    """
    pass

class FunctionLookupException(JellyFaasException):
    """
    Raised when there is an issue looking up a function.
    """
    pass

class SetRequestException(JellyFaasException):
    """
    Raised when there is an issue setting request parameters for a function.
    """
    pass

class InvocationException(JellyFaasException):
    """
    Raised when there is an issue invoking the function.
    """
    pass
