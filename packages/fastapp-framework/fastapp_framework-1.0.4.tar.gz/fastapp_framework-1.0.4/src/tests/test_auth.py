import pytest
import base64
from fastapi.testclient import TestClient

# import email.mime.multipart.MIMEMultipart
from . import get_token
from fastapp.core.mail import fastmail


# def test_unauthorized_request(client: TestClient):
#     response = client.get("/api/v1/auth/users/me")
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}


def test_create_user_unauthorized(client: TestClient):
    response = client.post(
        "/api/v1/auth/user/",
        json={
            "name": "user1", "email": "user1@users.com",
            "password": "password", "is_active": True, "is_superuser": False
        }
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_create_user_bad_authorization(client: TestClient):
    token = get_token(client, "admin", "admin")
    response = client.post(
        "/api/v1/auth/user/",
        json={
            "name": "user1", "email": "user1@users.com",
            "password": "password", "is_active": True, "is_superuser": False
        },
        headers={"Authorization": f"Bearer {token[:-4]+'1234'}"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_create_user_authorized(client: TestClient):
    token = get_token(client, "admin", "admin")
    response = client.post(
        "/api/v1/auth/user/",
        json={
            "name": "user1", "email": "user1@users.com",
            "password": "password", "is_active": True, "is_superuser": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == {
        'email': 'user1@users.com',
        'is_active': True,
        'is_admin': False,
        'name': 'user1',
        'first': None,
        'last': None
    }

    token = get_token(client, "user1", "password")
    response = client.get(
        "/api/v1/auth/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_create_user_duplicate(client: TestClient):
    token = get_token(client, "admin", "admin")
    response = client.post(
        "/api/v1/auth/user/",
        json={
            "name": "user1", "email": "user1@users.com",
            "password": "password", "is_active": True, "is_superuser": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Username or email already exists"}


def test_create_user_non_admin(client: TestClient):
    token = get_token(client, "user1", "password")
    response = client.post(
        "/api/v1/auth/user/",
        json={
            "name": "user2", "email": "user2@users.com",
            "password": "password", "is_active": True, "is_superuser": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "User cannot access requested resource"}


def test_create_non_active_user(client: TestClient):
    token = get_token(client, "admin", "admin")
    response = client.post(
        "/api/v1/auth/user/",
        json={
            "name": "user2", "email": "user2@users.com",
            "password": "password", "is_active": False, "is_superuser": False
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    token = get_token(client, "user2", "password")
    response = client.get(
        "/api/v1/auth/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Inactive user"}


def test_request_pass_reset(client: TestClient):
    fastmail.config.SUPPRESS_SEND = True
    with fastmail.record_messages() as outbox:
        response = client.get(
            "/api/v1/auth/user/reset-password/?email=user1@users.com",
        )

        assert response.status_code == 200
        assert response.json() == {}

        assert len(outbox) == 1

        for i in outbox[0].walk():
            if i.get_content_type() == "text/html":
                html = base64.b64decode(i.get_payload())
                start = html.find(b"?token=")
                end = html.find(b'"', start)

                assert start != -1
                assert end != -1
                
                token = html[start+7:end].decode("utf-8")

                assert len(token) > 0

                pytest.data["reset_token"] = token

                break


def test_do_pass_reset(client: TestClient):
    token = pytest.data["reset_token"]
    response = client.post(
        "/api/v1/auth/user/do-reset-password/",
        json={
            "token": token,
            "password": "newpassword"
        }
    )

    assert response.status_code == 200
    assert response.json() == {}

    access_token = get_token(client, "user1", "newpassword")

    response = client.get(
        "/api/v1/auth/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
