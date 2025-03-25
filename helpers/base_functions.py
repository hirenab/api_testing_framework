import requests
import logging
from resources.config import BASE_URL

# Send a POST, GET, PUT, DELETE request
def send_dynamic_request(method, endpoint, token, data=None):
    """
    Sends a dynamic HTTP request (POST, GET, PUT, DELETE).

    :param method: HTTP method (e.g., 'POST', 'GET', 'PUT', 'DELETE')
    :param endpoint: API endpoint
    :param token: Authorization token
    :param data: (Optional) Payload data for POST/PUT requests
    :return: Response object
    """
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    if data:
        headers['Content-Type'] = 'application/json'
    
    url = f"{BASE_URL}{endpoint}"
    try:
        # Send request based on method
        if method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        # Log the request and response
        logging.info(f"{method} request to {url} returned status code {response.status_code}")
        
        # Debugging purpose - print response JSON if it exists
        if response.content:  # Check if the response has content
            try:
                print("Response JSON:", response.json())
            except requests.exceptions.JSONDecodeError:
                print("Response is not in JSON format.")
            else:
                print("No content in response.")

        
        # Handle specific status codes
        if response.status_code >= 500:
            response.raise_for_status()
        elif response.status_code == 422:
            logging.error(f"Validation failed: {response.json()}")
        
        return response
    except requests.exceptions.HTTPError as err:
        logging.error(f"{method} request to {url} failed: {err}")
        raise
