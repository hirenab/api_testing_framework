
import pytest
from utils.base_functions import send_get_request, send_post_request, send_put_request, send_delete_request
from tests.payloads import create_post_payload, update_post_payload

@pytest.mark.smoke
def test_get_post():
    response = send_get_request("/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.regression
def test_create_post():
    response = send_post_request("/posts", data=create_post_payload)
    assert response.status_code == 201
    assert response.json()["title"] == create_post_payload["title"]

@pytest.mark.regression
def test_update_post():
    response = send_put_request("/posts/1", data=update_post_payload)
    assert response.status_code == 200
    assert response.json()["title"] == update_post_payload["title"]

@pytest.mark.regression
def test_delete_post():
    response = send_delete_request("/posts/1")
    assert response.status_code == 200
