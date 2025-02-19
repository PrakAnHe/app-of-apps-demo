import datetime
import os
import subprocess
import time
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db import Message, get_db, init_db

app = FastAPI()

ENV_MESSAGE = os.getenv("MESSAGE", "Default message from FastAPI")
ENV_CRASH_ON_START = os.getenv("CRASH_ON_START", "False")
print("Hest 1!")

if ENV_CRASH_ON_START.lower() == "true":
    time.sleep(10)
    print("Intentional crash!")
    os._exit(1)

print("Hest 2!")

crash_on_call = -1
error_on_call = -1


if __name__ == "__main__":
    import uvicorn

    print("Hest 3!")

    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.on_event("startup")
def startup():
    print("Hest 4!")
    init_db()


@app.get("/", response_class=FileResponse)
def web_page():
    check_crash()
    check_error()
    file_path = Path(__file__).parent / "static" / "index.html"
    return FileResponse(file_path)


@app.get("/h")
def healthcheck():
    return Response(status_code=200)


@app.get("/env")
def read_env():
    check_crash()
    check_error()
    return {"message": ENV_MESSAGE, "info": info_object()}


@app.post("/message/")
def save_message(text: str = Form(...), db: Session = Depends(get_db)):
    """Save a message to the database."""
    check_crash()
    check_error()
    new_message = Message(text=text)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"id": new_message.id, "text": new_message.text}


@app.get("/message/")
def get_messages(db: Session = Depends(get_db)):
    """Retrieve all messages from the database."""
    check_crash()
    check_error()
    messages = db.query(Message).all()
    return [{"id": m.id, "text": m.text, "timestamp": m.timestamp} for m in messages]


@app.get("/code/{code}")
def return_code(code: int):
    check_crash()
    check_error()
    return Response(status_code=code)


@app.get("/crash/")
def crash_now():
    crash()


@app.get("/crash/{amt}")
def crash_on_n_call(amt: int):
    global crash_on_call
    crash_on_call = amt
    return {"message": f"Container will crash during request number {amt} after this."}


@app.get("/error/")
def error_now():
    error()


@app.get("/error/{amt}")
def error_on_n_call(amt: int):
    global error_on_call
    error_on_call = amt
    return {
        "message": f"Container will raise a RuntimeError during request number {amt} after this."
    }


def check_crash():
    global crash_on_call
    crash_on_call = crash_on_call - 1
    if crash_on_call == 0:
        crash()


def check_error():
    global error_on_call
    error_on_call = error_on_call - 1
    if error_on_call == 0:
        error()


def crash():
    print("Intentional crash!")
    os._exit(1)


def error():
    raise RuntimeError("Intentional error!")


def info_object():
    return {
        "timestamp": datetime.datetime.now(),
        "container_name": subprocess.check_output(["cat", "/etc/hostname"])
        .decode()
        .strip(),
        "container_ip": subprocess.check_output(["hostname", "-I"]).decode().strip(),
    }
