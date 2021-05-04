import secrets
from fastapi import FastAPI, Response, status, Request, Cookie, HTTPException, Depends, status
from datetime import date
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import uuid

class Token(BaseModel):
    token: str

S_TOKENS = []
current_s_token = ""
T_TOKENS = []
current_t_token = ""

app = FastAPI()
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()

@app.get("/hello", response_class=HTMLResponse)
def get_hello(request: Request):
    date_today = date.today()
    return templates.TemplateResponse("index.html.j2", {"request": request ,"date_today": date_today})

@app.post("/login_session", status_code=201)
def post_login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    global current_s_token
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    current_s_token = str(uuid.uuid4())
    S_TOKENS.append(current_s_token)
    if len(S_TOKENS) == 4:
        S_TOKENS.pop(0)
    response.set_cookie(key="session_token", value=current_s_token)

@app.post("/login_token", status_code=201)
def post_login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    global current_t_token
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    current_t_token = str(uuid.uuid4())
    T_TOKENS.append(current_t_token)
    if len(T_TOKENS) == 4:
        T_TOKENS.pop(0)
    return {"token": current_t_token}

@app.get("/welcome_session", status_code=200)
def get_welcome_session(response: Response, format: Optional[str] = None, session_token: str = Cookie(None)):
    global S_TOKENS
    if session_token not in S_TOKENS:
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
    global T_TOKENS
    if token not in T_TOKENS:
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

@app.delete("/logout_session")
def delete_logout_session(request: Request, response: Response, format: Optional[str] = None, session_token: str = Cookie(None)):
    global current_s_token
    global S_TOKENS
    if session_token not in S_TOKENS:
        raise HTTPException(status_code=401, detail="Unathorised")
    S_TOKENS.remove(current_s_token)
    current_s_token = ""
    params = str(request.query_params)
    response = RedirectResponse(url=f'/logged_out?{params}', status_code=302)
    return response

@app.delete("/logout_token")
def delete_logout_token(request: Request, response: Response, format: Optional[str] = None, token: Optional[str] = None):
    global current_t_token
    global T_TOKENS
    if token not in T_TOKENS:
        raise HTTPException(status_code=401, detail="Unathorised")
    T_TOKENS.remove(current_t_token)
    current_t_token = ""
    params = str(request.query_params)
    response = RedirectResponse(url=f'/logged_out?{params}', status_code=302)
    return response

@app.get("/logged_out", status_code=200)
def get_logged_out(response: Response, format: Optional[str] = None):
    if format == "json":
        content = {"message": "Logged out!"}
        return JSONResponse(content=content)
    elif format == "html":
        content = "<h1>Logged out!</h1>"
        return HTMLResponse(content=content)
    else:
        content = "Logged out!"
        return PlainTextResponse(content = content)