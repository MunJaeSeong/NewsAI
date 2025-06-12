from typing import List
from pydantic import BaseModel

class SearchQuery(BaseModel):
    query: str

# 네이버 뉴스 API 응답 항목을 위한 스키마 (옵션: 더 상세한 검증을 위해)
class NaverNewsItem(BaseModel):
    title: str
    originallink: str
    link: str
    description: str
    pubDate: str

# 네이버 뉴스 API 전체 응답을 위한 스키마 (옵션)
class NaverNewsResponse(BaseModel):
    lastBuildDate: str
    total: int
    start: int
    display: int
    items: List[NaverNewsItem]

# search_api.py의 /search 응답을 위한 스키마
class SearchResponse(BaseModel):
    status: str
    data: dict # 실제 NaverNewsResponse가 들어올 것이지만, 유연성을 위해 dict로 둡니다.