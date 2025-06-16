from pydantic import BaseModel
from typing import Dict, List, Optional

class TextInput(BaseModel):
    text: str

# 감성 분석 결과 응답을 위한 스키마
class SentimentResponse(BaseModel):
    original_sentiment: str
    confidence_score: float
    final_sentiment: str
    input_text: str