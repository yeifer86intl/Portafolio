"""
import unittest

import requests


def login(username, password):
    url = f"http://0.0.0.0:8000/login"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "",
        "username": username,
        "password": password,
        "scope": "",
        "client_id": "",
        "client_secret": "",
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None


def test_login():
    token = login("admin@example.com", "admin")
    assert token is not None


def test_predict():
    token = login("admin@example.com", "admin")
    files = [("file", ("dog.jpeg", open("tests/dog.jpeg", "rb"), "image/jpeg"))]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        "http://localhost:8000/model/predict",
        headers=headers,
        files=files,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["prediction"] == "Eskimo_dog"
    assert data["score"] == 0.9346
"""

import unittest
import requests


class TestAPIIntegration(unittest.TestCase):

    BASE_URL = "http://localhost:8000"  # Asegúrate de que esta URL sea la correcta

    def login(self, username, password):
        url = f"{self.BASE_URL}/login"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "",
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        response = requests.post(url, headers=headers, data=data)
        self.assertEqual(response.status_code, 200, f"Login failed: {response.text}")
        return response.json().get("access_token")

    def test_login(self):
        token = self.login("admin@example.com", "admin")
        self.assertIsNotNone(token, "Token should not be None after login")

    def test_predict(self):
        token = self.login("admin@example.com", "admin")
        self.assertIsNotNone(token, "Token should not be None after login")

        files = [("file", ("dog.jpeg", open("tests/dog.jpeg", "rb"), "image/jpeg"))]
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{self.BASE_URL}/model/predict",
            headers=headers,
            files=files,
        )
        self.assertEqual(response.status_code, 200, f"Prediction failed: {response.text}")

        data = response.json()
        self.assertTrue(data["success"], "Prediction was not successful")
        self.assertEqual(data["prediction"], "Eskimo_dog", "Wrong prediction result")
        self.assertAlmostEqual(data["score"], 0.9346, places=4, msg="Prediction score mismatch")


if __name__ == "__main__":
    unittest.main()
