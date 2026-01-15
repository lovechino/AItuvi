from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from infra.supabase import supabase
from fastapi.middleware.cors import CORSMiddleware
from routes import auth,tuvi_charts
import os
from Model.tuvi_charts import TuViRequest
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


@app.post("/public/agent")
def analyze_agent(data: TuViRequest):
    chart = build_tuvi_engine(
        day=data.day,
        month=data.month,
        year=data.year,
        hour=data.hour,
        minute=data.minute,
        gender=data.gender,
        nam_xem=data.nam_xem
    )

    result = analyze_tuvi(
        chart_result=chart,
        year=data.nam_xem
    )

    return {
        "success": True,
        "data": result
    }
