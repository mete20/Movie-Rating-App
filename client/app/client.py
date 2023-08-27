from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse('<body><a href="http://localhost:8000/auth/login">Log In</a></body>')

@app.get("/token")
async def token():
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
                    req.open("get", "http://localhost:8000/auth/token?"+window.location.search.substr(1), true);
                    req.send("");

                }
                </script>
                <button onClick="send()">Get FastAPI JWT Token</button>

                <button onClick='fetch("http://localhost:8000/api/").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Unprotected API
                </button>
                
                <button onClick='fetch("http://localhost:8000/movies/").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Get Movies
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
                
                <button onClick='fetch("http://localhost:8000/users",{
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                }).then((r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Get Users
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
