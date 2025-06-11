import os
import sys
import urllib.request
import json # JSON 처리를 위해 추가
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv() # .env 파일 로드

app = FastAPI() # FastAPI 앱 인스턴스 생성

# 검색 쿼리를 위한 Pydantic 모델 정의
class SearchQuery(BaseModel):
    query: str # 검색어

@app.post("/search/") # POST 요청을 처리할 /search/ 엔드포인트 정의
async def search_news(search_query: SearchQuery):
    client_id = os.getenv("YOUR_CLIENT_ID")
    client_secret = os.getenv("YOUR_CLIENT_SECRET")

    # API 키가 설정되지 않았다면 에러 반환
    if not client_id or not client_secret:
        raise HTTPException(status_code=500, detail="네이버 API 인증 정보가 설정되지 않았습니다.")

    # 입력받은 쿼리(검색어)를 URL 인코딩
    encText = urllib.parse.quote(search_query.query)
    # 네이버 뉴스 API URL 구성 (display=10은 10개 결과, sort=sim은 유사도 순 정렬)
    url = "https://openapi.naver.com/v1/search/news?query=" + encText + "&display=20&sort=sim"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            # 네이버 API 응답을 JSON 객체로 파싱하여 반환
            return {"status": "success", "data": json.loads(response_body)}
        else:
            # API 호출 실패 시 에러 반환
            raise HTTPException(status_code=rescode, detail=f"네이버 API 에러 코드: {rescode}")
    except urllib.error.URLError as e:
        # 네트워크 관련 에러 발생 시 처리
        raise HTTPException(status_code=500, detail=f"네트워크 에러: {e.reason}")
    except Exception as e:
        # 그 외 예상치 못한 에러 발생 시 처리
        raise HTTPException(status_code=500, detail=f"예상치 못한 에러가 발생했습니다: {str(e)}")