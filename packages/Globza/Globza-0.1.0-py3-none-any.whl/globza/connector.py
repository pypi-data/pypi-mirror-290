# connector.py

import requests
import uuid


class API:
    """
    API class to interact with the cloud service for function registration and invocation.
    """
    def __init__(self, base_url='https://apiwwf-production.up.railway.app'):
        """
        Initialize with the base URL of the cloud service.
        """
        self.base_url = base_url

    def __getattr__(self, function_name):
        """
        Dynamically create a method corresponding to the called function name.
        """
        def method(*args, **kwargs):
            request_id = uuid.uuid4().hex  # Генерация уникального UUID для каждого запроса
            url = f"{self.base_url}/{function_name}"
            payload = {'request_id': request_id, 'args': args, 'kwargs': kwargs}
            try:
                response = requests.post(url, json=payload)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                return {'error': 'HTTP error', 'message': str(e)}
            except requests.exceptions.RequestException as e:
                return {'error': 'Request error', 'message': str(e)}
            except ValueError as e:
                return {'error': 'Decode error', 'message': str(e)}
        return method

    def to_register_function(self, id, function_url, metadata=None):
        """
        Register a function with the cloud service.
        """
        url = f"{self.base_url}/register_function"
        payload = {'id': id, 'function_url': function_url, 'metadata': metadata or {}}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def to_call_function(self, id, *args, **kwargs):
        """
        Call a registered function by its identifier with provided arguments.
        """
        return self.__getattr__(id)(*args, **kwargs)


api = API()
