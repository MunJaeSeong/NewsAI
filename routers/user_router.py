from fastapi import APIRouter, HTTPException
from schemas.user_schema import UserRegisterRequest, UserLoginRequest, UserResponse
from services import user_service

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(request: UserRegisterRequest):
    result = user_service.register_user(request.email, request.password)
    if result.data:
        user = result.data[0]
        return {"id": user["id"], "email": user["email"]}
    raise HTTPException(status_code=400, detail="회원가입 실패")

@router.post("/login", response_model=UserResponse)
def login(request: UserLoginRequest):
    user = user_service.login_user(request.email, request.password)
    if user:
        return user
    raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다")
