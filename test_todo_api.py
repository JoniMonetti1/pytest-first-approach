import requests

ENDPOINT = "https://todo.pixegami.io/"

response = requests.get(ENDPOINT)
print(response)

data = response.json()
status_code = response.status_code
print(status_code)
print(data)

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    payload = {
        "content": "Buy groceries",
        "user_id": "user_12345",
        "task_id": "task_67890",
        "is_done": False,
    }
    create_task_response = requests.put(ENDPOINT + "/create-task", json=payload)
    data = create_task_response.json()
    print(data)

    assert create_task_response.status_code == 200

    task_id = data["task"]["task_id"]
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")

    assert get_task_response.status_code == 200
    task_data = get_task_response.json()
    print(task_data)

    assert task_data["content"] == payload["content"]
    assert task_data["user_id"] == payload["user_id"]

def test_can_update_task():
    # Create a task first
    # update the task
    # get the validate task
    payload = new_task_payload()

    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # update the task
    update_payload = {
        "content": "Buy groceries and cook dinner updated",
        "user_id": payload["user_id"],
        "task_id": task_id,
        "is_done": True,
    }

    updated_task_response = update_task(update_payload)
    assert updated_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == update_payload["content"]
    assert get_task_data["is_done"] == update_payload["is_done"]



def create_task(payload: dict):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def get_task(task_id: str):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def update_task(payload: dict):
    return requests.put(ENDPOINT + f"/update-task", json=payload)

def new_task_payload():
    return {
        "content": "Buy groceries and cook dinner",
        "user_id": "user_12345",
        "task_id": "task_67890",
        "is_done": False,
    }
