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

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from router import router, Request
from fastapi.responses import HTMLResponse

app = FastAPI(title="NewsMind AI", description="뉴스 분석 AI 서비스")

# 라우터 연결
app.include_router(router)

# 정적 파일 서빙 설정
# app.mount("/static", StaticFiles(directory="static"), name="static")

async def read_root(request: Request):
    """
    루트 경로에 대한 GET 요청을 처리합니다.
    기본 HTML 페이지를 반환합니다.
    """
    # HTML 파일 경로 설정
    html_file_path = Path(__file__).parent / "index.html"
    
    # HTML 파일 읽기
    with open(html_file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    return HTMLResponse(content=content)