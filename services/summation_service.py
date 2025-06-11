from transformers import pipeline
from typing import List, Dict, Optional

# 모델은 한 번만 로드되도록 전역 변수로 유지
classifier = None

def load_summarization_model():
    global classifier
    if classifier is None:
        try:
            classifier = pipeline("summarization", "eenzeenee/t5-base-korean-summarization", device='cpu')
        except Exception as e:
            print(f"요약 모델 로드 중 에러 발생: {e}")
            classifier = None
            raise

async def get_summaries(texts: List[str]) -> List[Dict]:
    if classifier is None:
        raise ValueError("요약 모델이 로드되지 않았습니다. 서버 초기화를 확인해주세요.")
    
    summaries = []
    for text_item in texts:
        try:
            result = classifier(text_item)
            if result and isinstance(result, list) and len(result) > 0:
                summaries.append({
                    "original_text": text_item,
                    "summary": result[0].get('summary_text', '')
                })
            else:
                summaries.append({
                    "original_text": text_item,
                    "summary": None,
                    "error": "요약 파이프라인이 예상치 못한 형식의 결과를 반환했습니다."
                })
        except Exception as e:
            summaries.append({
                "original_text": text_item,
                "summary": None,
                "error": f"요약 중 에러 발생: {str(e)}"
            })
    return summaries

# 서버 시작 시 모델을 미리 로드하도록 함수 호출
# (main.py에서 앱 시작 시 호출하는 것이 더 명확하지만, 여기서는 서비스 파일 자체에서 로드 시도)
load_summarization_model()