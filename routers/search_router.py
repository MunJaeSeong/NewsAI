from fastapi import APIRouter, HTTPException
from schemas.search_schema import SearchQuery, SearchResponse # 스키마 임포트
from services import search_service # 서비스 임포트

router = APIRouter()

@router.post("/", response_model=SearchResponse) # /search/는 main.py에서 prefix로 처리
async def search_news_endpoint(search_query: SearchQuery):
    try:
        naver_data = await search_service.fetch_news_from_naver(search_query.query)
        return {"status": "success", "data": naver_data}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException as e:
        raise e # search_service에서 발생시킨 HTTPException은 그대로 전달
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 중 예상치 못한 에러: {str(e)}")