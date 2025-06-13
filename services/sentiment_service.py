# # NEWSIAI/services/sentiment_service.py
# from transformers import pipeline
# from typing import Dict

# sentiment_analyzer = None

# def load_sentiment_model():
#     global sentiment_analyzer
#     if sentiment_analyzer is None:
#         try:
#             sentiment_analyzer = pipeline("text-classification", model="snunlp/KR-FinBert-SC")
#             print("감성 분석 모델 로드 완료!") # 모델 로드 성공 시 메시지
#         except Exception as e:
#             print(f"감성 분석 모델 로드 중 에러 발생: {e}")
#             sentiment_analyzer = None
#             raise

# def analyze_financial_sentiment(text: str) -> Dict:
#     if sentiment_analyzer is None:
#         raise ValueError("감성 분석 모델이 로드되지 않았습니다. 서버 초기화를 확인해주세요.")

#     sentiment_result = sentiment_analyzer(text)
    
#     original_label = sentiment_result[0]['label'].lower()
#     score = sentiment_result[0]['score']
    
#     final_korean_label = ""
    
#     if score < 0.5:
#         final_korean_label = '중립'
#     else:
#         if original_label == 'positive':
#             final_korean_label = '긍정'
#         elif original_label == 'negative':
#             final_korean_label = '부정'
#         elif original_label == 'neutral':
#             positive_keywords = ["증가", "개선", "성장", "호조", "기대", "확대", "발전", "상승", "긍정적"]
#             negative_keywords = ["감소", "하락", "악화", "우려", "불안", "리스크", "경고", "둔화", "불확실", "부정적"]
            
#             is_positive = any(keyword in text for keyword in positive_keywords)
#             is_negative = any(keyword in text for keyword in negative_keywords)
            
#             if is_positive and not is_negative:
#                 final_korean_label = '긍정 (중립에서 조정됨)'
#             elif is_negative and not is_positive:
#                 final_korean_label = '부정 (중립에서 조정됨)'
#             elif is_positive and is_negative:
#                 final_korean_label = '부정 (혼합 감성)'
#             else:
#                 final_korean_label = '중립'
#         else:
#             final_korean_label = original_label
    
#     return {
#         "original_sentiment": original_label.capitalize(),
#         "confidence_score": round(score, 4),
#         "final_sentiment": final_korean_label,
#         "input_text": text
#     }

# # 이 부분은 main.py의 startup 이벤트에서 호출되므로 제거해도 됩니다.
# # load_sentiment_model()



# NEWSIAI/services/sentiment_service.py
from transformers import pipeline
import torch
from typing import List, Dict

# 모델 로딩은 애플리케이션 시작 시 한 번만 이루어지도록 전역 변수로 관리
sentiment_analyzer = None

async def load_sentiment_model():
    """
    감성 분석 모델을 로드합니다.
    애플리케이션 시작 시 한 번만 호출되도록 합니다.
    """
    global sentiment_analyzer
    if sentiment_analyzer is None:
        print("Loading sentiment analysis model...")
        # GPU 사용 가능 여부 확인
        # torch.cuda.is_available()이 True이면 첫 번째 GPU (0)를 사용하고, 아니면 CPU (-1)를 사용합니다.
        device = 0 if torch.cuda.is_available() else -1
        try:
            # model과 tokenizer를 명시적으로 지정
            sentiment_analyzer = pipeline(
                "sentiment-analysis", # 또는 "text-classification", 하지만 sentiment-analysis가 더 적합
                model="snunlp/KR-FinBert-SC",
                tokenizer="snunlp/KR-FinBert-SC",
                device=device  # GPU 또는 CPU 사용 설정
            )
            print(f"Sentiment analysis model loaded on device: {'cuda' if device == 0 else 'cpu'}")
        except Exception as e:
            print(f"Error loading sentiment analysis model: {e}")
            sentiment_analyzer = None # 로딩 실패 시 None으로 유지하여 재시도 또는 오류 처리 유도
            raise # 모델 로딩 실패 시 애플리케이션 시작을 중단할 수 있도록 예외 다시 발생
    return sentiment_analyzer

# 원래 analyze_financial_sentiment의 로직을 analyze_single_sentiment로 변경
async def analyze_single_sentiment(text: str) -> Dict:
    """
    단일 텍스트에 대한 감성 분석을 수행합니다.
    모델의 원본 레이블과 점수를 기반으로 최종 한글 감성 라벨을 결정합니다.
    """
    analyzer = await load_sentiment_model()
    if analyzer is None:
        raise ValueError("감성 분석 모델이 로드되지 않았습니다. 서버 초기화를 확인해주세요.")

    # pipeline은 기본적으로 list를 받으므로, 단일 텍스트도 list로 전달
    sentiment_result = analyzer(text)
    
    # 결과가 항상 리스트로 반환되므로 첫 번째 요소를 사용
    if not sentiment_result:
        return {
            "original_sentiment": "N/A",
            "confidence_score": 0.0,
            "final_sentiment": "분석 불가",
            "input_text": text
        }
    
    original_label = sentiment_result[0]['label'].lower()
    score = sentiment_result[0]['score']
    
    final_korean_label = ""
    
    # 모델의 신뢰도 점수가 0.5 미만이면 '중립'으로 판단
    if score < 0.5:
        final_korean_label = '중립'
    else:
        if original_label == 'positive':
            final_korean_label = '긍정'
        elif original_label == 'negative':
            final_korean_label = '부정'
        elif original_label == 'neutral':
            # 'neutral'로 분류되었지만, 텍스트 내 키워드를 통해 다시 판단
            positive_keywords = ["증가", "개선", "성장", "호조", "기대", "확대", "발전", "상승", "긍정적", "증권", "금융", "시장"] # 금융 관련 키워드 추가
            negative_keywords = ["감소", "하락", "악화", "우려", "불안", "리스크", "경고", "둔화", "불확실", "부정적", "손실", "위험"] # 금융 관련 키워드 추가
            
            is_positive = any(keyword in text for keyword in positive_keywords)
            is_negative = any(keyword in text for keyword in negative_keywords)
            
            if is_positive and not is_negative:
                final_korean_label = '긍정' # (중립에서 조정됨) 문구 제거, 최종 라벨만
            elif is_negative and not is_positive:
                final_korean_label = '부정' # (중립에서 조정됨) 문구 제거, 최종 라벨만
            elif is_positive and is_negative:
                # 긍정/부정 키워드가 모두 있으면 부정으로 판단 (금융 뉴스 특성상 보수적)
                final_korean_label = '부정' # (혼합 감성) 문구 제거, 최종 라벨만
            else:
                final_korean_label = '중립'
        else:
            # 예상치 못한 라벨의 경우 원본 라벨을 사용하거나 중립으로 처리
            final_korean_label = '중립' # 원본 라벨이 아닌 일관된 한글 라벨 사용

    return {
        "original_sentiment": original_label.capitalize(),
        "confidence_score": round(score, 4),
        "final_sentiment": final_korean_label, # 클라이언트에서 이 필드를 사용
        "input_text": text
    }

async def analyze_batch_sentiment(texts: List[str]) -> List[Dict]:
    """
    여러 텍스트에 대한 감성 분석을 배치로 수행합니다.
    analyze_single_sentiment의 로직을 각 배치 항목에 적용합니다.
    """
    analyzer = await load_sentiment_model()
    if analyzer is None:
        raise ValueError("감성 분석 모델이 로드되지 않았습니다. 서버 초기화를 확인해주세요.")
    
    if not texts:
        return []

    # pipeline의 배치 처리 기능 활용
    # 각 텍스트에 대해 모델의 raw 출력을 한 번에 얻음
    raw_results = analyzer(texts) # 이 부분이 핵심

    formatted_results = []
    for i, result in enumerate(raw_results):
        text = texts[i] # 원본 텍스트 가져오기
        original_label = result['label'].lower()
        score = result['score']

        final_korean_label = ""
        
        if score < 0.5:
            final_korean_label = '중립'
        else:
            if original_label == 'positive':
                final_korean_label = '긍정'
            elif original_label == 'negative':
                final_korean_label = '부정'
            elif original_label == 'neutral':
                positive_keywords = ["증가", "개선", "성장", "호조", "기대", "확대", "발전", "상승", "긍정적", "증권", "금융", "시장"]
                negative_keywords = ["감소", "하락", "악화", "우려", "불안", "리스크", "경고", "둔화", "불확실", "부정적", "손실", "위험"]
                
                is_positive = any(keyword in text for keyword in positive_keywords)
                is_negative = any(keyword in text for keyword in negative_keywords)
                
                if is_positive and not is_negative:
                    final_korean_label = '긍정'
                elif is_negative and not is_positive:
                    final_korean_label = '부정'
                elif is_positive and is_negative:
                    final_korean_label = '부정'
                else:
                    final_korean_label = '중립'
            else:
                final_korean_label = '중립' # 알 수 없는 라벨 처리

        formatted_results.append({
            "sentiment": final_korean_label, # 클라이언트에서 `sentiment` 필드를 사용하고 있으므로 여기에 최종 라벨 저장
            "score": round(score, 4),
            "original_label": original_label.capitalize(), # 디버깅을 위해 원본 라벨도 포함
            "input_text": text
        })
    return formatted_results

# main.py의 startup 이벤트에서 호출되므로, 이 파일에서 직접 호출하는 부분은 제거합니다.
# load_sentiment_model() # 이 부분 제거