import os
from fastapi.testclient import TestClient

if(os.path.isfile("test.db")):
    os.remove("test.db")

os.environ["SECRET_KEY"] = "mysupersecretkey"
os.environ["MAIL_USERNAME"] = "null"
os.environ["MAIL_PASSWORD"] = "null"
os.environ["MAIL_FROM"] = "null@null.com"
os.environ["MAIL_FROM_NAME"] = "null"
os.environ["MAIL_NAME"] = "null"
os.environ["MAIL_SERVER"] = "null"


def get_token(client: TestClient, username: str, password: str):
    response = client.post(
        "/api/v1/auth/token",
        data={"username": username, "password": password},
    )
    return response.json()["access_token"]