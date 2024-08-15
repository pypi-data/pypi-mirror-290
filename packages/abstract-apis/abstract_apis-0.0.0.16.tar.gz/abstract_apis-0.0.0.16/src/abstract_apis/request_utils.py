import json
from abstract_utilities import make_list
def get_headers():
    return {
        'Content-Type': 'application/json',
    }

def ensure_json(data):
    if isinstance(data, str):
        try:
            json.loads(data)  # Verify it's valid JSON
            return data
        except ValueError:
            pass  # Not valid JSON, continue to dump it
    return json.dumps(data)

def stripit(string, chars=[]):
    string = string or ''
    for char in make_list(chars):
        string = string.strip(char)
    return string

def make_endpoint(endpoint):
    return stripit(endpoint, chars='/')

def make_url(url):
    return stripit(url, chars='/')

def get_url(url, endpoint=None):
    return stripit(f"{make_url(url)}/{make_endpoint(endpoint)}", chars='/')

def get_text_response(response):
    try:
        return response.text
    except Exception as e:
        print(f"Could not read text response: {e}")
        return None

def load_inner_json(data):
    """Recursively load nested JSON strings within the main JSON response, even if nested within lists."""
    if isinstance(data, str):
        try:
            return load_inner_json(json.loads(data))  # Recursively parse inner JSON strings
        except (ValueError, TypeError):
            return data
    elif isinstance(data, dict):
        return {key: load_inner_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [load_inner_json(item) for item in data]
    return data    
def get_status_code(response):
    try:
        return response.status_code
    except Exception as e:
        print(f"Could not get status code: {e}")
        return None
