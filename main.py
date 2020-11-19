from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional

import datetime
import json
import os

from utils.date import plus_hhmmss

# entry
app = FastAPI()
# statics
app.mount("/static", StaticFiles(directory="static"), name="static")
# templates
templates = Jinja2Templates(directory="templates")


class Log(BaseModel):
    start_time: str
    pause_time: str
    end_time: str
    pure_time: str
    belong: str
    backlog: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    render_params = {
        "request": request
    }
    return templates.TemplateResponse("index.html", render_params)


@app.get("/history")
@app.get("/history/{mode}")
async def history(request: Request, mode: Optional[str] = None):
    # 读取日志共用方法
    def read_logs(date_str: str):
        logs = []
        date_log = 'logs/{}.log'.format(date_str)
        if os.path.exists(date_log):
            with open(date_log) as logs_that_day:
                for log in logs_that_day:
                    logs.append(json.loads(log.strip()))
        return logs

    def get_simple_stats(logs):
        total_pure_time = '00:00:00'
        total_pause_time = '00:00:00'
        # print(logs)
        for log in logs:
            total_pure_time = plus_hhmmss(total_pure_time, log['pause_time'])
            total_pause_time = plus_hhmmss(total_pause_time, log['pure_time'])
        return {
            'total_pure_time': total_pure_time,
            'total_pause_time': total_pause_time
        }

    date_logs = dict()
    date_stats = dict()
    today = datetime.datetime.today()
    # 今天
    if not mode:
        today_str = today.strftime("%Y-%m-%d")
        date_logs[today_str] = read_logs(today_str)
        # 统计
        date_stats[today_str] = get_simple_stats(date_logs[today_str])
        # 近两天
    if mode == 'last-2-days':
        last_2_days_list = [(today - datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 2)]
        for date in last_2_days_list:
            date_logs[date] = read_logs(date)
            # 统计
            date_stats[date] = get_simple_stats(date_logs[date])
    # 近七天
    elif mode == 'last-week':
        last_week_list = [(today - datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 7)]
        for date in last_week_list:
            date_logs[date] = read_logs(date)
            # 统计
            date_stats[date] = get_simple_stats(date_logs[date])

    render_params = {
        "request": request,
        "_data": {
            "date_logs": date_logs,
            "date_stats": date_stats
        }
    }
    return templates.TemplateResponse("history.html", render_params)


@app.get("/statistics")
async def statistics(request: Request):
    logs = []
    render_params = {
        "request": request,
        "_data": {
            "logs": logs
        }
    }
    return templates.TemplateResponse("statistics.html", render_params)


@app.post("/logs", status_code=status.HTTP_201_CREATED)
async def add_logs(log: Log):
    # save
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    log_file_name = 'logs/{}.log'.format(today)
    with open(log_file_name, 'a') as log_file:
        log_file.write(json.dumps(log, default=lambda o: o.__dict__) + '\n')
