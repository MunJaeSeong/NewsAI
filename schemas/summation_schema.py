from pydantic import BaseModel
from typing import List, Optional

class TextsToSummarize(BaseModel):
    texts: List[str]

# 요약 결과 개별 항목을 위한 스키마
class SummaryItem(BaseModel):
    original_text: str
    summary: Optional[str] = None # 요약 실패 시 None 가능
    error: Optional[str] = None # 요약 실패 시 에러 메시지 가능

# 요약 API 전체 응답을 위한 스키마
class SummariesResponse(BaseModel):
    status: str
    summaries: List[SummaryItem]