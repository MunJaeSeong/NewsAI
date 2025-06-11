import os
import urllib.request
import json

from fastapi import HTTPException

async def fetch_news_from_naver(query: str) -> dict:
    client_id = os.getenv("YOUR_CLIENT_ID")
    client_secret = os.getenv("YOUR_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("네이버 API 인증 정보가 설정되지 않았습니다.")

    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/news?query={encText}&display=20&sort=sim" # 최대 100개

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            return json.loads(response_body)
        else:
            raise HTTPException(status_code=rescode, detail=f"네이버 API 에러 코드: {rescode}")
    except urllib.error.URLError as e:
        raise HTTPException(status_code=500, detail=f"네트워크 에러: {e.reason}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"예상치 못한 에러가 발생했습니다: {str(e)}")