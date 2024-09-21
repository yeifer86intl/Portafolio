import unittest

import requests


def login(username, password):
    url = f"http://localhost:8000/login"
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



