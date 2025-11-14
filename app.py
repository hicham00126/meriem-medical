from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pathlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/login", response_class=HTMLResponse)
def login_page():
    path = pathlib.Path(__file__).parent / "login.html"
    return path.read_text(encoding="utf-8")

@app.get("/request", response_class=HTMLResponse)
def request_page():
    path = pathlib.Path(__file__).parent / "request.html"
    return path.read_text(encoding="utf-8")

@app.post("/login_check")
async def login_check(data: dict):
    username = data.get("username", "")
    password = data.get("password", "")
    if username == "hicham" and password == "1234":
        return {"status": "ok"}
    return {"status": "error"}

@app.post("/create_request")
async def create_request(data: dict):
    return {"message": "تم إرسال الطلب بنجاح"}