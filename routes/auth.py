from fastapi import APIRouter, Depends, Request, HTTPException, Query
from infra.supabase import supabase
import os
from middlewares.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])






# ===== Protected route =====
@router.get("/me")
def me(user=Depends(get_current_user)):
     return {
        # "user_id": user["sub"],
        # "email": user["email"]
        "user":user
    }
   
