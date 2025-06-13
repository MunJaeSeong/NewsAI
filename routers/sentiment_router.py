# from fastapi import APIRouter, HTTPException
# from schemas.sentiment_schema import TextInput, SentimentResponse # 스키마 임포트
# from services import sentiment_service # 서비스 임포트

# router = APIRouter()

# @router.post("/analyze", response_model=SentimentResponse) # /sentiment/analyze
# async def analyze_text_endpoint(text_input: TextInput):
#     try:
#         result = sentiment_service.analyze_financial_sentiment(text_input.text)
#         return result
#     except ValueError as e:
#         raise HTTPException(status_code=503, detail=str(e)) # 모델 로드 실패 등
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"감성 분석 중 예상치 못한 에러: {str(e)}")



# NEWSIAI/routers/sentiment_router.py
from fastapi import APIRouter, HTTPException
# 스키마 임포트: 단일 요청/응답 및 배치 요청/응답 스키마 모두 필요
from schemas.sentiment_schema import SentimentRequest, SentimentResponse, BatchSentimentRequest, BatchSentimentResponse, BatchSentimentResult
# 서비스 임포트: 단일 분석 및 배치 분석 함수 모두 필요
from services import sentiment_service

router = APIRouter() # APIRouter 객체 이름이 'router'이므로 그대로 사용

@router.post("/analyze", response_model=SentimentResponse) # /sentiment/analyze
async def analyze_text_endpoint(request: SentimentRequest): # TextInput 대신 SentimentRequest 사용
    """
    단일 텍스트에 대한 감성 분석을 수행합니다.
    """
    try:
        # sentiment_service.py에서 함수 이름을 analyze_sentiment로 변경했으므로 이에 맞춰 호출
        result = await sentiment_service.analyze_sentiment(request.text) # await 추가
        # 서비스에서 반환하는 dict를 SentimentResponse 스키마에 맞게 반환
        return SentimentResponse(sentiment=result["sentiment"], score=result["score"])
    except ValueError as e:
        raise HTTPException(status_code=503, detail=f"감성 분석 모델 로드 또는 처리 실패: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"단일 감성 분석 중 예상치 못한 에러: {str(e)}")

@router.post("/analyze/batch", response_model=BatchSentimentResponse)
async def analyze_batch_text_endpoint(request: BatchSentimentRequest):
    """
    여러 텍스트에 대한 감성 분석을 배치로 수행합니다.
    """
    if not request.texts:
        return BatchSentimentResponse(results=[])
    try:
        # sentiment_service.py에서 analyze_batch_sentiment 함수 호출
        results = await sentiment_service.analyze_batch_sentiment(request.texts) # await 추가
        
        # 서비스에서 반환된 결과가 BatchSentimentResult 스키마에 맞는지 확인하고 변환
        formatted_results = [BatchSentimentResult(sentiment=r["sentiment"], score=r["score"]) for r in results]
        return BatchSentimentResponse(results=formatted_results)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=f"배치 감성 분석 모델 로드 또는 처리 실패: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"배치 감성 분석 중 예상치 못한 에러: {str(e)}")