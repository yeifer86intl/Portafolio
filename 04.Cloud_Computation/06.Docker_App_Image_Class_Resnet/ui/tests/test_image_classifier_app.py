import os
import unittest
from io import BytesIO
from unittest import mock

import app.image_classifier_app as ui_app
import requests
from PIL import Image

path_tests = os.path.dirname(os.path.abspath(__file__))


class TestMLService(unittest.TestCase):
    def setUp(self):
        self.token = "dummy_token"
        self.image_file = Image.open(path_tests + "/dog.jpeg")
        self.uploaded_file = mock.MagicMock(spec=BytesIO)
        self.uploaded_file.getvalue.return_value = BytesIO()
        self.uploaded_file.name = "dog.jpeg"
        self.image_file.save(self.uploaded_file, format="JPEG")
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_login_success(self):
        expected_token = "dummy_token"
        response_data = {"access_token": expected_token}
        with mock.patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = response_data

            token = ui_app.login("username", "password")

            headers = {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            self.assertEqual(token, expected_token)
            mock_post.assert_called_once_with(
                ui_app.API_BASE_URL + "/login",
                headers=headers,
                data={
                    "grant_type": "",
                    "username": "username",
                    "password": "password",
                    "scope": "",
                    "client_id": "",
                    "client_secret": "",
                },
            )

    def test_login_failure(self):
        with mock.patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 401

            token = ui_app.login("username", "password")

            headers = {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            self.assertIsNone(token)
            mock_post.assert_called_once_with(
                ui_app.API_BASE_URL + "/login",
                headers=headers,
                data={
                    "grant_type": "",
                    "username": "username",
                    "password": "password",
                    "scope": "",
                    "client_id": "",
                    "client_secret": "",
                },
            )

    def test_predict_success(self):
        expected_response = {"prediction": "Eskimo_dog", "score": 0.9346}
        with mock.patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = expected_response

            response = ui_app.predict(self.token, self.uploaded_file)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), expected_response)
            mock_post.assert_called_once_with(
                ui_app.API_BASE_URL + "/model/predict",
                files={
                    "file": (self.uploaded_file.name, self.uploaded_file.getvalue())
                },
                headers=self.headers,
            )

    def test_predict_failure(self):
        with mock.patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 500

            response = ui_app.predict(self.token, self.uploaded_file)

            self.assertEqual(response.status_code, 500)
            mock_post.assert_called_once_with(
                ui_app.API_BASE_URL + "/model/predict",
                files={
                    "file": (self.uploaded_file.name, self.uploaded_file.getvalue())
                },
                headers=self.headers,
            )

    def test_send_feedback_success(self):
        expected_response = {"status": "success"}
        feedback = "This is a feedback"
        score = 0.9346
        prediction = "Eskimo_dog"
        image_file_name = "dog.jpeg"
        with mock.patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 201
            mock_post.return_value.json.return_value = expected_response

            response = ui_app.send_feedback(
                self.token, feedback, score, prediction, image_file_name
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json(), expected_response)
            mock_post.assert_called_once_with(
                ui_app.API_BASE_URL + "/feedback",
                json={
                    "feedback": feedback,
                    "score": score,
                    "predicted_class": prediction,
                    "image_file_name": image_file_name,
                },
                headers=self.headers,
            )

    def test_send_feedback_failure(self):
        feedback = "This is a feedback"
        score = 0.9346
        prediction = "Eskimo_dog"
        image_file_name = "dog.jpeg"
        with mock.patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 500

            response = ui_app.send_feedback(
                self.token, feedback, score, prediction, image_file_name
            )

            self.assertEqual(response.status_code, 500)
            mock_post.assert_called_once_with(
                ui_app.API_BASE_URL + "/feedback",
                json={
                    "feedback": feedback,
                    "score": score,
                    "predicted_class": prediction,
                    "image_file_name": image_file_name,
                },
                headers=self.headers,
            )


if __name__ == "__main__":
    unittest.main()
