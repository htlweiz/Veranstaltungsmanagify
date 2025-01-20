import pytest
from fastapi.testclient import TestClient
from api.auth import router, msal_client, users
from api.model import MSALLogin, SignupSchema, LoginDB
from db.model import User
from unittest.mock import patch, MagicMock
import bcrypt



def test_signup(test_app: TestClient, monkeypatch):
    def mock(_):
        return User(
            email="test@example.com",
            password="irrelevant",
            access_token="access_token",
        )

    monkeypatch.setattr(users, "create", mock)

    response = test_app.post("/signup", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 201
    assert response.text == "access_token"

def test_login_success(test_app: TestClient, monkeypatch):
    def mock(_):
        return User(
            email="test@example.com",
            password="irrelevant",
            access_token="access_token",
        )

    monkeypatch.setattr(users, "create", mock)

    test_app.post("/signup", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    def mock_login(_):
        user = User(
            email="test@example.com",
            password="testpassword",
            access_token="access_token",
        )

        byte_password = user.password.encode("utf-8")
        salt = bcrypt.gensalt(8)
        hsh = bcrypt.hashpw(byte_password, salt)

        user.password = hsh.decode("utf-8")
        return user

    monkeypatch.setattr(users, "get_by_email", mock_login)
    
    response = test_app.post("/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user_not_found(test_app: TestClient):
    response = test_app.post("/login", json={
        "email": "nonexistent@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 404
    assert response.text == "User not found"

def test_login_invalid_password(test_app: TestClient):
    test_app.post("/signup", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    
    response = test_app.post("/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.text == "Invalid Password"