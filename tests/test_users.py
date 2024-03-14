from app import schema
from app.config import settings
from jose import jwt
import pytest

def test_root(client):
    res = client.get("/")
    # print(res.json()['message'])
    assert res.json()['message'] == "Hello Yacine!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "test456@gmail.com", "password": "pwd123"})
    new_user = schema.UserResponse(**res.json())
    assert new_user.email == "test456@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ("wrongemail@gmail.com", "pwd123", 403),
    ("test456@gmail.com", "wrongCredential", 403),
    ("wrongemail@gmail.com", "wrongCredential", 403),
    (None, "wrongCredential", 422),
    ("wrongemail@gmail.com", None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json()['detail'] == "Invalid Credentials"