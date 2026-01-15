from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from infra.supabase import supabase
from fastapi.middleware.cors import CORSMiddleware
from routes import auth,tuvi_charts
import os
from core.core import build_tuvi_engine
from tuvi_rag import analyze_tuvi
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


@app.get("/public/agent")
def test():
    chart =  build_tuvi_engine(
    day=15,
    month=7,
    year=2006,
    hour=8,
    minute=40,      # 8h40 vẫn là giờ Thìn
    gender="Nam",
    nam_xem=2026
    )

    # result = analyze_tuvi(chart_result=chart,year=2026)
    result = analyze_tuvi(chart_result=chart,year=2026)
    return{
        "result":result
    }
