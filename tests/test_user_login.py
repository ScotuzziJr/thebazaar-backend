from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app=app)

def test_user_login():
    response = client.post("/api/users/login", json={
        "username": "John Doe",
        "password": "12345",
    })
    
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response.json(), dict)

    assert all(key in response.json() for key in ('access_token', 'token_type')) 

def test_user_login_invalid_credentials():
    response = client.post("/api/users/login", json={
        "username": "John", # wrong username
        "email": "johndoe@gmail.com",
        "password": "12345",
    })

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json() == { "detail" : "Invalid credentials" }
