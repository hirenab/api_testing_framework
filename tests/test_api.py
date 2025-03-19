import pytest
from helpers.base_functions import send_get_request, send_post_request, send_put_request, send_delete_request
from helpers.payloads import create_post_payload, update_post_payload

# Add the setup and teardown fixture (New Code)
@pytest.fixture(scope="function")
def setup_and_teardown():
    # Setup: This runs before each test
    print("\nSetting up resources before test...")

    yield  # This separates setup and teardown

    # Teardown: This runs after each test
    print("\nTearing down resources after test...")

# Existing Test function for GET request to retrieve a post (Update with fixture)
@pytest.mark.get_request
def test_get_post(setup_and_teardown):  # Add fixture argument here
    response = send_get_request("/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

# Existing Test function for POST request to create a new post (Update with fixture)
@pytest.mark.post_request
def test_create_post(setup_and_teardown):  # Add fixture argument here
    response = send_post_request("/posts", data=create_post_payload)
    assert response.status_code == 201
    assert response.json()["title"] == create_post_payload["title"]

# Existing Test function for PUT request to update a post (Update with fixture)
@pytest.mark.put_request
def test_update_post(setup_and_teardown):  # Add fixture argument here
    response = send_put_request("/posts/1", data=update_post_payload)
    assert response.status_code == 200
    assert response.json()["title"] == update_post_payload["title"]

# Existing Test function for DELETE request to delete a post (Update with fixture)
@pytest.mark.delete_request
def test_delete_post(setup_and_teardown):  # Add fixture argument here
    response = send_delete_request("/posts/1")
    assert response.status_code == 200