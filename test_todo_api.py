import requests
import uuid

ENDPOINT = "https://todo.pixegami.io/"

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

    assert create_task_response.status_code == 200

    task_id = data["task"]["task_id"]
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")

    assert get_task_response.status_code == 200
    task_data = get_task_response.json()

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

def test_can_list_tasks():
    #Crete n tasks
    n = 5
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # List tasks
    user_id = payload["user_id"]
    list_tasks_response = list_tasks(user_id)
    assert list_tasks_response.status_code == 200
    data = list_tasks_response.json()
    assert len(data["tasks"]) == n

def test_can_delete_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404, "Task should be deleted and not found"




def create_task(payload: dict):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def get_task(task_id: str):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def list_tasks(user_id: str):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def update_task(payload: dict):
    return requests.put(ENDPOINT + f"/update-task", json=payload)

def delete_task(task_id: str):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False,
    }
