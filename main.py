from fastapi import FastAPI
from dotenv import load_dotenv
import os

# 각 라우터를 임포트합니다.
from routers import search, summation, sentiment

load_dotenv() # .env 파일 로드

app = FastAPI(
    title="News Analysis API",
    description="뉴스 검색, 요약, 감성 분석을 제공하는 통합 API",
    version="1.0.0"
)

# 각 라우터를 메인 앱에 포함시킵니다.
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(summation.router, prefix="/summarize", tags=["Summation"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment Analysis"])

@app.get("/")
async def root():
    return {"message": "Welcome to the News Analysis API. Check /docs for API documentation."}