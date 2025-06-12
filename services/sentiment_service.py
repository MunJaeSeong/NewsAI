# NEWSIAI/services/sentiment_service.py
from transformers import pipeline
from typing import Dict

sentiment_analyzer = None

def load_sentiment_model():
    global sentiment_analyzer
    if sentiment_analyzer is None:
        try:
            sentiment_analyzer = pipeline("text-classification", model="snunlp/KR-FinBert-SC")
            print("감성 분석 모델 로드 완료!") # 모델 로드 성공 시 메시지
        except Exception as e:
            print(f"감성 분석 모델 로드 중 에러 발생: {e}")
            sentiment_analyzer = None
            raise

def analyze_financial_sentiment(text: str) -> Dict:
    if sentiment_analyzer is None:
        raise ValueError("감성 분석 모델이 로드되지 않았습니다. 서버 초기화를 확인해주세요.")

    sentiment_result = sentiment_analyzer(text)
    
    original_label = sentiment_result[0]['label'].lower()
    score = sentiment_result[0]['score']
    
    final_korean_label = ""
    
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

# 이 부분은 main.py의 startup 이벤트에서 호출되므로 제거해도 됩니다.
# load_sentiment_model()