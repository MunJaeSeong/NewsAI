from fastapi import APIRouter, HTTPException
from schemas.sentiment import TextInput, SentimentResponse # 스키마 임포트
from services import sentiment_service # 서비스 임포트

router = APIRouter()

@router.post("/analyze", response_model=SentimentResponse) # /sentiment/analyze
async def analyze_text_endpoint(text_input: TextInput):
    try:
        result = sentiment_service.analyze_financial_sentiment(text_input.text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) # 모델 로드 실패 등
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"감성 분석 중 예상치 못한 에러: {str(e)}")