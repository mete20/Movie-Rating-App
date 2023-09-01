from datetime import datetime, timedelta
import requests
import jwt
import os

# Configurations
SERVER_URL = "http://web:8000"
AUTH_ROUTE = "/auth/token"
MOVIES_ROUTE = "/movies"
USERS_ROUTE = "/users"
API_SECRET_KEY = os.environ['API_SECRET_KEY']
API_ALGORITHM = os.environ['API_ALGORITHM']

#Authentication and Authorization
def mock_authorize(email: str):
    """
    Mock the authorization process for a given email.
    :param email: The email to be authorized.
    :return: A dictionary containing the access token.
    """
    expire_time = datetime.utcnow() + timedelta(minutes=15)
    user_info = {'sub': email, 'exp': expire_time}
    access_token = jwt.encode(user_info, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return {
        'access_token': access_token,
    }


def mock_authenticate_admin():
    tokens = mock_authorize("test@ku.edu.tr")
    return tokens.get("access_token")


def mock_authenticate_user():
    tokens = mock_authorize("test@gmail.com")
    return tokens.get("access_token")


# Movie Requests
def get_movies():
    response = requests.get(f"{SERVER_URL}{MOVIES_ROUTE}")
    return response.json()


def create_movie(token: str, movie: dict) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{SERVER_URL}{MOVIES_ROUTE}", headers=headers, json=movie)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_movie_by_id(movie_id: int) -> dict:
    response = requests.get(f"{SERVER_URL}{MOVIES_ROUTE}/{movie_id}")
    
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

# User Requests

def create_user(token: str, user: dict) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{SERVER_URL}{USERS_ROUTE}/", headers=headers, json=user)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_users(token: str) -> list:
    response = requests.get(f"{SERVER_URL}{USERS_ROUTE}/")
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_user_by_id(token: str, user_id: int) -> dict:
    response = requests.get(f"{SERVER_URL}{USERS_ROUTE}/{user_id}")
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def delete_user(token: str, user_id: int) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{SERVER_URL}{USERS_ROUTE}/{user_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
