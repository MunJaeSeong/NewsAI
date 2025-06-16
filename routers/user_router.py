from fastapi import APIRouter, HTTPException
from schemas.user_schema import UserRegisterRequest, UserLoginRequest, UserResponse
from services import user_service

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(request: UserRegisterRequest):
    result = user_service.register_user(
        username=request.username,
        password=request.password,
        email=request.email,
        name=request.name
    )
    if result.data:
        user = result.data[0]
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "name": user["name"]
        }
    raise HTTPException(status_code=400, detail="회원가입 실패")

@router.post("/login", response_model=UserResponse)
def login(request: UserLoginRequest):
    user = user_service.login_user(request.username, request.password)
    if user:
        return user
    raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다")
