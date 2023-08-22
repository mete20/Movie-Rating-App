from base64 import urlsafe_b64encode
import os
from datetime import datetime
from fastapi import FastAPI
from fastapi import Request
from starlette.applications import Starlette
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from app.config import Config as cf
from app.authentication.jwt import create_token
from app.authentication.jwt import CREDENTIALS_EXCEPTION
from app.authentication.jwt import create_refresh_token
from app.authentication.jwt import decode_token
# Create the auth app
auth_app = FastAPI()

# OAuth settings
GOOGLE_CLIENT_ID = cf.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = cf.GOOGLE_CLIENT_SECRET
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up OAuth
API_SECRET_KEY = os.environ.get('API_SECRET_KEY')
config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    id_token_signing_alg_values_supported=["HS256", "RS256"],
    jwks={
        "keys": [{
            "kid": API_SECRET_KEY,
            "kty": "oct",
            "alg": "RS256",
        }]
    },
    client_kwargs={'scope': 'openid email profile'},
)
SECRET_KEY = os.environ.get('SECRET_KEY')
FRONTEND_URL = os.environ.get('FRONTEND_URL')
auth_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@auth_app.route('/login')
async def login(request: Request):
    redirect_uri = FRONTEND_URL
    return await oauth.google.authorize_redirect(request, redirect_uri)

async def logout(request: Request):
    request.session.clear()
    return JSONResponse({'result': True, 'message': 'Logged out successfully'})

@auth_app.route('/token', name='token')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
        userinfo = access_token['userinfo']
    except OAuthError:
        raise CREDENTIALS_EXCEPTION
    return JSONResponse({
            'result': True,
            'access_token': create_token(userinfo['email']),
            'refresh_token': create_refresh_token(userinfo['email']),
        })
   
@auth_app.post('/refresh')
async def refresh(request: Request):
    try:
        # Only accept post requests
        if request.method == 'POST':
            form = await request.json()
            if form.get('grant_type') == 'refresh_token':
                token = form.get('refresh_token')
                payload = decode_token(token)
                # Check if token is not expired
                # if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
                email = payload.get('sub')
                    # Validate email
                    # Create and return token
                return JSONResponse({'result': True, 'access_token': create_token(email)})

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION       