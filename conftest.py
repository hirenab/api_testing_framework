import os
import uuid
import pytest
from helpers.base_functions import send_dynamic_request
from resources.config import BASE_URL
from tests.test_api import create_user_payload

TOKEN = os.getenv('API_TOKEN')

@pytest.fixture(autouse=True)
def setup_and_teardown(request):
    # Skip user creation if test is marked with 'no_setup'
    if request.node.get_closest_marker("no_setup"):
        yield None
        return

    max_attempts = 3
    user_id = None

    for attempt in range(max_attempts):
        # Use a fresh copy of the payload to avoid global mutations
        payload = create_user_payload.copy()
        # Generate a unique email using uuid
        payload['email'] = f"hiren_{uuid.uuid4()}@example.com"

        print(f"Setting up resources before test... Attempt {attempt + 1}")
        response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=payload)
        response_data = response.json()
        print(f"Create user response ({response.status_code}): {response_data}")

        # Check if user creation succeeded (status code 201) and the response is a dict with an 'id'
        if response.status_code == 201:
            if isinstance(response_data, dict) and 'id' in response_data:
                user_id = response_data['id']
                break
            else:
                raise Exception(f"Unexpected response format: {response_data}")
        else:
            # If error is due to duplicate email, retry
            if response.status_code == 422 and any("has already been taken" in err.get('message', '') for err in response_data):
                print("Duplicate email error received, retrying with a new email...")
                continue
            else:
                pytest.skip(f"User creation failed with status {response.status_code}: {response_data}")
    else:
        pytest.skip("User creation failed after multiple attempts.")

    yield user_id

    print("Tearing down resources after test...")
    send_dynamic_request("DELETE", f"/public/v2/users/{user_id}", token=TOKEN)

# Hook to add dynamic workers option
def pytest_addoption(parser):
    parser.addoption(
        "--workers", action="store", default="auto", help="Number of workers for multiprocessing"
    )

@pytest.fixture(scope="session")
def worker_count(request):
    return request.config.getoption("--workers")

# Hook to modify collected items before test run
def pytest_collection_modifyitems(session, config, items):
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

# Capture logs when a test fails
def pytest_runtest_logreport(report):
    if report.when == 'call' and report.failed:
        print(f"Test {report.nodeid} failed.")
