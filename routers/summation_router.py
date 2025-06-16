# routers/summation.py 파일의 내용
from fastapi import APIRouter, HTTPException
from schemas.summation_schema import TextsToSummarize, SummariesResponse # 스키마 임포트
from services import summation_service # 서비스 임포트

router = APIRouter()

@router.post("/multiple", response_model=SummariesResponse) # <-- 엔드포인트를 "/multiple"로 변경
async def summarize_multiple_texts_endpoint(texts_to_summarize: TextsToSummarize):
    try:
        summaries = await summation_service.get_summaries(texts_to_summarize.texts)
        return {"status": "success", "summaries": summaries}
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"요약 중 예상치 못한 에러: {str(e)}")