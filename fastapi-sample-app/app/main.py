import datetime
import os
import subprocess

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

ENV_MESSAGE = os.getenv("MESSAGE", "Default message from FastAPI")


@app.get("/")
def read_root():
    return {info_object()}


@app.get("/env")
def read_env():
    return {"message": ENV_MESSAGE, "info": info_object()}


@app.get("/web", response_class=HTMLResponse)
def web_page():
    return "<h1>Welcome to FastAPI</h1><p>This is a simple web page.</p><p>Hest!</p>"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


def info_object():
    return {
        "timestamp": datetime.datetime.now(),
        "container_name": subprocess.check_output(["cat", "/etc/hostname"])
        .decode()
        .strip(),
        "container_ip": subprocess.check_output(["hostname", "-I"]).decode().strip(),
    }
