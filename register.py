import requests

url = "http://localhost:8000/users/register"
data = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "secret123"
}
response = requests.post(url, json=data)
print("Status code:", response.status_code)
print("Response:", response.json())
