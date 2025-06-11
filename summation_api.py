from fastapi import FastAPI, HTTPException
from transformers import pipeline
from pydantic import BaseModel
from typing import List # 리스트 타입을 위해 추가

app = FastAPI()

# 요약 파이프라인을 전역으로 초기화
try:
    classifier = pipeline("summarization", "eenzeenee/t5-base-korean-summarization", device='cpu')
except Exception as e:
    print(f"요약 모델 로드 중 에러 발생: {e}")
    classifier = None

# 요약할 텍스트 리스트를 위한 Pydantic 모델 정의
class TextsToSummarize(BaseModel):
    texts: List[str] # 텍스트 리스트를 받도록 변경

@app.post("/summarize_multiple/") # 엔드포인트 이름 변경 (client_script.py와 일치하도록)
async def summarize_multiple_texts(texts_to_summarize: TextsToSummarize):
    if not classifier:
        raise HTTPException(status_code=503, detail="요약 모델이 로드되지 않았습니다. 서버 로그를 확인해주세요.")
    
    summaries = [] # 요약 결과를 담을 리스트
    
    # 입력받은 텍스트 리스트를 순회하며 각각 요약
    for text_item in texts_to_summarize.texts:
        try:
            result = classifier(text_item)
            if result and isinstance(result, list) and len(result) > 0:
                summaries.append({
                    #"original_text": text_item, # 원문도 포함 (선택 사항)
                    "summary": result[0].get('summary_text', '')
                })
            else:
                summaries.append({
                    #"original_text": text_item,
                    "summary": None,
                    "error": "요약 파이프라인이 예상치 못한 형식의 결과를 반환했습니다."
                })
        except Exception as e:
            summaries.append({
                #"original_text": text_item,
                "summary": None,
                "error": f"요약 중 에러 발생: {str(e)}"
            })
            
    return {"status": "success", "summaries": summaries}