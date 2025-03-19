
import pytest
from helpers.base_functions import *
from helpers.payloads import * 

from helpers import *
# Importing payload data for creating and updating posts

create_post_payload = create_post_payload
update_post_payload = update_post_payload
# Test function for GET request to retrieve a post
@pytest.mark.get_request
def test_get_post():
    """
    Test the GET request to retrieve a specific post by its ID.
    """
    response = send_get_request("/posts/1")  # Sending GET request for post with ID 1
    assert response.status_code == 200  # Assert that the response status is 200 (OK)
    assert response.json()["id"] == 1  # Assert that the retrieved post has the expected ID (1)

# Test function for POST request to create a new post
@pytest.mark.post_request
def test_create_post():
    """
    Test the POST request to create a new post.
    """
    response = send_post_request("/posts", data=create_post_payload)  # Sending POST request with payload to create a new post
    assert response.status_code == 201  # Assert that the response status is 201 (Created)
    assert response.json()["title"] == create_post_payload["title"]  # Assert that the created post has the correct title from the payload

# Test function for PUT request to update an existing post
@pytest.mark.put_request
def test_update_post():
    """
    Test the PUT request to update an existing post.
    """
    response = send_put_request("/posts/1", data=update_post_payload)  # Sending PUT request to update post with ID 1
    assert response.status_code == 200  # Assert that the response status is 200 (OK)
    assert response.json()["title"] == update_post_payload["title"]  # Assert that the updated post has the correct title from the payload

# Test function for DELETE request to delete a post
@pytest.mark.delete_request
def test_delete_post():
    """
    Test the DELETE request to delete a specific post.
    """
    response = send_delete_request("/posts/1")  # Sending DELETE request to delete post with ID 1
    assert response.status_code == 200  # Assert that the response status is 200 (OK), indicating successful deletion


