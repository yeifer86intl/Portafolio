from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from app.auth.jwt import get_current_user
from app.model.schema import PredictResponse
from fastapi import UploadFile
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_predict():
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test_image.png"
    mock_file.read = AsyncMock(return_value=b"fake-image-data")

    mock_user = MagicMock()
    mock_user.id = 1

    mock_current_user = MagicMock()
    mock_current_user.return_value = "testtoken"

    app.dependency_overrides[get_current_user] = lambda: mock_current_user

    with patch("app.model.router.utils.get_file_hash", return_value="fakehash123"):
        with patch(
            "app.model.router.model_predict", new_callable=AsyncMock
        ) as mock_model_predict:
            with patch("app.model.router.os.path.exists", return_value=False):
                mock_model_predict.return_value = ("cat", 0.95)
                with patch("builtins.open", new_callable=MagicMock):
                    async with AsyncClient(app=app, base_url="http://test") as ac:
                        response = await ac.post(
                            "/model/predict",
                            files={
                                "file": (
                                    "test_image.png",
                                    mock_file.read.return_value,
                                    "image/png",
                                )
                            },
                            headers={"Authorization": "Bearer testtoken"},
                        )

                        assert response.status_code == 200

                        response_data = response.json()
                        assert response_data["success"] is True
                        assert response_data["prediction"] == "cat"
                        assert response_data["score"] == 0.95
                        assert response_data["image_file_name"] == "fakehash123"


@pytest.mark.asyncio
async def test_predict_fails_bad_extension():
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test_image.png"
    mock_file.read = AsyncMock(return_value=b"fake-image-data")

    mock_user = MagicMock()
    mock_user.id = 1

    mock_current_user = MagicMock()
    mock_current_user.return_value = "testtoken"

    app.dependency_overrides[get_current_user] = lambda: mock_current_user

    with patch("app.model.router.utils.get_file_hash", return_value="fakehash123"):
        with patch(
            "app.model.router.model_predict", new_callable=AsyncMock
        ) as mock_model_predict:
            with patch("app.model.router.os.path.exists", return_value=False):
                mock_model_predict.return_value = ("cat", 0.95)
                with patch("builtins.open", new_callable=MagicMock):
                    async with AsyncClient(app=app, base_url="http://test") as ac:
                        response = await ac.post(
                            "/model/predict",
                            files={
                                "file": (
                                    "test_image.pdf",
                                    mock_file.read.return_value,
                                    "image/png",
                                )
                            },
                            headers={"Authorization": "Bearer testtoken"},
                        )

                        assert response.status_code == 400
                        assert response.json() == {
                            "detail": "File type is not supported."
                        }
