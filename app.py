from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pathlib

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/login", response_class=HTMLResponse)
def get_login_page():
    path = pathlib.Path(__file__).parent / "login.html"
    return path.read_text(encoding="utf-8")

@app.get("/request", response_class=HTMLResponse)
def get_request_page():
    path = pathlib.Path(__file__).parent / "request.html"
    return path.read_text(encoding="utf-8")

USERS = {
    "hicham": "1234"
}

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login_check")
def login_check(data: LoginData):
    if data.username in USERS and USERS[data.username] == data.password:
        return {"status": "ok"}
    return {"status": "error"}

class TransferRequest(BaseModel):
    patient_name: str
    from_dep: str
    to_dep: str

@app.post("/create_request")
def create_request(data: TransferRequest):
    return {"message": "تم إرسال الطلب بنجاح"}
