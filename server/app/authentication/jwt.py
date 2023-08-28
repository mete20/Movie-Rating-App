import os
from datetime import datetime
from datetime import timedelta
from typing import Annotated
import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

http_bearer = HTTPBearer()

# Helper to read numbers using var envs
def cast_to_number(id):
    temp = os.environ.get(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None


# Configuration
API_SECRET_KEY = os.environ.get('API_SECRET_KEY') or None
if API_SECRET_KEY is None:
    raise BaseException('Missing API_SECRET_KEY env var.')
API_ALGORITHM = os.environ.get('API_ALGORITHM') or 'HS256'
API_ACCESS_TOKEN_EXPIRE_MINUTES = cast_to_number('API_ACCESS_TOKEN_EXPIRE_MINUTES') or 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30


# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


# Create token internal function
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt


# Create token for an email
def create_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': email}, expires_delta=access_token_expires)
    return access_token


def is_admin(email):
    domain = email.split('@')[1]
    return domain == 'ku.edu.tr'

async def is_admin_dep(token: Annotated[str, HTTPAuthorizationCredentials] = Depends(http_bearer)):
    email = await get_current_user_email(token)
    try:
        domain = email.split('@')[1]
    except IndexError as e:
        raise HTTPException(
            status_code=422,
            
            detail="Incorrect email input. {e}"
        )
    if (domain == 'ku.edu.tr'):
        return True
    else:
        raise HTTPException(
            status_code=403,
            detail="You don't have the necessary permissions."
        )


async def get_current_user_email(token: Annotated[str, HTTPAuthorizationCredentials] = Depends(http_bearer)):
    try:
        payload = jwt.decode(token.credentials, API_SECRET_KEY, algorithms=[API_ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return email


def create_refresh_token(email):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={'sub': email}, expires_delta=expires)

def decode_token(token):
    return jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])

async def get_current_user_token(token: str = Depends(http_bearer)):
    _ = await get_current_user_email(token)
    return token

