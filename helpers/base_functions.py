import requests
from resources.config import BASE_URL

# Send a POST, GET, PUT, DELETE, PATCH request
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
        elif method.upper() == "PATCH":  # Added support for PATCH method
            response = requests.patch(url, json=data, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        return response

    except requests.exceptions.RequestException as err:
        raise err

