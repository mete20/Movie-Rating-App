from base64 import urlsafe_b64encode
import os

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI
from fastapi import Request
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from .config import Config as cf
from app.jwt import create_token
from app.jwt import CREDENTIALS_EXCEPTION
from app.jwt import is_admin
from starlette.applications import Starlette

# Create the auth app
auth_app = Starlette()

# OAuth settings
GOOGLE_CLIENT_ID = cf.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = cf.GOOGLE_CLIENT_SECRET
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    id_token_signing_alg_values_supported=["HS256", "RS256"],
    jwks={
        "keys": [{
            "kid": "AIzaSyCNmCAf8HqRyOvXgRE4ol5_9W4v90G_vBE",
            "kty": "oct",
            "alg": "RS256",
        }]
    },
    client_kwargs={'scope': 'openid email profile'},
)

# Set up the middleware to read the request session
SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
auth_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Frontend URL:
FRONTEND_URL = os.environ.get('FRONTEND_URL') or 'http://localhost:8000/token'


@auth_app.route('/login')
async def login(request: Request):
    redirect_uri = FRONTEND_URL  # This creates the url for our /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_app.route('/token')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
        userinfo = access_token['userinfo']
    except OAuthError:
        raise CREDENTIALS_EXCEPTION
    return JSONResponse({'result': True, 'access_token': create_token(userinfo['email'])})
   
        