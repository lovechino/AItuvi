from datetime import date, time
from pydantic import BaseModel
from typing import Dict, Any

class TuviChartCreate(BaseModel):
    birth_date: date
    birth_time: time
    gender: str
    year_view: int
    core_json: Dict[str, Any]