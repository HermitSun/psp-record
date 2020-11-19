from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import json
import time

# entry
app = FastAPI()
# statics
app.mount("/static", StaticFiles(directory="static"), name="static")
# templates
templates = Jinja2Templates(directory="templates")

_data = {
    "logs": []
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    render_params = {
        "request": request,
        "_data": _data
    }
    return templates.TemplateResponse("index.html", render_params)


@app.get("/history")
async def index(request: Request):
    render_params = {
        "request": request,
        "_data": _data
    }
    return templates.TemplateResponse("history.html", render_params)


@app.get("/statistics")
async def index(request: Request):
    render_params = {
        "request": request,
        "_data": _data
    }
    return templates.TemplateResponse("statistics.html", render_params)


class Log(BaseModel):
    start_time: str
    pause_time: str
    end_time: str
    pure_time: str
    belong: str
    backlog: str


@app.post("/logs", status_code=status.HTTP_201_CREATED)
async def add_logs(log: Log):
    _data["logs"].append(log)
    # save
    log_file_name = time.strftime("%Y-%m-%d", time.localtime()) + '.log'
    with open(log_file_name, 'a') as log_file:
        log_file.write(json.dumps(log, default=lambda o: o.__dict__) + '\n')
