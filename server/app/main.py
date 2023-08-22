from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from .authentication.jwt import CREDENTIALS_EXCEPTION
from .authentication.jwt import get_current_user_token
from .authentication.jwt import get_current_user_email
from .authentication.auth import auth_app
from app.api import api_app
from .crud import crud_movie, crud_rating, crud_user
from .schemas import schema_movie, schema_rating, schema_user
from .db.database import SessionLocal
from typing import List

app = FastAPI()
app.mount('/auth', auth_app)
app.mount('/api', api_app)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
@app.get('/')
async def root():
    return HTMLResponse('<body><a href="/auth/login">Log In</a></body>')
@app.get('/logout')
def logout(token: str = Depends(get_current_user_token)):
    return JSONResponse({'result': True})
@app.get('/token')
async def token(request: Request):
    return HTMLResponse('''
                <script>
                function send(){
                    var req = new XMLHttpRequest();
                    req.onreadystatechange = function() {
                        if (req.readyState === 4) {
                            console.log(req.response);
                            if (req.response["result"] === true) {
                                window.localStorage.setItem('jwt', req.response["access_token"]);
                                window.localStorage.setItem('refresh', req.response["refresh_token"]);
                            }
                        }
                    }
                    req.withCredentials = true;
                    req.responseType = 'json';
                    req.open("get", "/auth/token?"+window.location.search.substr(1), true);
                    req.send("");

                }
                </script>
                <button onClick="send()">Get FastAPI JWT Token</button>

                <button onClick='fetch("http://localhost:8000/api/").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Unprotected API
                </button>
                <button onClick='fetch("http://localhost:8000/api/protected").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API without JWT
                </button>
                <button onClick='fetch("http://localhost:8000/api/protected",{
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                }).then((r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API wit JWT
                </button>

                <button onClick='fetch("http://localhost:8000/logout",{
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                }).then((r)=>r.json()).then((msg)=>{
                    console.log(msg);
                    if (msg["result"] === true) {
                        window.localStorage.removeItem("jwt");
                    }
                    });'>
                Logout
                </button>

                <button onClick='fetch("http://localhost:8000/auth/refresh",{
                    method: "POST",
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                    body:JSON.stringify({
                        grant_type:\"refresh_token\",
                        refresh_token:window.localStorage.getItem(\"refresh\")
                        })
                }).then((r)=>r.json()).then((msg)=>{
                    console.log(msg);
                    if (msg["result"] === true) {
                        window.localStorage.setItem("jwt", msg["access_token"]);
                    }
                    });'>
                Refresh
                </button>

            ''')
    
    
@app.post("/users/", response_model=schema_user.User)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user_email)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Not Found",
                "message": f"User with email: '{user.email}' already registered.",
            },
        )
    return crud_user.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schema_user.User])
def read_users(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schema_user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
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

###############

@app.post("/movies/", response_model=schema_movie.Movie)
def create_movie(movie: schema_movie.MovieCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user_email)):
    db_movie = crud_movie.get_movie_by_name(db, name= movie.Name)
    if db_movie:
        raise HTTPException(
        
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Movie already exist",
                "message": f"Movie with ID: '{movie.movie_id}' created before.",
            },
        )
    return crud_movie.create_movie(db=db, movie=movie)


@app.get("/movies/", response_model=List[schema_movie.Movie])
def read_movies(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    movies = crud_movie.get_movies(db, skip=skip, limit=limit)
    return movies

@app.get("/movies/{movie_id}", response_model=schema_movie.Movie)
def read_user(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud_movie.get_movie(db, movie_id=movie_id)
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

############

@app.post("/ratings/", response_model=schema_rating.Rating)
def create_rating(rating: schema_rating.RatingCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id = rating.user_id)
    db_movie = crud_movie.get_movie(db, rating.movie_id)

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
    
    is_rating_exist = crud_rating.is_rating_exist(db, rating.user_id, rating.movie_id)
    
    if is_rating_exist:
        raise HTTPException(
            status_code=400,
            detail={
                "error code:": 400,
                "error description": "Rating already exist",
                "message": f"User with ID: '{rating.user_id}' has voted the movie '{rating.movie_id}' before.",
            },
        )
    return crud_rating.create_rating(db, rating)



