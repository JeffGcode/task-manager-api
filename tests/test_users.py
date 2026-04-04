def test_register(client):
    response = client.post(
        "/users/register",
        json={"email": "test@example.com", "username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

def test_login(client):
    # First register
    client.post("/users/register", json={"email": "login@example.com", "username": "loginuser", "password": "pass"})
    response = client.post(
        "/users/token",
        data={"username": "loginuser", "password": "pass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_me(client):
    # Register and login to get token
    client.post("/users/register", json={"email": "me@example.com", "username": "meuser", "password": "pass"})
    login_resp = client.post("/users/token", data={"username": "meuser", "password": "pass"})
    token = login_resp.json()["access_token"]
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "meuser"