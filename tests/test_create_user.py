from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app=app)

def test_create_user():
    response = client.post("/api/users/create", json={
        "username": "John Doe",
        "email": "johndoe@gmail.com",
        "password": "12345",
    })
    
    assert response.status_code == status.HTTP_201_CREATED

    assert isinstance(response.json(), dict)

    assert all(key in response.json() for key in ("user_id", "username", "email", "password")) 

def test_create_existing_user():
    response = client.post("/api/users/create", json={
        "username": "John Doe",
        "email": "johndoe@gmail.com",
        "password": "12345",
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json() == { "detail" : "User already exists" }
