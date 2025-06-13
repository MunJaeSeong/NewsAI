# # NEWSIAI/main.py
# """
# NewsMind AI - 뉴스 분석 웹 애플리케이션

# 이 애플리케이션은 다음과 같은 기능을 제공합니다:
# 1. 뉴스 데이터 표시 및 필터링
#    - 날짜순으로 뉴스 정렬
#    - 감성(긍정/부정/중립)별 필터링
# 2. 회사 정보 관리
#    - 관심 회사 목록 조회
# 3. 검색 기능
#    - 뉴스 검색
#    - 검색 기록 관리
# 4. 감성 분석
#    - 뉴스의 감성을 긍정/부정/중립으로 분류
#    - 감성별 뉴스 개수 표시
# """

# from fastapi import FastAPI, Request
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import Response
# import uvicorn
# from dotenv import load_dotenv
# import os # os 모듈 임포트 추가

# # routers 디렉토리에서 라우터들을 임포트
# from routers import search_router, sentiment_router, summation_router
# # services 디렉토리에서 서비스들을 임포트
# from services import search_service, sentiment_service, summation_service

# load_dotenv() # .env 파일 로드

# app = FastAPI(title="NewsMind AI", description="뉴스 분석 AI 서비스")

# # 정적 파일 설정
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Jinja2 템플릿 설정 (templates 폴더를 HTML 템플릿 디렉토리로 지정)
# templates = Jinja2Templates(directory="templates")

# # --- FastAPI 앱 시작 시 모델 로드 ---
# @app.on_event("startup")
# async def startup_event():
#     print("FastAPI 앱 시작 이벤트 감지: 모델 로드 시작...")
#     try:
#         # 서비스 파일에 정의된 모델 로드 함수 호출
#         # (각 서비스 파일에 load_XXX_model() 함수가 정의되어 있다고 가정)
#         # search_service에는 모델 로드가 필요 없을 수 있습니다.
#         if hasattr(summation_service, 'load_summarization_model'):
#             summation_service.load_summarization_model()
#         if hasattr(sentiment_service, 'load_sentiment_model'):
#             sentiment_service.load_sentiment_model()
            
#         # 네이버 API 키 환경 변수 확인
#         client_id = os.getenv("YOUR_CLIENT_ID")
#         client_secret = os.getenv("YOUR_CLIENT_SECRET")
#         if not client_id or not client_secret:
#             print("경고: 네이버 API 클라이언트 ID 또는 시크릿이 .env 파일에 설정되지 않았습니다.")
#             print("검색 기능이 정상적으로 작동하지 않을 수 있습니다.")
#         else:
#             print("네이버 API 인증 정보 확인 완료.")

#         print("모든 초기화 및 모델 로드 완료.")
#     except Exception as e:
#         print(f"초기화 또는 모델 로드 실패: {e}. 서버가 제대로 작동하지 않을 수 있습니다.")
# # -----------------------------------

# # 라우터 연결 (API 경로를 /api/{기능} 형태로 구성)
# app.include_router(search_router.router, prefix="/api/search", tags=["Search"])
# app.include_router(summation_router.router, prefix="/api/summarize", tags=["Summation"])
# app.include_router(sentiment_router.router, prefix="/api/sentiment", tags=["Sentiment Analysis"])

# # 루트 경로 ("/")로 접속 시 index.html 파일을 렌더링하여 반환
# @app.get("/")
# async def read_root(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/favicon.ico")
# async def get_favicon():
#     return Response(status_code=204)

# if __name__ == '__main__':
#     print("뉴스 분석 AI 서비스 시작 준비 중...")
#     print("http://localhost:8000 에서 확인하세요")
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



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

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response
import uvicorn
from dotenv import load_dotenv
import os # os 모듈 임포트 추가

# routers 디렉토리에서 라우터들을 임포트
# 현재 프로젝트 구조에 따라 상대경로 대신 직접 임포트 사용
from routers import search_router, sentiment_router, summation_router
# services 디렉토리에서 서비스들을 임포트
# 현재 프로젝트 구조에 따라 상대경로 대신 직접 임포트 사용
from services import search_service, sentiment_service, summation_service

load_dotenv() # .env 파일 로드

app = FastAPI(title="NewsMind AI", description="뉴스 분석 AI 서비스")

# 정적 파일 설정
# 현재 `main.py`가 프로젝트 루트에 있고 `static` 디렉토리가 같은 레벨에 있다고 가정
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 템플릿 설정 (templates 폴더를 HTML 템플릿 디렉토리로 지정)
# 현재 `main.py`가 프로젝트 루트에 있고 `templates` 디렉토리가 같은 레벨에 있다고 가정
templates = Jinja2Templates(directory="templates")

# --- FastAPI 앱 시작 시 모델 로드 ---
@app.on_event("startup")
async def startup_event():
    print("FastAPI 앱 시작 이벤트 감지: 모델 로드 시작...")
    try:
        # 서비스 파일에 정의된 모델 로드 함수 호출
        # (각 서비스 파일에 load_XXX_model() 함수가 정의되어 있다고 가정)
        # `async` 함수이므로 `await` 키워드 사용이 필요합니다.
        
        # summation_service 모델 로드
        if hasattr(summation_service, 'load_summarization_model'):
            await summation_service.load_summarization_model() # await 추가
        
        # sentiment_service 모델 로드
        if hasattr(sentiment_service, 'load_sentiment_model'):
            await sentiment_service.load_sentiment_model() # await 추가
            
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
# 현재 라우터 파일들이 router 객체를 직접 내보내므로, .router 속성 사용
app.include_router(search_router.router, prefix="/api/search", tags=["Search"])
app.include_router(summation_router.router, prefix="/api/summarize", tags=["Summation"])
app.include_router(sentiment_router.router, prefix="/api/sentiment", tags=["Sentiment Analysis"])

# 루트 경로 ("/")로 접속 시 index.html 파일을 렌더링하여 반환
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/favicon.ico")
async def get_favicon():
    # favicon 요청에 대한 빈 응답 (204 No Content)
    return Response(status_code=204)

if __name__ == '__main__':
    print("뉴스 분석 AI 서비스 시작 준비 중...")
    print("http://localhost:8000 에서 확인하세요")
    # uvicorn.run의 첫 번째 인자는 "모듈이름:FastAPI앱객체이름" 입니다.
    # 이 파일이 main.py 이므로 "main:app" 으로 설정합니다.
    # reload=True는 코드 변경 시 자동으로 서버를 재시작합니다. 개발 환경에 유용합니다.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)