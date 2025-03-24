import pytest
import json
import time
import os  # Import to access environment variables
from helpers.base_functions import send_post_request, send_get_request, send_put_request, send_delete_request
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
    response = send_post_request("/public/v2/users", token=TOKEN, data=create_user_payload)
    user_id = response.json()['id']
    yield user_id
    # Teardown: Delete the user
    print("Tearing down resources after test...")
    send_delete_request(f"/public/v2/users/{user_id}", token=TOKEN)

def test_verify_user_can_create_new_user_successfully(setup_and_teardown):
    # Setup should create a user and return the user ID
    user_id = setup_and_teardown
    assert user_id is not None, "User creation failed"
    print(f"Created user with ID: {user_id}")

def test_verify_user_can_get_user_details_successfully(setup_and_teardown):
    # Get the user by ID created during setup
    user_id = setup_and_teardown
    response = send_get_request(f"/public/v2/users/{user_id}", token=TOKEN)
    assert response.status_code == 200, "Fetching user failed"
    user_data = response.json()
    print(f"Fetched user: {user_data}")
    assert user_data['id'] == user_id, "User ID mismatch"

def test_verify_user_can_update_user_successfully(setup_and_teardown):
    # Update the user created during setup
    user_id = setup_and_teardown
    response = send_put_request(f"/public/v2/users/{user_id}", token=TOKEN, data=update_user_payload)
    assert response.status_code == 200, "Updating user failed"
    updated_data = response.json()
    print(f"Updated user: {updated_data}")
    assert updated_data['email'] == update_user_payload['email'], "Email not updated"

def test_verify_user_can_delete_user_successfully(setup_and_teardown):
    # Teardown will automatically delete the user
    user_id = setup_and_teardown
    print(f"User {user_id} will be deleted after the test.")

    # Create user with invalid email
def test_verify_cannot_create_user_with_invalid_email():
    # Make the request to create a user with invalid email
    response = send_post_request("/public/v2/users", token=TOKEN, data=invalid_update_payload)
    
    # Assert that the status code is 422 (Unprocessable Entity) since the email is invalid
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}"
    
    # Extract the response JSON
    response_json = response.json()
    
    # Assert that the response contains the expected error message for the email field
    email_error = next((error for error in response_json if error['field'] == 'email'), None)
    assert email_error is not None, "Email validation error not found in response"
    assert email_error['message'] == 'is invalid', f"Unexpected error message: {email_error['message']}"



    # Create user without required fields
def test_verify_cannot_create_user_without_required_fields():
    incomplete_payload = {
        "email": ""
    }  # Payload missing required fields
    response = send_post_request("/public/v2/users", token=TOKEN, data=incomplete_payload)
    assert response.status_code == 422, "User creation should fail due to missing fields"
    error_message = response.json()
    print(f"Error response: {error_message}")
    assert "email" in error_message[0]['field'], "Error does not mention email field"

    # Update user with invalid email

def test_verify_cannot_update_user_with_invalid_email(setup_and_teardown):
    user_id = setup_and_teardown  # Assuming this returns the user_id from setup
    invalid_update_payload = payloads['invalid_update_payload']
    
    # Sending the PUT request with invalid email
    response = send_put_request(f"/public/v2/users/{user_id}", token=TOKEN, data=invalid_update_payload)
    
    # Assert the status code is 422
    assert response.status_code == 422, f"Expected status code 422, but got {response.status_code}"
    
    # Assert the error message
    response_json = response.json()
    assert response_json[0]['field'] == 'email', f"Expected 'email' field, but got {response_json[0]['field']}"
    assert response_json[0]['message'] == 'is invalid', f"Expected 'is invalid' message, but got {response_json[0]['message']}"

