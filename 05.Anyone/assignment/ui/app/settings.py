import os

API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", 8000)
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"
