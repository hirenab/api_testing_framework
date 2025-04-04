import pytest
import json
import os
import logging
import uuid
from helpers.base_functions import send_dynamic_request

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the token from the environment variable
TOKEN = os.getenv('API_TOKEN')

# Load the JSON payloads from the file
with open('resources/user_payloads.json', 'r') as file:
    payloads = json.load(file)

# Extract the create and update payloads
create_user_payload = payloads['create_user_payload']
update_user_payload = payloads['update_user_payload']
invalid_update_payload = payloads['invalid_update_payload']


@pytest.fixture
def setup_and_teardown():
    if not TOKEN:
        raise Exception("API_TOKEN environment variable is not set")
    
    # Use a fresh copy of the payload and generate a unique email with UUID
    payload = create_user_payload.copy()
    unique_email = f"hiren_{uuid.uuid4()}@example.com"
    payload['email'] = unique_email

    logger.info("Setting up resources before test...")
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=payload)
    logger.info(f"Create user response: {response.status_code} - {response.json()}")

    if response.status_code != 201:
        raise Exception(f"User creation failed: {response.status_code} - {response.json()}")

    user_id = response.json()['id']
    # Return both user_id and email for duplicate tests
    yield {"user_id": user_id, "email": unique_email}

    logger.info(f"Tearing down resources after test, deleting user with ID: {user_id}")
    send_dynamic_request("DELETE", f"/public/v2/users/{user_id}", token=TOKEN)


@pytest.mark.create_user(order=1)
def test_verify_user_can_create_new_user_successfully(setup_and_teardown):
    user = setup_and_teardown
    user_id = user["user_id"]
    assert user_id is not None, "User creation failed"
    logger.info(f"Created user successfully with ID: {user_id}")


@pytest.mark.get_user(order=2)
def test_verify_user_can_get_user_details_successfully(setup_and_teardown):
    user = setup_and_teardown
    user_id = user["user_id"]
    logger.info(f"Fetching user details for ID: {user_id}")
    response = send_dynamic_request("GET", f"/public/v2/users/{user_id}", token=TOKEN)
    logger.info(f"Get user response: {response.status_code} - {response.json()}")
    
    assert response.status_code == 200, "Fetching user failed"
    user_data = response.json()
    assert user_data['id'] == user_id, "User ID mismatch"


@pytest.mark.update_user(order=3)
def test_verify_user_can_update_user_successfully(setup_and_teardown):
    user = setup_and_teardown
    user_id = user["user_id"]
    # Generate a new unique email for the update payload to ensure uniqueness
    updated_payload = update_user_payload.copy()
    updated_payload['email'] = f"updated_{uuid.uuid4()}@example.com"
    
    logger.info(f"Updating user details for ID: {user_id}")
    response = send_dynamic_request("PUT", f"/public/v2/users/{user_id}", token=TOKEN, data=updated_payload)
    logger.info(f"Update user response: {response.status_code} - {response.json()}")

    assert response.status_code == 200, "Updating user failed"
    updated_data = response.json()
    assert updated_data['email'] == updated_payload['email'], "Email not updated"


@pytest.mark.delete_user(order=4)
def test_verify_user_can_delete_user_successfully(setup_and_teardown):
    user = setup_and_teardown
    user_id = user["user_id"]
    logger.info(f"User {user_id} will be deleted after the test.")
    # No further action needed; teardown in fixture deletes the user.


@pytest.mark.invalid_email
@pytest.mark.negative_test
def test_verify_cannot_create_user_with_invalid_email():
    # This test creates a user with an invalid email, so it doesn't use the fixture.
    invalid_payload = invalid_update_payload.copy()
    logger.info(f"Testing invalid email creation with payload: {invalid_payload}")
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=invalid_payload)
    logger.info(f"Invalid email response: {response.status_code} - {response.json()}")

    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}"
    response_json = response.json()
    email_error = next((error for error in response_json if error['field'] == 'email'), None)
    assert email_error is not None, "Email validation error not found in response"
    assert email_error['message'] == 'is invalid', f"Unexpected error message: {email_error['message']}"


@pytest.mark.missing_fields
@pytest.mark.negative_test
def test_verify_cannot_create_user_without_required_fields():
    incomplete_payload = {"email": ""}
    logger.info(f"Testing user creation with missing fields: {incomplete_payload}")
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=incomplete_payload)
    logger.info(f"Missing fields response: {response.status_code} - {response.json()}")
    
    assert response.status_code == 422, "User creation should fail due to missing fields"
    error_message = response.json()
    required_fields = ["email", "name", "gender", "status"]
    for field in required_fields:
        assert any(error['field'] == field for error in error_message), f"{field} validation error not found"


@pytest.mark.invalid_email
@pytest.mark.negative_test
def test_verify_cannot_update_user_with_invalid_email(setup_and_teardown):
    user = setup_and_teardown
    user_id = user["user_id"]
    logger.info(f"Testing invalid email update for user ID: {user_id}")
    response = send_dynamic_request("PUT", f"/public/v2/users/{user_id}", token=TOKEN, data=invalid_update_payload)
    logger.info(f"Invalid email update response: {response.status_code} - {response.json()}")

    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}"
    response_json = response.json()
    assert response_json[0]['field'] == 'email', f"Expected 'email' field, but got {response_json[0]['field']}"
    assert response_json[0]['message'] == 'is invalid', f"Expected 'is invalid' message, but got {response_json[0]['message']}"


@pytest.mark.duplicate_email
@pytest.mark.negative_test
def test_verify_cannot_create_user_with_duplicate_email(setup_and_teardown):
    user = setup_and_teardown
    # Use the email from the fixture to force a duplicate
    duplicate_payload = create_user_payload.copy()
    duplicate_payload['email'] = user["email"]
    logger.info(f"Testing duplicate email creation with payload: {duplicate_payload}")
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=duplicate_payload)
    logger.info(f"Duplicate email response: {response.status_code} - {response.json()}")

    assert response.status_code == 422, "Expected failure due to duplicate email"
    response_json = response.json()
    email_error = next((error for error in response_json if error['field'] == 'email'), None)
    assert email_error is not None, "Email duplication error not found"
    assert email_error['message'] == 'has already been taken', f"Unexpected error message: {email_error['message']}"


#   Parameterized Test for Updating a User

@pytest.mark.update_user
@pytest.mark.parametrize("payload_key,expected_status", [
    ("valid_update_payload", 200),
    ("invalid_update_payload", 422)
])
def test_update_user_parametrized(setup_and_teardown, payload_key, expected_status):
    """
    Parameterized test for updating a user.
    """
    user = setup_and_teardown
    user_id = user["user_id"]

    # For a valid update payload
    payload = payloads[payload_key].copy()
    if payload_key == 'valid_update_payload':
        payload['email'] = f"updated_{uuid.uuid4()}@example.com"

    logger.info(f"Updating user with payload: {payload} for user ID: {user_id}")
    response = send_dynamic_request("PUT", f"/public/v2/users/{user_id}", token=TOKEN, data=payload)

    logger.info(f"Parameterized update response: {response.status_code} - {response.json()}")
    assert response.status_code == expected_status, f"Expected {expected_status}, but got {response.status_code}"


def test_verify_cannot_get_non_existent_user():
    non_existent_user_id = 9999999
    response = send_dynamic_request("GET", f"/public/v2/users/{non_existent_user_id}", token=TOKEN)
    assert response.status_code == 404, "Expected 404 for non-existent user"
    response_json = response.json()
    assert response_json['message'] == 'Resource not found', f"Unexpected message: {response_json['message']}"


def test_verify_cannot_update_user_with_empty_fields(setup_and_teardown):
    user = setup_and_teardown
    user_id = user["user_id"]
    empty_update_payload = {"name": "", "email": ""}
    response = send_dynamic_request("PUT", f"/public/v2/users/{user_id}", token=TOKEN, data=empty_update_payload)
    assert response.status_code == 422, "Expected 422 for updating with empty fields"
    response_json = response.json()
    required_fields = ["email", "name"]
    for field in required_fields:
        assert any(error['field'] == field for error in response_json), f"{field} validation error not found"


def test_verify_cannot_access_with_invalid_token():
    invalid_token = "invalid_token_value"
    response = send_dynamic_request("GET", "/public/v2/users", token=invalid_token)
    assert response.status_code == 401, "Expected 401 Unauthorized"
    response_json = response.json()
    assert response_json['message'] == 'Invalid token', f"Unexpected message: {response_json['message']}"


def test_verify_cannot_delete_non_existent_user():
    non_existent_user_id = 9999999
    response = send_dynamic_request("DELETE", f"/public/v2/users/{non_existent_user_id}", token=TOKEN)
    assert response.status_code == 404, "Expected 404 for deleting non-existent user"
    response_json = response.json()
    assert response_json['message'] == 'Resource not found', f"Unexpected message: {response_json['message']}"


def test_verify_invalid_http_method():
    response = send_dynamic_request("PATCH", "/public/v2/users", token=TOKEN)
    assert response.status_code in [404, 405], f"Expected 404 or 405, but got {response.status_code}"
