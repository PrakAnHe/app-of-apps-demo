import datetime
import os
import subprocess
from pathlib import Path

from fastapi import Depends, FastAPI, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db import Message, get_db, init_db

app = FastAPI()

ENV_MESSAGE = os.getenv("MESSAGE", "Default message from FastAPI")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def read_root():
    return {"info": info_object()}


@app.get("/env")
def read_env():
    return {"message": ENV_MESSAGE, "info": info_object()}


@app.get("/web", response_class=FileResponse)
def web_page():
    file_path = Path(__file__).parent / "static" / "index.html"
    return FileResponse(file_path)


# @app.get("/web", response_class=HTMLResponse)
# def web_page():
#     return "<h1>Welcome to FastAPI</h1><p>This is a simple web page.</p><p>Hest!</p>"


@app.post("/save/")
def save_message(text: str = Form(...), db: Session = Depends(get_db)):
    """Save a message to the database."""
    new_message = Message(text=text)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"id": new_message.id, "text": new_message.text}


@app.get("/messages/")
def get_messages(db: Session = Depends(get_db)):
    """Retrieve all messages from the database."""
    messages = db.query(Message).all()
    return [{"id": m.id, "text": m.text, "timestamp": m.timestamp} for m in messages]


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
