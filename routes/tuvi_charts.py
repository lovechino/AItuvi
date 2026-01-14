from .auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query
from infra.supabase import supabase
from Model.tuvi_charts import TuviChartCreate
router = APIRouter(
    prefix="/tuvi-charts",
    tags=["Tu Vi Charts"]
)

@router.get("")
def get_my_charts(
    user=Depends(get_current_user),   # ✅ BẮT BUỘC
    limit: int = Query(10, le=50),
    offset: int = 0,
):
    user_id = user.id

    res = (
        supabase.table("tuvi_charts")
        .select("id, birth_date, birth_time, gender, year_view, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )

    return {"items": res.data}

@router.get("/{chart_id}")
def get_chart_detail(
    chart_id: str,
    user=Depends(get_current_user),   # ✅
):
    user_id = user.id

    res = (
        supabase.table("tuvi_charts")
        .select("*")
        .eq("id", chart_id)
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    if not res.data:
        raise HTTPException(status_code=404, detail="Chart not found")

    return res.data


@router.post("")
def create_chart(
    payload: TuviChartCreate,
    user=Depends(get_current_user),   # ✅
):
    user_id = user.id

    res = (
        supabase.table("tuvi_charts")
        .insert({
            "user_id": user_id,
            **payload.dict()
        })
        .execute()
    )

    return res.data[0]

