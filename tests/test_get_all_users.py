from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app=app)

def test_get_all_users():
    response = client.get("/api/users/all")
    
    assert response.status_code == status.HTTP_200_OK

    # the response should always be a list - either empty or with dicts
    assert isinstance(response.json(), list)

    # this assertion is poorly written but I check if the list contains dicts only if the list is not empty
    assert isinstance(response.json()[0], dict) if len(response.json()) != 0 else True

    # again I'm checking the keys of dict only if the list is not empty
    assert all(key in response.json()[0] for key in ("user_id", "username", "email", "password")) \
        if len(response.json()) != 0 else True
