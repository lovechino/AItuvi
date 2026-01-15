from datetime import date, time
from pydantic import BaseModel, Field
from typing import Dict, Any,Literal

class TuviChartCreate(BaseModel):
    birth_date: date
    birth_time: time
    gender: str
    year_view: int
    core_json: Dict[str, Any]



class TuViRequest(BaseModel):
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    gender: Literal["Nam", "Nữ"]
    nam_xem: int = Field(..., ge=1900)