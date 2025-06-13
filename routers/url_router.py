from fastapi import APIRouter, HTTPException, Query
from services.search_service import fetch_news_from_naver

router = APIRouter()

@router.get("/")
async def get_news_urls(keyword: str = Query(..., description="뉴스 검색어")):
    try:
        data = await fetch_news_from_naver(keyword)
        results = [
            {
                "title": item["title"],
                "link": item.get("link"),
                "originallink": item.get("originallink")
            }
            for item in data.get("items", [])
        ]
        return {"keyword": keyword, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
