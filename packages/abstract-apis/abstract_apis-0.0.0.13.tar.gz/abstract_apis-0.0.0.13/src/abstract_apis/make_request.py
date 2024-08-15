import json
import requests
import aiohttp
from abstract_utilities import *
from .request_utils import *
def make_request(url, data=None, headers=None, method='GET', endpoint=None, status_code=False, raw_response=False, response_result=None, load_nested_json=True):
    url = get_url(url, endpoint=endpoint)
    if headers is None:
        headers = get_headers()
    data = ensure_json(data)

    try:
        if method.upper() == 'POST':
            response = requests.post(url, params=data, headers=headers)
        elif method.upper() == 'GET':
            response = requests.get(url, params=data, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    except Exception as e:
        print(f"Could not make {method} request: {e}")
        if status_code:
            return None, None
        return None

    if status_code:
        return get_response(response, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json), get_status_code(response)
    return get_response(response, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json)


def get_json_response(response, response_result=None, load_nested_json=True):
    response_result = response_result or 'result'
    try:
        response_json = response.json()
        if isinstance(response_json,dict):
            response_json = response_json.get(response_result, response_json)
        if load_nested_json:
            response_json = load_inner_json(response_json)
        if response_json is not None:
            return response_json
        # Fallback to the last key if 'result' is not found
        last_key = list(response_json.keys())[-1] if response_json else None
        return response_json.get(last_key, None)
    except Exception as e:
        print(f"Could not read JSON response: {e}")
        return None


def get_response(response, response_result=None, raw_response=False, load_nested_json=True):
    if raw_response:
        return response
    json_response = get_json_response(response, response_result=response_result, load_nested_json=load_nested_json)
    if json_response is not None:
        return json_response
    text_response = get_text_response(response)
    if text_response:
        return text_response
    return response.content  # Return raw content as a last resort

def postRequest(url, data, headers=None, endpoint=None, status_code=False, raw_response=False, response_result=None, load_nested_json=True):
    return make_request(url, data=data, headers=headers, endpoint=endpoint, method='POST', status_code=status_code, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json)

def getRequest(url, data, headers=None, endpoint=None, status_code=False, raw_response=False, response_result=None, load_nested_json=True):
    return make_request(url, data=data, headers=headers, endpoint=endpoint, method='GET', status_code=status_code, raw_response=raw_response, response_result=response_result, load_nested_json=load_nested_json)
