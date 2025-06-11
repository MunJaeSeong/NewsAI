from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import Dict, List

app = FastAPI(title="SentimentAI API", description="한국어 금융 텍스트 감성 분석 API")

# 한국어 금융 감성 분석 모델 로드
sentiment_analyzer = pipeline("text-classification", model="snunlp/KR-FinBert-SC")

class TextInput(BaseModel):
    text: str

def analyze_sentiment(text: str) -> Dict:
    # 감성 분석 실행
    sentiment_result = sentiment_analyzer(text)
    
    # 모델의 원본 감성 레이블과 신뢰도
    original_label = sentiment_result[0]['label'].lower()
    score = sentiment_result[0]['score']
    
    # 최종적으로 반환할 감성 레이블
    final_korean_label = ""
    
    # 감성 후처리 로직
    if score < 0.5:
        final_korean_label = '중립'
    else:
        if original_label == 'positive':
            final_korean_label = '긍정'
        elif original_label == 'negative':
            final_korean_label = '부정'
        elif original_label == 'neutral':
            positive_keywords = ["증가", "개선", "성장", "호조", "기대", "확대", "발전", "상승", "긍정적"]
            negative_keywords = ["감소", "하락", "악화", "우려", "불안", "리스크", "경고", "둔화", "불확실", "부정적"]
            
            is_positive = any(keyword in text for keyword in positive_keywords)
            is_negative = any(keyword in text for keyword in negative_keywords)
            
            if is_positive and not is_negative:
                final_korean_label = '긍정 (중립에서 조정됨)'
            elif is_negative and not is_positive:
                final_korean_label = '부정 (중립에서 조정됨)'
            elif is_positive and is_negative:
                final_korean_label = '부정 (혼합 감성)'
            else:
                final_korean_label = '중립'
        else:
            final_korean_label = original_label
    
    return {
        "original_sentiment": original_label.capitalize(),
        "confidence_score": round(score, 4),
        "final_sentiment": final_korean_label,
        "input_text": text
    }

@app.post("/analyze", response_model=Dict)
async def analyze_text(text_input: TextInput):
    try:
        result = analyze_sentiment(text_input.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to SentimentAI API. Use POST /analyze endpoint with text input to analyze sentiment."} 