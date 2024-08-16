# JellyFAAS Python SDK

This Python module provides a client for interacting with the JellyFAAS API. The client supports authentication, function lookup, setting request parameters, invoking functions, and handling responses with optional response class transformation.

### Requirements

- Python 3.12+ (Note: Need to test earlier versions?)
- `requests` library

### Installation

Ensure you have the `requests` library installed. If not, you can install it using pip:

```sh
pip install requests
```

### Environment Setup

It is recommended to set your API key as an environment variable.

### `Client` Class

#### Initialization

Create an instance of the `Client` class with your API key:

- **Parameters**:
    - `api_key (str)`: Your JellyFAAS API key.
- **Returns**:
    - The client instance.

```python
client = Client(api_key)
```

#### Methods

##### `lookup_function(function_id)`

Look up a function by its ID (shortname).

- **Parameters**:
    - `function_id (str)`: The ID (shortname) of the function to look up.
- **Returns**:
    - The client instance.

Example:

```python
client = Client("API_KEY").lookup_function("FUNCTION_ID")
```

##### `set_request(query_params={}, request_body_instance=None)`

Set the request parameters and body.

- **Parameters**:
    - `query_params (dict)`: Query parameters for the request.
    - `request_body_instance (dict or object)`: JSON body for the request. Can be a dictionary or an instance of a class with attributes.
- **Returns**:
    - The client instance.

Example:

```python
client = Client("API_KEY").lookup_function("FUNCTION_ID").set_request(query_params={"param1": "value1"}, request_body_instance={"key": "value"})
```

##### `invoke()`

Invoke the function with the set parameters and body.

- **Returns**: 
    - A tuple of the client instance and the response JSON if successful, otherwise a tuple of the client instance and `None`.

Example:

```python
p48client, result = client.invoke()
```

##### `set_response(type)`

Set the response type for automatic transformation of the response JSON into an instance of a specified class.

- **Parameters**:
    - `type (class)`: The class type to transform the response JSON into.
- **Returns**:
    - The client instance.

Example:

```python
client.set_response(MyResponseClass)
```

### Debugging

The client uses Python's built-in logging module to provide debug and error logs. Ensure you configure the logging level appropriately in your application.

### Complete Example Usage:

```python
import os
import jellyfaas

# Retrieve the API key from environment variable
api_key = os.getenv("JELLYFAAS_API_KEY")

if api_key is None:
    raise ValueError("API key is not set in environment variables")

# Define a response class (optional)
class MyResponse:
    def __init__(self):
        self.key = None
        self.value = None

# Create a JellyFAAS client and invoke a function
p48client, result = (
    jellyfaas.Client(api_key)
    .lookup_function("joesjokes")
    .set_request(query_params={"param1": "value1"}, request_body_instance={"key": "value"})
    .set_response(MyResponse)
    .invoke()
)

print(result)
```

### Handling Exceptions

The SDK raises custom exceptions for various error conditions:

- `AuthenticationFailedException`: Raised when authentication fails.
- `FunctionLookupException`: Raised when function lookup fails.
- `SetRequestException`: Raised when setting the request parameters or body fails.
- `InvocationException`: Raised when invocation of the function fails.

These all inherit from a base `JellyFaasException` type which you can optionally use instead, to catch all exceptions from the SDK.

You can handle these exceptions as needed in your application.

Example:

```python
import jellyfaas
import os

api_key = os.getenv("JELLYFAAS_API_KEY")

try:
    p48client, result = (
        jellyfaas.Client(api_key)
        .lookup_function("joesjokes")
        .set_request(query_params={"param1": "value1"}, request_body_instance={"key": "value"})
        .invoke()
    )
    print(result)
except jellyfaas.AuthenticationFailedException as e:
    print(f"Authentication failed: {e}")
except jellyfaas.FunctionLookupException as e:
    print(f"Function lookup failed: {e}")
except jellyfaas.SetRequestException as e:
    print(f"Setting request failed: {e}")
except jellyfaas.InvocationException as e:
    print(f"Function invocation failed: {e}")
```

### Additional Information

The client supports validation of request bodies against input schemas if provided in the function requirements. It also includes debug logging to help trace the internal state and steps of computation, aiding in debugging and development.

Ensure you have configured logging in your application to capture debug logs:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```
