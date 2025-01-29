import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!", "timecode": datetime.datetime.now()}


@app.get("/web", response_class=HTMLResponse)
def web_page():
    return "<h1>Welcome to FastAPI</h1><p>This is a simple web page.</p><p>Hest!</p>"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
