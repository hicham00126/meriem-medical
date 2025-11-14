from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pathlib

app = FastAPI()

# السماح للمتصفح بالوصول للملفات (مثل الصور)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# نركّب ملفات الستاتيك على المسار /static
# ضع الصورة eph_logo.png في نفس مجلد المشروع (مع login.html و request.html)
app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/login", response_class=HTMLResponse)
def login_page():
    path = pathlib.Path("login.html")
    return path.read_text(encoding="utf-8")

@app.get("/request", response_class=HTMLResponse)
def request_page():
    path = pathlib.Path("request.html")
    return path.read_text(encoding="utf-8")

@app.post("/login")
def login(data: dict):
    if data.get("username") == "khelef" and data.get("password") == "lina":
        return {"status": "ok"}
    return {"status": "error"}, 401

@app.post("/create_request")
def create_request(data: dict):
    return {"message": "تم إرسال الطلب بنجاح"}