# NEWSIAI/main.py
"""
NewsMind AI - 뉴스 분석 웹 애플리케이션

이 애플리케이션은 다음과 같은 기능을 제공합니다:
1. 뉴스 데이터 표시 및 필터링
   - 날짜순으로 뉴스 정렬
   - 감성(긍정/부정/중립)별 필터링
2. 회사 정보 관리
   - 관심 회사 목록 조회
3. 검색 기능
   - 뉴스 검색
   - 검색 기록 관리
4. 감성 분석
   - 뉴스의 감성을 긍정/부정/중립으로 분류
   - 감성별 뉴스 개수 표시
"""

from fastapi import FastAPI, Request, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from dotenv import load_dotenv
import os # os 모듈 임포트 추가

# 라우터 임포트
from routers import search_router, summation_router, sentiment_router, url_router, user_router
# services 디렉토리에서 서비스들을 임포트
from services import search_service, sentiment_service, summation_service

load_dotenv() # .env 파일 로드

app = FastAPI(title="NewsMind AI", description="뉴스 분석 AI 서비스")

# 정적 파일 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 템플릿 설정 (templates 폴더를 HTML 템플릿 디렉토리로 지정)
templates = Jinja2Templates(directory="templates")

# --- FastAPI 앱 시작 시 모델 로드 ---
@app.on_event("startup")
async def startup_event():
    print("FastAPI 앱 시작 이벤트 감지: 모델 로드 시작...")
    try:
        # 서비스 파일에 정의된 모델 로드 함수 호출
        # (각 서비스 파일에 load_XXX_model() 함수가 정의되어 있다고 가정)
        # search_service에는 모델 로드가 필요 없을 수 있습니다.
        if hasattr(summation_service, 'load_summarization_model'):
            summation_service.load_summarization_model()
        if hasattr(sentiment_service, 'load_sentiment_model'):
            sentiment_service.load_sentiment_model()
            
        # 네이버 API 키 환경 변수 확인
        client_id = os.getenv("YOUR_CLIENT_ID")
        client_secret = os.getenv("YOUR_CLIENT_SECRET")
        if not client_id or not client_secret:
            print("경고: 네이버 API 클라이언트 ID 또는 시크릿이 .env 파일에 설정되지 않았습니다.")
            print("검색 기능이 정상적으로 작동하지 않을 수 있습니다.")
        else:
            print("네이버 API 인증 정보 확인 완료.")

        print("모든 초기화 및 모델 로드 완료.")
    except Exception as e:
        print(f"초기화 또는 모델 로드 실패: {e}. 서버가 제대로 작동하지 않을 수 있습니다.")
# -----------------------------------

# 라우터 연결 (API 경로를 /api/{기능} 형태로 구성)
app.include_router(search_router.router, prefix="/search", tags=["Search"])
app.include_router(summation_router.router, prefix="/summarize", tags=["Summation"])
app.include_router(sentiment_router.router, prefix="/sentiment", tags=["Sentiment Analysis"])
app.include_router(url_router.router, prefix="/url", tags=["URL Fetch"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])

# 루트 경로 ("/")로 접속 시 index.html 파일을 렌더링하여 반환
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/check-login")
async def check_login(request: Request, username: str = Cookie(default=None)):
    """
    로그인 상태를 확인하는 엔드포인트. (쿠키에 username이 있으면 로그인된 것으로 간주)
    실제 구현에 맞게 세션/쿠키/토큰 확인 로직을 수정하세요.
    """
    if username:
        return {"loggedIn": True, "username": username}
    else:
        return {"loggedIn": False}
