import pytest
import time
import os  # Import to access environment variables
from helpers.base_functions import send_dynamic_request
from resources.config import BASE_URL
from tests.test_api import create_user_payload, update_user_payload, invalid_update_payload  # Import payloads

# Get the token from the environment variable
TOKEN = os.getenv('API_TOKEN')

@pytest.fixture(autouse=True)
def setup_and_teardown():
    if not TOKEN:
        raise Exception("API_TOKEN environment variable is not set")
    
    # Dynamically modify the email to ensure uniqueness for each test run
    create_user_payload['email'] = f"hiren_{int(time.time())}@example.com"
    
    # Setup: Create a user using the existing payload and dynamic request function
    print("Setting up resources before test...")
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=create_user_payload)
    
    user_id = response.json()['id']
    yield user_id
    
    # Teardown: Delete the user
    print("Tearing down resources after test...")
    send_dynamic_request("DELETE", f"/public/v2/users/{user_id}", token=TOKEN)
