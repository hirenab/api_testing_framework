import pytest
import requests
from helpers.logger import logger  # Custom logger to log request/response information
from helpers.config import BASE_URL, TIMEOUT  # Base URL and timeout configuration for requests

# Function to send a GET request
@pytest.mark.get_request
def send_get_request(endpoint, params=None):

    url = f"{BASE_URL}{endpoint}"  # Construct full URL by appending the endpoint to the base URL
    try:
        # Send the GET request
        response = requests.get(url, params=params, timeout=TIMEOUT)
        # Raise an exception for HTTP errors (4xx and 5xx)
        response.raise_for_status()
        # Log the successful request
        logger.info(f"GET {url} - Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        # Log the error if the request fails
        logger.error(f"GET {url} failed: {str(e)}")
        raise  # Re-raise the exception for the caller to handle

# Function to send a POST request
@pytest.mark.post_request
def send_post_request(endpoint, data=None):

    url = f"{BASE_URL}{endpoint}"  # Construct full URL by appending the endpoint to the base URL
    try:
        # Send the POST request with the data payload
        response = requests.post(url, json=data, timeout=TIMEOUT)
        response.raise_for_status()
        # Log the successful request
        logger.info(f"POST {url} - Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        # Log the error if the request fails
        logger.error(f"POST {url} failed: {str(e)}")
        raise

# Function to send a PUT request
@pytest.mark.put_request
def send_put_request(endpoint, data=None):

    url = f"{BASE_URL}{endpoint}"  # Construct full URL by appending the endpoint to the base URL
    try:
        # Send the PUT request with the data payload
        response = requests.put(url, json=data, timeout=TIMEOUT)
        response.raise_for_status()
        # Log the successful request
        logger.info(f"PUT {url} - Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        # Log the error if the request fails
        logger.error(f"PUT {url} failed: {str(e)}")
        raise

# Function to send a DELETE request
@pytest.mark.delete_request
def send_delete_request(endpoint):

    url = f"{BASE_URL}{endpoint}"  # Construct full URL by appending the endpoint to the base URL
    try:
        # Send the DELETE request
        response = requests.delete(url, timeout=TIMEOUT)
        response.raise_for_status()
        # Log the successful request
        logger.info(f"DELETE {url} - Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        # Log the error if the request fails
        logger.error(f"DELETE {url} failed: {str(e)}")
        raise
