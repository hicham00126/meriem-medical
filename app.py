# app.py
from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pathlib
import uvicorn
from typing import List
from pydantic import BaseModel
from datetime import datetime
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials

BASE = pathlib.Path(__file__).parent

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (css, images, js, manifest)
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")

# In-memory storage for demo (replace with DB in production)
requests_store = []
request_id_seq = 1

# ADMIN basic auth (simple demo). Change user/pass before production.
security = HTTPBasic()
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"  # غيّرها فوراً

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

class TransferRequest(BaseModel):
    patient_name: str
    patient_state: str
    from_dep: str
    to_dep: str
    created_at: str = None
    id: int = None
    status: str = "pending"

@app.get("/", response_class=HTMLResponse)
def root():
    return FileResponse(BASE / "static" / "index.html")

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return FileResponse(BASE / "static" / "login.html")

@app.get("/request", response_class=HTMLResponse)
def request_page():
    return FileResponse(BASE / "static" / "request.html")

@app.get("/admin", response_class=HTMLResponse)
def admin_page(username: str = Depends(get_current_username)):
    return FileResponse(BASE / "static" / "admin.html")

@app.post("/login")
async def api_login(data: dict):
    # demo auth (for web page JS). For production use sessions/JWT.
    if data.get("username") == "khelef" and data.get("password") == "lina":
        return {"status":"ok"}
    return JSONResponse({"status":"error","message":"invalid credentials"}, status_code=401)

@app.post("/create_request")
async def create_request(req: TransferRequest):
    global request_id_seq
    req.created_at = datetime.utcnow().isoformat()
    req.id = request_id_seq
    request_id_seq += 1
    requests_store.append(req.dict())
    return {"message":"تم إرسال الطلب بنجاح", "id": req.id}

@app.get("/api/requests", response_model=List[TransferRequest])
def list_requests(username: str = Depends(get_current_username)):
    return requests_store

@app.post("/api/requests/{rid}/status")
def change_status(rid: int, status: str = Form(...), username: str = Depends(get_current_username)):
    for r in requests_store:
        if r["id"] == rid:
            r["status"] = status
            return {"ok": True}
    raise HTTPException(status_code=404, detail="not found")

# serve PWA files
@app.get("/manifest.json")
def manifest():
    return FileResponse(BASE / "static" / "manifest.json")

@app.get("/service-worker.js")
def sw():
    return FileResponse(BASE / "static" / "service-worker.js")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)