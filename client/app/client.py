from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/token")
async def root():
    return FileResponse("static/index.html")

@app.get("/")
async def root():
    return HTMLResponse('<body><a href="http://localhost:8000/auth/login">Log In</a></body>')

