import os
from typing import Optional, Any
import json
import threading
from functools import wraps

from .rpc.rpc import call_rpc
from .utils import create_data


def call(url: str, workspace_api_key: Optional[str] = None, data: Optional[dict] = None, callback: Optional[Any] = None,
         inputs: Optional[dict] = None, is_batch: Optional[bool] = False):
    """
    Call Inferless API
    :param url: Inferless Model API URL
    :param workspace_api_key: Inferless Workspace API Key
    :param data: Model Input Data as a dictionary, example: {"question": "What is the capital of France?", "context": "Paris is the capital of France."}
    :param callback: Callback function to be called after the response is received
    :param inputs: Model Input Data in inferless format
    :param is_batch: Whether the input is a batch of inputs, default is False
    :return: Response from the API call
    """
    try:
        if inputs is not None and data is not None:
            raise Exception("Cannot provide both data and inputs")

        if data is not None:
            inputs = create_data(data, is_batch)

        import requests
        if workspace_api_key is None:
            workspace_api_key = os.environ.get("INFERLESS_API_KEY")
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {workspace_api_key}"}
        if inputs is None:
            inputs = {}
        response = requests.post(url, data=json.dumps(inputs), headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to call {url} with status code {response.status_code} and response {response.text}")
        if callback is not None:
            callback(None, response.json())
        return response.json()
    except Exception as e:
        if callback is not None:
            callback(e, None)
        else:
            raise e


def call_async(url: str, workspace_api_key: Optional[str] = None, data: Optional[dict] = None,
               callback: Any = None, inputs: Optional[dict] = None, is_batch: Optional[bool] = False):
    """
    Call Inferless API
    :param url: Inferless Model API URL
    :param workspace_api_key: Inferless Workspace API Key
    :param data: Model Input Data as a dictionary, example: {"question": "What is the capital of France?", "context": "Paris is the capital of France."}
    :param callback: Callback function to be called after the response is received
    :param inputs: Model Input Data in inferless format
    :param is_batch: Whether the input is a batch of inputs, default is False
    :return: Response from the API call
    """
    thread = threading.Thread(target=call, args=(url, workspace_api_key, data, callback, inputs, is_batch))
    thread.start()
    return thread


def method(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import sys
        if sys.argv[1].endswith("yaml"):
            config_path = sys.argv[1]
        else:
            raise Exception("Please provide the path to the configuration file")

        return call_rpc(func, config_path, *args, **kwargs)

    return wrapper


# my_lib.py

def cls(user_class):
    class InferlessRpcClass(user_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Collect methods with @load and @infer decorators
            for name, func in user_class.__dict__.items():
                if hasattr(func, '_is_load'):
                    setattr(self, name, self.wrap_load(func))
                elif hasattr(func, '_is_infer'):
                    setattr(self, name, self.wrap_infer(func))

            import sys
            if sys.argv[1].endswith("yaml"):
                self.config_path = sys.argv[1]
            else:
                raise Exception("Please provide the path to the configuration file")

        def wrap_load(self, func):
            def wrapper(*args, **kwargs):
                # Slight modification: Just printing method call
                # print(f"Calling modified load method: {func.__name__}")
                return func(*args, **kwargs)

            return wrapper

        def wrap_infer(self, func):
            def wrapper(*args, **kwargs):
                # Slight modification: Just printing method call
                # print(f"Calling modified infer method: {func.__name__}")
                def rpc_func():
                    self.wrap_load(func)()

                    return func(*args, **kwargs)
                return call_rpc(rpc_func, self.config_path, *args, **kwargs)
            return wrapper

    return InferlessRpcClass


def load(func):
    func._is_load = True
    return func


def infer(func):
    func._is_infer = True
    return func
