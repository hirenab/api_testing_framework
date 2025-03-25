import pytest
import json
import time
import os  # Import to access environment variables
from helpers.base_functions import send_dynamic_request
from resources.config import BASE_URL

# Get the token from the environment variable
TOKEN = os.getenv('API_TOKEN')

# Load the JSON payloads from the file
with open('resources/user_payloads.json', 'r') as file:
    payloads = json.load(file)

# Extract the create and update payloads
create_user_payload = payloads['create_user_payload']
update_user_payload = payloads['update_user_payload']
invalid_update_payload = payloads['invalid_update_payload']

# Dynamically modify the email to ensure uniqueness for each test run
create_user_payload['email'] = f"hiren_{int(time.time())}@example.com"
update_user_payload['email'] = f"hirenab_{int(time.time())}@example.com"
invalid_update_payload['email'] = f"hirenab"

@pytest.fixture
def setup_and_teardown():
    if not TOKEN:
        raise Exception("API_TOKEN environment variable is not set")
    
    # Setup: Create a user
    print("Setting up resources before test...")
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=create_user_payload)
    
    user_id = response.json()['id']
    yield user_id
    
    # Teardown: Delete the user
    print("Tearing down resources after test...")
    send_dynamic_request("DELETE", f"/public/v2/users/{user_id}", token=TOKEN)

    # Verify user can create a new user successfully
def test_verify_user_can_create_new_user_successfully(setup_and_teardown):
    # Setup should create a user and return the user ID
    user_id = setup_and_teardown
    assert user_id is not None, "User creation failed"
    print(f"Created user with ID: {user_id}")

    # Verify user can get user details successfully
def test_verify_user_can_get_user_details_successfully(setup_and_teardown):
    # Get the user by ID created during setup
    user_id = setup_and_teardown
    response = send_dynamic_request("GET", f"/public/v2/users/{user_id}", token=TOKEN)
    assert response.status_code == 200, "Fetching user failed"
    user_data = response.json()
    print(f"Fetched user: {user_data}")
    assert user_data['id'] == user_id, "User ID mismatch"

    # Verify user can update user details successfully
def test_verify_user_can_update_user_successfully(setup_and_teardown):
    # Update the user created during setup
    user_id = setup_and_teardown
    response = send_dynamic_request("PUT", f"/public/v2/users/{user_id}", token=TOKEN, data=update_user_payload)
    assert response.status_code == 200, "Updating user failed"
    updated_data = response.json()
    print(f"Updated user: {updated_data}")
    assert updated_data['email'] == update_user_payload['email'], "Email not updated"

    # Verify user can delete a user successfully
def test_verify_user_can_delete_user_successfully(setup_and_teardown):
    # Teardown will automatically delete the user
    user_id = setup_and_teardown
    print(f"User {user_id} will be deleted after the test.")

    # Verify user cannot create a user with an invalid email
def test_verify_cannot_create_user_with_invalid_email():
    # Make the request to create a user with invalid email
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=invalid_update_payload)
    
    # Assert that the status code is 422 (Unprocessable Entity) since the email is invalid
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}"
    response_json = response.json()
    email_error = next((error for error in response_json if error['field'] == 'email'), None)
    assert email_error is not None, "Email validation error not found in response"
    assert email_error['message'] == 'is invalid', f"Unexpected error message: {email_error['message']}"

    # Verify user cannot create a user without required fields
def test_verify_cannot_create_user_without_required_fields():
    incomplete_payload = {
        "email": "" 
    }
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=incomplete_payload)
    
    assert response.status_code == 422, "User creation should fail due to missing fields"
    error_message = response.json()
    print(f"Error response: {error_message}")
    
    # Check all the required fields are missing
    required_fields = ["email", "name", "gender", "status"]
    for field in required_fields:
        assert any(error['field'] == field for error in error_message), f"{field} validation error not found"

# Verify user cannot update a user with invalid email
def test_verify_cannot_update_user_with_invalid_email(setup_and_teardown):
    user_id = setup_and_teardown
    response = send_dynamic_request("PUT", f"/public/v2/users/{user_id}", token=TOKEN, data=invalid_update_payload)
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}"
    response_json = response.json()
    assert response_json[0]['field'] == 'email', f"Expected 'email' field, but got {response_json[0]['field']}"
    assert response_json[0]['message'] == 'is invalid', f"Expected 'is invalid' message, but got {response_json[0]['message']}"

    # Verify user cannot create a user with duplicate email
def test_verify_cannot_create_user_with_duplicate_email(setup_and_teardown):
    user_id = setup_and_teardown
    duplicate_payload = create_user_payload.copy()
    response = send_dynamic_request("POST", "/public/v2/users", token=TOKEN, data=duplicate_payload)
    assert response.status_code == 422, "Expected failure due to duplicate email"
    response_json = response.json()
    email_error = next((error for error in response_json if error['field'] == 'email'), None)
    assert email_error is not None, "Email duplication error not found"
    assert email_error['message'] == 'has already been taken', f"Unexpected error message: {email_error['message']}"

    # Verify user cannot get details of a non-existent user
def test_verify_cannot_get_non_existent_user():
    non_existent_user_id = 9999999
    response = send_dynamic_request("GET", f"/public/v2/users/{non_existent_user_id}", token=TOKEN)
    assert response.status_code == 404, "Expected 404 for non-existent user"
    response_json = response.json()
    assert response_json['message'] == 'Resource not found', f"Unexpected message: {response_json['message']}"

    # Verify user cannot update a user with empty fields
def test_verify_cannot_update_user_with_empty_fields(setup_and_teardown):
    user_id = setup_and_teardown
    empty_update_payload = {
        "name": "",
        "email": ""
    }
    response = send_dynamic_request("PUT", f"/public/v2/users/{user_id}", token=TOKEN, data=empty_update_payload)
    assert response.status_code == 422, "Expected 422 for updating with empty fields"
    response_json = response.json()
    required_fields = ["email", "name"]
    for field in required_fields:
        assert any(error['field'] == field for error in response_json), f"{field} validation error not found"

    # Verify access is denied with invalid token
def test_verify_cannot_access_with_invalid_token():
    invalid_token = "invalid_token_value"
    response = send_dynamic_request("GET", "/public/v2/users", token=invalid_token)
    assert response.status_code == 401, "Expected 401 Unauthorized"
    response_json = response.json()
    assert response_json['message'] == 'Invalid token', f"Unexpected message: {response_json['message']}"

    # Verify user cannot delete a non-existent user
def test_verify_cannot_delete_non_existent_user():
    non_existent_user_id = 9999999
    response = send_dynamic_request("DELETE", f"/public/v2/users/{non_existent_user_id}", token=TOKEN)
    assert response.status_code == 404, "Expected 404 for deleting non-existent user"
    response_json = response.json()
    assert response_json['message'] == 'Resource not found', f"Unexpected message: {response_json['message']}"

    # Verify invalid HTTP method handling
def test_verify_invalid_http_method():
    response = send_dynamic_request("PATCH", "/public/v2/users", token=TOKEN)
    assert response.status_code in [404, 405], f"Expected 404 or 405, but got {response.status_code}"
