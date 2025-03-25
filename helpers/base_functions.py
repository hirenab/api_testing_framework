import requests
import logging
from resources.config import BASE_URL

# Send a POST, GET, PUT, DELETE request
def send_dynamic_request(method, endpoint, token, data=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = f"{BASE_URL}{endpoint}"
    
    try:
        # Send request based on method
        if method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
         # Check for validation errors (assuming status code 422 for validation issues)
        # if response.status_code == 422:
        #      logging.info(f"Validation failed: {response.json()}")
        # else:
        #      response.raise_for_status()
            
        return response

    except requests.exceptions.RequestException as err:
        #  logging.error(f"Request failed: {err}")
        raise
