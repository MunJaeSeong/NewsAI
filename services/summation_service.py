# # NEWSIAI/services/summation_service.py
# from transformers import pipeline
# from typing import List, Dict, Optional

# classifier = None

# def load_summarization_model():
#     global classifier
#     if classifier is None:
#         try:
#             classifier = pipeline("summarization", "eenzeenee/t5-base-korean-summarization", device='cpu')
#             print("요약 모델 로드 완료!") # 모델 로드 성공 시 메시지
#         except Exception as e:
#             print(f"요약 모델 로드 중 에러 발생: {e}")
#             classifier = None
#             raise

# async def get_summaries(texts: List[str]) -> List[Dict]:
#     if classifier is None:
#         raise ValueError("요약 모델이 로드되지 않았습니다. 서버 초기화 로그를 확인해주세요.")
    
#     summaries = []
#     for text_item in texts:
#         try:
#             result = classifier(text_item)
#             if result and isinstance(result, list) and len(result) > 0:
#                 summaries.append({
#                     "original_text": text_item,
#                     "summary": result[0].get('summary_text', '')
#                 })
#             else:
#                 summaries.append({
#                     "original_text": text_item,
#                     "summary": None,
#                     "error": "요약 파이프라인이 예상치 못한 형식의 결과를 반환했습니다."
#                 })
#         except Exception as e:
#             summaries.append({
#                 "original_text": text_item,
#                 "summary": None,
#                 "error": f"요약 중 에러 발생: {str(e)}"
#             })
#     return summaries


# NEWSIAI/services/summation_service.py
from transformers import pipeline
import torch # GPU 사용을 위해 torch 임포트
from typing import List, Dict, Optional
import traceback # traceback 모듈 임포트 추가

summarization_pipeline = None # classifier 대신 더 명확한 이름 사용

async def load_summarization_model(): # <--- async 키워드 추가
    """
    요약 모델을 로드합니다.
    애플리케이션 시작 시 한 번만 호출되도록 합니다.
    """
    global summarization_pipeline
    if summarization_pipeline is None:
        print("Loading summarization model...")
        # GPU 사용 가능 여부 확인: torch.cuda.is_available()이 True이면 첫 번째 GPU (0)를 사용하고, 아니면 CPU (-1)를 사용합니다.
        device = 0 if torch.cuda.is_available() else -1
        try:
            # device 인자 추가
            summarization_pipeline = pipeline(
                "summarization",
                model="eenzeenee/t5-base-korean-summarization",
                tokenizer="eenzeenee/t5-base-korean-summarization",
                device=device # GPU 또는 CPU 사용 설정
            )
            print(f"요약 모델 로드 완료! (Device: {'cuda' if device == 0 else 'cpu'})") # 디바이스 정보 출력
        except Exception as e:
            print(f"요약 모델 로드 중 에러 발생: {e}")
            traceback.print_exc() # 모델 로딩 실패 시 스택 트레이스 출력
            summarization_pipeline = None # 로딩 실패 시 None으로 유지
            raise # 모델 로딩 실패 시 애플리케이션 시작을 중단할 수 있도록 예외 다시 발생
    return summarization_pipeline  # <- 반환 추가

async def get_summaries(texts: List[str]) -> List[Dict]:
    """
    주어진 텍스트 리스트에 대해 요약을 수행합니다.
    모델의 배치 처리 기능을 활용하여 효율성을 높입니다.
    """
    # 모델이 로드되었는지 확인
    summarizer = await load_summarization_model() # 모델이 로드되어 있는지 확인하고 가져옴
    if summarizer is None:
        # 혹시라도 summarization_pipeline이 할당되어 있으면 그걸 사용
        global summarization_pipeline
        summarizer = summarization_pipeline
    if summarizer is None:
        raise ValueError("요약 모델이 로드되지 않았습니다. 서버 초기화 로그를 확인해주세요.")
    
    if not texts:
        return []

    summaries = []
    try:
        # pipeline의 배치 처리 기능 활용: 텍스트 리스트를 직접 전달
        # min_length와 max_length를 적절히 조절하여 요약 길이 제어
        # do_sample=False (기본값)는 탐욕적 디코딩을 사용하여 더 일관된 결과
        # num_beams=5 (일반적으로 좋은 품질)는 빔 서치 사용
        print(f"요약 시작: 총 {len(texts)}개의 텍스트 요약 시도.") # 디버깅용 로그
        results = summarizer(
            texts, 
            max_length=150,  # 요약의 최대 길이 (원본 텍스트 길이에 따라 조절)
            min_length=30,   # 요약의 최소 길이
            do_sample=False, 
            num_beams=5
        )
        print("요약 파이프라인 호출 완료.") # 디버깅용 로그
        
        for i, original_text in enumerate(texts):
            summary_text = None
            error_message = None

            if i < len(results) and results[i] and isinstance(results[i], dict):
                summary_text = results[i].get('summary_text')
            else:
                error_message = "요약 파이프라인이 예상치 못한 형식의 결과를 반환했습니다."
            
            if not summary_text: # 요약 결과가 비어있거나 생성되지 않았을 경우
                error_message = error_message or "요약 생성에 실패했습니다." # 기존 에러 메시지 유지
                summaries.append({
                    "original_text": original_text,
                    "summary": None,
                    "error": error_message
                })
            else:
                summaries.append({
                    "original_text": original_text,
                    "summary": summary_text
                })

    except Exception as e:
        print(f"get_summaries 함수 내 요약 처리 중 예상치 못한 에러 발생: {e}") # 디버깅용 로그
        traceback.print_exc() # 정확한 스택 트레이스 출력
        # 배치 처리 중 전체적인 에러 발생 시 모든 항목에 에러를 기록
        for text_item in texts:
            summaries.append({
                "original_text": text_item,
                "summary": None,
                "error": f"요약 중 전체 에러 발생: {str(e)}"
            })
        raise # 이 예외를 다시 던져 라우터에서 처리되도록 함
    
    return summaries