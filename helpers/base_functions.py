import requests
import logging
from resources.config import BASE_URL

# Send a POST request
def send_post_request(endpoint, token, data):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    url = f"{BASE_URL}{endpoint}"
    print(f"Making POST request to: {url}")
    response = requests.post(url, headers=headers, json=data)
    
    # Log the response for debugging
    logging.info(f"POST request to {url} returned status code {response.status_code}")
    print("Response JSON:", response.json())  # Debugging purpose

    response.raise_for_status()  # Raise an error for bad status codes
    return response

# Send a GET request
def send_get_request(endpoint, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, headers=headers)
        logging.info(f"GET request to {url} successful")
        print("Response JSON:", response.json())  # Debugging purpose
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as err:
        logging.error(f"GET {url} failed: {err}")
        raise

# Send a PUT request
def send_put_request(endpoint, token, data):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.put(url, headers=headers, json=data)
        logging.info(f"PUT request to {url} successful")
        print("Response JSON:", response.json())  # Debugging purpose
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as err:
        logging.error(f"PUT {url} failed: {err}")
        raise

# Send a DELETE request
def send_delete_request(endpoint, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.delete(url, headers=headers)
        logging.info(f"DELETE request to {url} successful")
        
        # Only try to decode JSON if there's content
        if response.status_code == 204 or not response.content:  # 204 No Content expected
            print("No content in response, deletion successful.")
        else:
            print("Response JSON:", response.json())  # Debugging purpose
        
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as err:
        logging.error(f"DELETE {url} failed: {err}")
        raise
