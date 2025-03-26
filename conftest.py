import pytest
import time
import os
from helpers.base_functions import send_dynamic_request
from resources.config import BASE_URL
from tests.test_api import create_user_payload, update_user_payload, invalid_update_payload  # Import payloads

TOKEN = os.getenv('API_TOKEN')

@pytest.fixture(autouse=True)
def setup_and_teardown():
    if not TOKEN:
        raise Exception("API_TOKEN environment variable is not set")
    
    create_user_payload['email'] = f"hiren_{int(time.time())}@example.com"
    
    # Create a user using the existing payload and dynamic request function
    print("Setting up resources before test...")
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=create_user_payload)
    
    user_id = response.json()['id']
    yield user_id
    
    # Delete the user
    print("Tearing down resources after test...")
    send_dynamic_request("DELETE", f"/public/v2/users/{user_id}", token=TOKEN)

    # Hook to modify collected items before the test run
def pytest_collection_modifyitems(session, config, items):
    # Custom marker to each collected test item
    for item in items:
        if "get" in item.nodeid.lower():
            item.add_marker(pytest.mark.get_request)
        elif "post" in item.nodeid.lower():
            item.add_marker(pytest.mark.post_request)
        elif "put" in item.nodeid.lower():
            item.add_marker(pytest.mark.put_request)
        elif "delete" in item.nodeid.lower():
            item.add_marker(pytest.mark.delete_request)

    # Hook to execute code before the test session starts
def pytest_sessionstart(session):
    print("\nTest session is starting...\n")

    # Hook to execute code after the test session finishes
def pytest_sessionfinish(session, exitstatus):
    print("\nTest session has finished.\n")

    # Hook to execute code before each test
def pytest_runtest_setup(item):
    print(f"\nSetting up test: {item.name}\n")

    # Hook to execute code after each test
def pytest_runtest_teardown(item, nextitem):
    print(f"\nTearing down test: {item.name}\n")
