import secrets
from fastapi import FastAPI, Response, status, Request, Cookie, HTTPException, Depends, status
from datetime import date
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

class Token(BaseModel):
    token: str

S_TOKEN = "fake-cookie-session-value"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()

@app.post("/login_session", status_code=201)
def post_login_session(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    response.set_cookie(key="session_token", value=S_TOKEN)
    return credentials.username

@app.post("/login_token")
def post_login_token(*, response: Response, session_token: str = Cookie(None)):
    if session_token != S_TOKEN:
        raise HTTPException(status_code=401, detail="Unathorised")
    else:
        return {"token": S_TOKEN}