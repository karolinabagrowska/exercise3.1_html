import secrets
from fastapi import FastAPI, Response, status, Request, Cookie, HTTPException, Depends, status
from datetime import date
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    token: str

TOKEN_STR = "fake-cookie-session-value"
S_TOKEN = ""
T_TOKEN = ""

app = FastAPI()
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()

@app.get("/hello", response_class=HTMLResponse)
def get_hello(request: Request):
    date_today = date.today()
    return templates.TemplateResponse("index.html.j2", {"request": request ,"date_today": date_today})

@app.post("/login_session", status_code=201)
def post_login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    global S_TOKEN
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    S_TOKEN = TOKEN_STR
    response.set_cookie(key="session_token", value=S_TOKEN)

@app.post("/login_token", status_code=201)
def post_login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    global T_TOKEN
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    T_TOKEN = TOKEN_STR
    return {"token": T_TOKEN}

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
    if not token or token != T_TOKEN:
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
    global S_TOKEN
    if not session_token or session_token != S_TOKEN:
        raise HTTPException(status_code=401, detail="Unathorised")
    S_TOKEN = ""
    params = str(request.query_params)
    response = RedirectResponse(url=f'/logged_out?{params}', status_code=302)
    return response

@app.delete("/logout_token")
def delete_logout_token(request: Request, response: Response, format: Optional[str] = None, token: Optional[str] = None):
    global T_TOKEN
    if not token or token != T_TOKEN:
        raise HTTPException(status_code=401, detail="Unathorised")
    T_TOKEN = ""
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