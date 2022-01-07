from fastapi import responses
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user_already_exists():
    response = client.post('/signup', json={"email": "test@user.com", "first_name": "test", "last_name": "user", "password": "fakepassword", },)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_read_user_not_found():
    response = client.get('/user/34')
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_login_user_not_found():
    response = client.post('/login', json={"password": "fakepassword", "email": "random@fakeemail.com"},)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_check_task_status_task_not_found():
    response = client.get('/status/34')
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}