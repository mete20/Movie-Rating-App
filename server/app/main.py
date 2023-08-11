from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import List, Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from sqlalchemy.orm import Session
import secrets
import os
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError


app = FastAPI()

# OAuth settings

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None

if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up OAuth

config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    cleint_kwargs={'scope': 'openid email profile'},
)

#Set up middleware to read the request session
SECRET_KEY= os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise BaseException('Missing SECRET_KEY')
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.get('/')
def public(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
    return HTMLResponse('<a href=/login>Login</a>')

@app.route('/logout/')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@app.route('/login/')
async def login(request: Request):
    redirect_uri = request.url_for('auth')  # This creates the url for our /auth endpoint
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth/')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    user_data = await oauth.google.parse_id_token(request, access_token)
    request.session['user'] = dict(user_data)
    return RedirectResponse(url='/')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Not Found",
                "message": f"User with email: '{user.email}' already registered.",
            },
        )
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error code:": 404,
                "error description": "Not Found",
                "message": f"User with ID: '{user_id}' not found",
            },
        )
    return db_user


@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate,
    db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_name(db, name= movie.Name)
    if db_movie:
        raise HTTPException(
        
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Movie already exist",
                "message": f"Movie with ID: '{rating.movie_id}' created before.",
            },
        )
    return crud.create_movie(db=db, movie=movie)


@app.get("/movies/", response_model=List[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_user(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error code:": 404,
                "error description": "Not Found",
                "message": f"Movie with ID: '{movie_id}' could not be found",
            },
        )
    return db_movie


@app.post("/ratings/", response_model=schemas.Rating)
def create_rating(rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id = rating.user_id)
    db_movie = crud.get_movie(db, rating.movie_id)

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error code:": 404,
                "error description": "Not Found",
                "message": f"User with ID: '{rating.user_id}' could not be found",
            },
        )
    
    if db_movie is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error code:": 404,
                "error description": "Not Found",
                "message": f"Movie with ID: '{rating.movie_id}' could not be found",
            },
        )
    
    is_rating_exist = crud.is_rating_exist(db, rating.user_id, rating.movie_id)
    
    if is_rating_exist:
        raise HTTPException(
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Rating already exist",
                "message": f"User with ID: '{rating.user_id}' has voted the movie '{rating.movie_id}' before.",
            },
        )
        return crud.create_rating(db, rating)



