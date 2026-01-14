from fastapi import Request, HTTPException,Header
from jose import jwt, JWTError
from infra.supabase import supabase
import os

SUPABASE_JWT_SECRET = str(os.getenv("SUPABASE_JWT_SECRET")).strip()
ALGORITHM = "ES256"

PUBLIC_PATHS = [
    "/auth/login",
    "/auth/callback",
    "/docs",
    "/openapi.json",
    "/public"
]

async def auth_middleware(request: Request, call_next):
    # ✅ Cho OPTIONS đi qua (CORS)
    if request.method == "OPTIONS":
        return await call_next(request)

    # ✅ Cho public routes đi qua
    if any(request.url.path.startswith(p) for p in PUBLIC_PATHS):
        return await call_next(request)

    auth_header = request.headers.get("authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=[ALGORITHM],
            audience="authenticated",
            options={"verify_aud": True},
        )

        # ✅ Gắn user vào request
        request.state.user = payload

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    return await call_next(request)



async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(status_code=401, detail="No Authorization header found")

    # Xử lý lấy token linh hoạt
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        # Trường hợp frontend chỉ gửi mỗi token (không có Bearer)
        token = auth_header

    try:
        # Xác thực với Supabase
        user_response = supabase.auth.get_user(token)
        return user_response.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")