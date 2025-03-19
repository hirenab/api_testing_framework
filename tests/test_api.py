import pytest
from helpers.base_functions import send_get_request, send_post_request, send_put_request, send_delete_request
from helpers.payloads import create_user_payload, update_user_payload  # Updated payloads for /users
from helpers.schemas import validate_response, create_user_schema, update_user_schema, delete_user_schema

# Add the setup and teardown fixture
@pytest.fixture(scope="function")
def setup_and_teardown():
    print("\nSetting up resources before test...")
    yield
    print("\nTearing down resources after test...")

# Test GET request with schema validation
@pytest.mark.get_request
def test_get_user(setup_and_teardown):
    response = send_get_request("/users/1")
    assert response.status_code == 200
    response_data = response.json()

    # Validate the response using the correct schema for GET /users/{id}
    assert validate_response(response_data, create_user_schema), "GET /users/1 response validation failed"

# Test POST request with schema validation
@pytest.mark.post_request
def test_create_user(setup_and_teardown):
    response = send_post_request("/users", data=create_user_payload)
    assert response.status_code == 201, "POST /users request failed"
    response_data = response.json()

    # Validate response with updated create_user_schema
    assert validate_response(response_data, create_user_schema), "POST /users response validation failed"

# Test PUT request with schema validation
@pytest.mark.put_request
def test_update_user(setup_and_teardown):
    response = send_put_request("/users/1", data=update_user_payload)
    assert response.status_code == 200, "PUT /users/1 request failed"
    response_data = response.json()
    
    # Validate response with update_user_schema
    assert validate_response(response_data, update_user_schema), "PUT /users/1 response validation failed"

# Test DELETE request with schema validation

@pytest.mark.delete_request
def test_delete_user(setup_and_teardown):
    response = send_delete_request("/users/1")
    assert response.status_code == 200, "DELETE /users/1 request failed"
    response_data = response.json()
    
    # Validate response with updated delete_user_schema
    assert validate_response(response_data, delete_user_schema), "DELETE /users/1 response validation failed"