import uuid

import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("API_BASE_URL")

def test_can_list_users(auth_token):
    headers = {
        'Authorization': 'Bearer ' + auth_token
    }

    response = get_users(headers)

    list_of_users = response.json()

    assert response.status_code == 200
    assert len(list_of_users) > 0

def test_can_get_user_by_id(auth_token):
    headers = {
        'Authorization': 'Bearer ' + auth_token
    }

    list_response = get_users(headers)
    assert list_response.status_code == 200

    list_of_users = list_response.json()
    assert len(list_of_users) > 0

    user_id = list_of_users[0]['id']
    username = list_of_users[0]['username']


    response = get_user(user_id, headers)

    assert response.status_code == 200
    user = response.json()
    assert user['id'] == user_id
    assert user['username'] == username


def test_can_create_user(auth_token):
        headers = {
            'Authorization': 'Bearer ' + auth_token,
            'Content-Type': 'application/json'
        }

        payload = new_user_payload()

        response = create_user(payload, headers)
        assert response.status_code == 201
        user = response.json()
        assert user['username'] == payload['username']
        assert user['email'] == payload['email']



def new_user_payload():
    username = f"test_username_{uuid.uuid4().hex}"
    return {
        "username": username,
        "email": f"{username}@gmail.com",
        "password": "123456aA"
    }

def create_user(payload: dict, headers: dict):
    return requests.post(BASE_URL + "/user", headers=headers, json=payload)

def get_user(user_id: int, headers: dict):
    return requests.get(BASE_URL + f"/user/{user_id}", headers=headers)

def get_users(headers: dict):
    return requests.get(BASE_URL + "/user", headers=headers)