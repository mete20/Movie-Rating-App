from base64 import urlsafe_b64encode
import os

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI
from fastapi import Request
from starlette.config import Config
from starlette.requests import Request
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

config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
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

@auth_app.route('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        data = json.dumps(user)
        return JSONResponse(data)
    return JSONResponse({"user": "Not Found!"})


@auth_app.route('/login')
async def login(request: Request):
    redirect_uri = request.url_for('token')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_app.route('/token', name='token')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
        userinfo = access_token['userinfo']
    except OAuthError:
        raise CREDENTIALS_EXCEPTION
    return JSONResponse({'result': True, 'access_token': create_token(userinfo['email'])})
   
        