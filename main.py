from fastapi import FastAPI, Response, status, Request
from datetime import date, datetime, time, timedelta
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/hello", response_class=HTMLResponse)
def get_hello(request: Request):
    date_today = date.today()
    return templates.TemplateResponse("index.html.j2", {"request": request ,"date_today": date_today})



        