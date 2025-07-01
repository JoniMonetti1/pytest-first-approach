import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope='session')
def auth_token():
    username = os.getenv('TEST_USERNAME')
    password = os.getenv('TEST_PASSWORD')
    api_base_url = os.getenv('API_BASE_URL')

    print(f"Username: {username}")
    print(f"Password: {'*' * len(password) if password else None}")
    print(f"API URL: {api_base_url}")

    auth_response = requests.post(
        api_base_url + 'auth/login',
        data={
            'grant_type': 'password',
            'username': username,
            'password': password,
            'scope': '',
            'client_id': 'string',
            'client_secret': ''
        },
        headers= {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )

    print(f"Response status: {auth_response.status_code}")
    print(f"Response body: {auth_response.text}")

    auth_response.raise_for_status()

    token = auth_response.json().get('access_token')
    yield token