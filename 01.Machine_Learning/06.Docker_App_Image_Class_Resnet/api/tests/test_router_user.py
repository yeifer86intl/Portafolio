from unittest.mock import MagicMock

import pytest
from app import db
from app.auth.jwt import create_access_token
from app.user.models import User
from app.user.schema import User as UserSchema
from httpx import AsyncClient
from main import app
from sqlalchemy.orm import Session


@pytest.mark.asyncio
async def test_all_users():
    mock_session = MagicMock(spec=Session)
    mock_user = User(
        name="John Doe", email="john@yahoo.com", password="123456", kwargs={"id": 1}
    )

    mock_session.query(User).all.return_value = [mock_user]

    app.dependency_overrides[db.get_db] = lambda: mock_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "john@gmail.com"})
        response = await ac.get(
            "/user/", headers={"Authorization": f"Bearer {user_access_token}"}
        )
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["name"] == "John Doe"


@pytest.mark.asyncio
async def test_create_user_registration_success():
    mock_session = MagicMock(spec=Session)
    request = UserSchema(
        id=0, name="John Doe", email="john@gmail.com", password="123456"
    )

    mock_session.query(User).filter.return_value.first.return_value = None

    app.dependency_overrides[db.get_db] = lambda: mock_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/user/", json=request.dict())

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_user_registration_fails():
    mock_session = MagicMock(spec=Session)
    mock_user = User(id=0, name="John Doe", email="john@gmail.com", password="123456")
    request = UserSchema(
        id=0, name="John Doe", email="john@gmail.com", password="123456"
    )

    mock_session.query(User).filter.return_value.first.return_value = mock_user

    app.dependency_overrides[db.get_db] = lambda: mock_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/user/", json=request.dict())

    assert response.status_code == 400
