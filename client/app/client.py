
import requests
import os
import time
# Configuration from environment variables
SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:8000")

def create_user(user_data):
    try:
        response = requests.post(f"{SERVER_URL}/users/", json=user_data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to create user. Server Response: {response.text}", "status_code": response.status_code}
    except requests.RequestException as e:
        return {"error": str(e)}

def get_user_by_id(user_id):
    try:
        response = requests.get(f"{SERVER_URL}/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch user with ID {user_id}", "status_code": response.status_code}
    except requests.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Sample usage
    #time.sleep(20)
    new_user = {"email": "john@example.com", "password": "deneme"}
    print(create_user(new_user))
    print(get_user_by_id(1))
