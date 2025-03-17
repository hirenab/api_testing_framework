
import requests
from utils.logger import logger
from utils.config import BASE_URL, TIMEOUT

def send_get_request(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        logger.info(f"GET {url} - Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"GET {url} failed: {str(e)}")
        raise

def send_post_request(endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.post(url, json=data, timeout=TIMEOUT)
        response.raise_for_status()
        logger.info(f"POST {url} - Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"POST {url} failed: {str(e)}")
        raise

def send_put_request(endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.put(url, json=data, timeout=TIMEOUT)
        response.raise_for_status()
        logger.info(f"PUT {url} - Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"PUT {url} failed: {str(e)}")
        raise

def send_delete_request(endpoint):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.delete(url, timeout=TIMEOUT)
        response.raise_for_status()
        logger.info(f"DELETE {url} - Status: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"DELETE {url} failed: {str(e)}")
        raise
