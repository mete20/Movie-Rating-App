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
from app.routers import router_user, router_movie, router_rating 

app = FastAPI()
app.mount('/auth', auth_app)
app.mount('/api', api_app)
app.include_router(router_user.router)
app.include_router(router_movie.router)
app.include_router(router_rating.router)

        
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
    



