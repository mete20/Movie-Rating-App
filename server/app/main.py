from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
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
from app.routers import router_user, router_movie, router_rating 

app = FastAPI()
app.mount('/auth', auth_app)
app.mount('/api', api_app)
app.include_router(router_user.router)
app.include_router(router_movie.router)
app.include_router(router_rating.router)

origins = [
    "http://localhost:8001", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


    



