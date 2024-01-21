from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapp.db.schema import Base, User
from fastapp.auth.password import get_password_hash
from fastapp.db.db import get_db
from fastapp.main import get_application

import pytest

# MAYBE PUT OS ENV VARS HERE

app = get_application()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

db = next(override_get_db())
db.add(User(name="admin", email="admin", password=get_password_hash("admin"), is_active=True, is_admin=True))
db.commit()

app.dependency_overrides[get_db] = override_get_db

fastapp_client = TestClient(app)

@pytest.fixture()
def client():
    return fastapp_client

def pytest_configure():
    pytest.data = {'reset_token': None}