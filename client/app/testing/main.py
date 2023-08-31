from datetime import datetime, timedelta
import requests
import jwt
import os

# Configurations
SERVER_URL = "http://web:8000"
AUTH_ROUTE = "/auth/token"
MOVIES_ROUTE = "/movies"
API_SECRET_KEY = os.environ['API_SECRET_KEY']
API_ALGORITHM = os.environ['API_ALGORITHM']


def mock_authorize(email: str):
    """
    Mock the authorization process for a given email.
    :param email: The email to be authorized.
    :return: A dictionary containing the access token.
    """
    # This function directly generates tokens without actual authentication for testing purposes.
    expire_time = datetime.utcnow() + timedelta(minutes=15)
    user_info = {'sub': email, 'exp': expire_time}
    access_token = jwt.encode(user_info, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return {
        'access_token': access_token,
    }

def mock_authenticate():
    # This function simulates the authentication process by directly mocking the authorization for a given email.
    # For this mock, the email "test@ku.edu.tr" is used for testing purposes.
    tokens = mock_authorize("test@ku.edu.tr")
    return tokens.get("access_token")

# Get Movies Function
def get_movies(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{SERVER_URL}{MOVIES_ROUTE}", headers=headers)
    return response.json()

def create_movie(token: str, movie: dict) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{SERVER_URL}{MOVIES_ROUTE}", headers=headers, json=movie)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def get_movie_by_id(token: str, movie_id: int) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{SERVER_URL}{MOVIES_ROUTE}/{movie_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
        
def delete_movie(token: str, movie_id: int) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{SERVER_URL}{MOVIES_ROUTE}/{movie_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example usage
if __name__ == "__main__":
    token = mock_authenticate()
    movies = get_movies(token)
    print(movies)

