def test_create_task(client):
    # Register and login
    client.post("/users/register", json={"email": "task@example.com", "username": "taskuser", "password": "pass"})
    login = client.post("/users/token", data={"username": "taskuser", "password": "pass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Do it"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert not data["completed"]