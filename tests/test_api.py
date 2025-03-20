import pytest
from helpers.base_functions import send_post_request, send_get_request, send_put_request, send_delete_request
from resources.payloads import create_user_payload, update_user_payload
from resources.config import BASE_URL
from helpers.auth import TOKEN 

@pytest.fixture
def setup_and_teardown():
    # Setup: Create a user
    print("Setting up resources before test...")
    response = send_post_request("/public/v2/users", token=TOKEN, data=create_user_payload)
    user_id = response.json()['id']
    yield user_id
    # Teardown: Delete the user
    print("Tearing down resources after test...")
    send_delete_request(f"/public/v2/users/{user_id}", token=TOKEN)

def test_create_user(setup_and_teardown):
    # Setup should create a user and return the user ID
    user_id = setup_and_teardown
    assert user_id is not None, "User creation failed"
    print(f"Created user with ID: {user_id}")

def test_get_user(setup_and_teardown):
    # Get the user by ID created during setup
    user_id = setup_and_teardown
    response = send_get_request(f"/public/v2/users/{user_id}", token=TOKEN)
    assert response.status_code == 200, "Fetching user failed"
    user_data = response.json()
    print(f"Fetched user: {user_data}")
    assert user_data['id'] == user_id, "User ID mismatch"

def test_update_user(setup_and_teardown):
    # Update the user created during setup
    user_id = setup_and_teardown
    response = send_put_request(f"/public/v2/users/{user_id}", token=TOKEN, data=update_user_payload)
    assert response.status_code == 200, "Updating user failed"
    updated_data = response.json()
    print(f"Updated user: {updated_data}")
    assert updated_data['email'] == update_user_payload['email'], "Email not updated"

def test_delete_user(setup_and_teardown):
    # Teardown will automatically delete the user
    user_id = setup_and_teardown
    print(f"User {user_id} will be deleted after the test.")
