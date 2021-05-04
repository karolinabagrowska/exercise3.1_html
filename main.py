import secrets
from fastapi import FastAPI, Response, status, Request, Cookie, HTTPException, Depends, status
from datetime import date
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    token: str

S_TOKEN = "fake-cookie-session-value"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()

@app.get("/hello", response_class=HTMLResponse)
def get_hello(request: Request):
    date_today = date.today()
    return templates.TemplateResponse("index.html.j2", {"request": request ,"date_today": date_today})

@app.post("/login_session", status_code=201)
def post_login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    response.set_cookie(key="session_token", value=S_TOKEN)

@app.post("/login_token", status_code=201)
def post_login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"token": S_TOKEN}

@app.get("/welcome_session", status_code=200)
def get_welcome_session(response: Response, format: Optional[str] = None, session_token: str = Cookie(None)):
    if not session_token or session_token != S_TOKEN:
        raise HTTPException(status_code=401, detail="Unathorised")
    if format == "json":
        content = {"message": "Welcome!"}
        return JSONResponse(content=content)
    elif format == "html":
        content = "<h1>Welcome!</h1>"
        return HTMLResponse(content=content)
    else:
        content = "Welcome!"
        return PlainTextResponse(content = content)

@app.get("/welcome_token", status_code=200)
def get_welcome_token(response: Response, token: Optional[str] = None, format: Optional[str] = None):
    if not token or token != S_TOKEN:
        raise HTTPException(status_code=401, detail="Unathorised")
    if format == "json":
        content = {"message": "Welcome!"}
        return JSONResponse(content=content)
    elif format == "html":
        content = "<h1>Welcome!</h1>"
        return HTMLResponse(content=content)
    else:
        content = "Welcome!"
        return PlainTextResponse(content = content)