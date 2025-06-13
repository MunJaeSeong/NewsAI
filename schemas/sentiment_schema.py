# from pydantic import BaseModel
# from typing import Dict, List, Optional

# class TextInput(BaseModel):
#     text: str

# # 감성 분석 결과 응답을 위한 스키마
# class SentimentResponse(BaseModel):
#     original_sentiment: str
#     confidence_score: float
#     final_sentiment: str
#     input_text: str



# NEWSIAI/schemas/sentiment_schema.py
from pydantic import BaseModel
from typing import Dict, List, Optional

# 기존 TextInput 스키마 유지
class TextInput(BaseModel):
    text: str

# 기존 SentimentResponse 스키마 유지 (단일 감성 분석 결과)
# 이 스키마는 sentiment_service.py의 analyze_sentiment 함수 반환 값에 맞춰야 합니다.
class SentimentResponse(BaseModel):
    sentiment: str # 변경: original_sentiment 대신 'sentiment'로 통일 (클라이언트와 일관성 위해)
    score: float # 변경: confidence_score 대신 'score'로 통일
    original_label: Optional[str] = None # 원본 모델 라벨 (선택 사항, 디버깅 용)
    input_text: Optional[str] = None # 입력 텍스트 (선택 사항, 디버깅 용)

# Note: sentiment_service.py에서 analyze_sentiment 함수는 
# {"sentiment": final_korean_label, "score": round(score, 4), "original_label": original_label, "input_text": text}
# 를 반환하므로, SentimentResponse를 이 형식에 맞췄습니다.
# 만약 클라이언트에서 'original_sentiment', 'confidence_score', 'final_sentiment'를 기대한다면
# SentimentResponse를 다시 조정하거나, 서비스 레이어에서 반환 키를 조정해야 합니다.
# 현재 클라이언트 (index.js)는 'sentiment'와 'score'를 사용하고 있으므로, 이 스키마가 더 적합합니다.

# 단일 감성 분석 요청 스키마 (라우터의 /analyze 엔드포인트에서 사용)
# `TextInput`과 동일하지만, 의미상 명확하게 구분하기 위해 `SentimentRequest`로 정의
class SentimentRequest(BaseModel):
    text: str

# 배치 감성 분석 요청의 각 결과 항목에 대한 스키마
class BatchSentimentResult(BaseModel):
    sentiment: str
    score: float

# 배치 감성 분석 요청 스키마
class BatchSentimentRequest(BaseModel):
    texts: List[str]

# 배치 감성 분석 응답 스키마
class BatchSentimentResponse(BaseModel):
    results: List[BatchSentimentResult]