from abstract_database import *
from abstract_apis import *
from .utils import *
def get_rate_limit_url(method_name, *args, **kwargs):
    endpoint = make_endpoint("/rate_limit")
    for arg in args:
        if "method" not in kwargs:
            kwargs["method"] = arg
    return getRequest(getRateLimitUrl(), kwargs, endpoint=endpoint)

def log_response(method_name, response_data,*args,**kwargs):
    endpoint = make_endpoint("/log_response")
    payload = {
        "method": kwargs.get("method", method_name),
        "response_data": kwargs.get("response_data", response_data)
    }
    payload.update(kwargs) 
    for arg in args:
        if "method" not in payload:
            payload["method"] = arg
        if "response_data" not in payload:
            payload["response_data"] = arg
    return getRequest(getRateLimitUrl(), payload, endpoint=endpoint)
