from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from infra.supabase import supabase
from fastapi.middleware.cors import CORSMiddleware
from routes import auth,tuvi_charts
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

# app.middleware("http")(get_current_user)

# Routers
app.include_router(auth.router)
app.include_router(tuvi_charts.router)

@app.get("/public/health")
def health():
    return {"status": "ok"}



