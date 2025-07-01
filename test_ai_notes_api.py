import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("API_BASE_URL")

def test_can_list_users(auth_token):
    headers = {
        'Authorization': 'Bearer ' + auth_token
    }

    response = requests.get(
        BASE_URL + 'user',
        headers=headers
    )

    list_of_users = response.json()

    assert response.status_code == 200
    assert len(list_of_users) > 0

