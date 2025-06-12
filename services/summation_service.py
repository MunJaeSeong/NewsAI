# NEWSIAI/services/summation_service.py
from transformers import pipeline
from typing import List, Dict, Optional

classifier = None

def load_summarization_model():
    global classifier
    if classifier is None:
        try:
            classifier = pipeline("summarization", "eenzeenee/t5-base-korean-summarization", device='cpu')
            print("요약 모델 로드 완료!") # 모델 로드 성공 시 메시지
        except Exception as e:
            print(f"요약 모델 로드 중 에러 발생: {e}")
            classifier = None
            raise
            
async def get_summaries(texts: List[str]) -> List[Dict]:
    if classifier is None:
        raise ValueError("요약 모델이 로드되지 않았습니다. 서버 초기화 로그를 확인해주세요.")
    
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