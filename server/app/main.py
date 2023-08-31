from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .authentication.auth import auth_app
from app.api import api_app
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