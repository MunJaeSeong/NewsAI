from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import os

# 라우터 생성
router = APIRouter()

# 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")

# 임시 사용자 저장소 (실제로는 데이터베이스를 사용해야 함)
users_db = {}

@router.get("/login")
async def login_page(request: Request):
    """
    로그인 페이지를 렌더링합니다.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/api/login")
async def login(
    username: str = Form(...),
    password: str = Form(...)
):
    """
    사용자 로그인을 처리합니다.
    """
    # 실제 인증 로직이 들어가야 합니다.
    print(f"로그인 시도: {username}")
    return {"message": "로그인 성공", "success": True}

@router.get("/signup")
async def signup_page(request: Request):
    """
    회원가입 페이지를 렌더링합니다.
    """
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/api/signup")
async def signup(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    name: str = Form(...)
):
    """
    사용자 회원가입을 처리합니다.
    """
    # 사용자 이름 중복 확인
    if username in users_db:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자 이름입니다.")
    
    # 사용자 정보 저장 (실제로는 데이터베이스에 저장해야 함)
    users_db[username] = {
        "username": username,
        "password": password,  # 실제로는 해시 처리해야 함
        "email": email,
        "name": name
    }
    
    print(f"새로운 사용자 가입: {username}, {email}, {name}")
    return {"message": "회원가입이 완료되었습니다.", "success": True}

@router.get("/api/check-login")
async def check_login(request: Request):
    """
    사용자 로그인 상태를 확인합니다.
    """
    # 실제 세션 확인 로직이 들어가야 함
    username = None
    return {
        "loggedIn": username is not None,
        "username": username
    }

@router.post("/api/logout")
async def logout():
    """
    사용자 로그아웃을 처리합니다.
    """
    # 실제 세션 삭제 로직이 들어가야 함
    return {"message": "로그아웃 되었습니다.", "success": True}
