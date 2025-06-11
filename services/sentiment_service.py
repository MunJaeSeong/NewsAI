from transformers import pipeline
from typing import Dict

# 모델은 한 번만 로드되도록 전역 변수로 유지
sentiment_analyzer = None

def load_sentiment_model():
    global sentiment_analyzer
    if sentiment_analyzer is None:
        try:
            sentiment_analyzer = pipeline("text-classification", model="snunlp/KR-FinBert-SC")
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
            final_korean_label = original_label # 예외 케이스
    
    return {
        "original_sentiment": original_label.capitalize(),
        "confidence_score": round(score, 4),
        "final_sentiment": final_korean_label,
        "input_text": text
    }

# 서버 시작 시 모델을 미리 로드하도록 함수 호출
load_sentiment_model()