from datetime import datetime
from fastapi import FastAPI
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth
from app.config import Config as cf
from app.authentication.jwt import create_token, CREDENTIALS_EXCEPTION, create_refresh_token, decode_token
from app.crud.crud_user import get_user_by_email, create_user
from app.schemas.schema_user import UserCreate
from .jwt import is_admin
from app.db.database import get_db

# OAuth settings
GOOGLE_CLIENT_ID = cf.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = cf.GOOGLE_CLIENT_SECRET
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Create the auth app
auth_app = FastAPI()

# Set up OAuth
config = Config()
oauth = OAuth(config)

oauth.register(
    name='google',
    server_metadata_url=
    'https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

auth_app.add_middleware(SessionMiddleware, secret_key=cf.SECRET_KEY)    

@auth_app.route('/login')
async def login(request: Request):
    redirect_uri = cf.FRONTEND_URL
    return await oauth.google.authorize_redirect(request, redirect_uri)


async def logout(request: Request):
    request.session.clear()
    return JSONResponse({
        'result': True, 'message': 'Logged out successfully'
        })


@auth_app.route('/token', name='token')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
        userinfo = access_token['userinfo']
        user_email = userinfo['email']
        
        db = next(get_db())
        if get_user_by_email(db, user_email):
            print("Hello", user_email)
        else:
            print("not registered")
            user_role: str = "user"
            if is_admin(user_email):
                print("role should be admin")
                user_role = "admin"
            new_user = UserCreate(email=user_email, role=user_role)
            create_user(db, new_user)
        
    except Exception as e:
        print(e)
        raise CREDENTIALS_EXCEPTION
    return JSONResponse({
            'result': True,
            'access_token': create_token(user_email),
            'refresh_token': create_refresh_token(user_email),
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
                if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
                    email = payload.get('sub')
                    # Validate email
                    # Create and return token
                    return JSONResponse({
                        'result': True, 'access_token': create_token(email)
                        })

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION       

