import requests
import json
import sys

# 0단계: 사용자로부터 검색어 입력받기
search_term = input("검색어를 입력하세요: ")

# 통합 API의 기본 URL (main.py가 실행되는 포트)
BASE_API_URL = "http://127.0.0.1:8000" # main.py가 8000번 포트에서 실행된다고 가정

# 감성별 개수를 저장할 딕셔너리 초기화 (3가지 주요 감성만)
sentiment_counts = {
    "긍정": 0,
    "부정": 0,
    "중립": 0,
    "요약 실패": 0,
    "감성 분석 실패": 0
}

try:
    # 1단계: 통합 검색 API 호출 (prefix로 /search가 붙음)
    search_url = f"{BASE_API_URL}/search/"
    search_payload = {"query": search_term}
    search_response = requests.post(search_url, json=search_payload)
    search_response.raise_for_status()
    
    search_data = search_response.json()
    if search_data.get("status") == "success":
        naver_news_data = search_data.get("data")
        
        descriptions = [item["description"] for item in naver_news_data.get("items", [])]
        
        if descriptions:
            print(f"\n--- 검색어: '{search_term}' ---")
            print(f"총 {len(descriptions)}개의 뉴스를 처리합니다.\n")

            # 2단계: 모든 description을 통합 요약 API에 한 번에 전송 (prefix로 /summarize가 붙음)
            summarize_url = f"{BASE_API_URL}/summarize/multiple" # 통합 라우터 엔드포인트
            summarize_payload = {"texts": descriptions}
            summarize_response = requests.post(summarize_url, json=summarize_payload)
            summarize_response.raise_for_status()
            
            summarized_data = summarize_response.json()
            if summarized_data.get("status") == "success":
                for i, item in enumerate(summarized_data.get("summaries", [])):
                    original_text = item.get('original_text', 'N/A')
                    summary_text = item.get('summary')
                    
                    print(f"\n--- 뉴스 {i+1} ---")
                    # print(f"원문: {original_text}")
                    
                    if summary_text is not None:
                        print(f"요약: {summary_text}")
                        
                        # 3단계: 요약된 텍스트를 통합 감성 분석 API에 전송 (prefix로 /sentiment가 붙음)
                        sentiment_url = f"{BASE_API_URL}/sentiment/analyze" # 통합 라우터 엔드포인트
                        sentiment_payload = {"text": summary_text}
                        try:
                            sentiment_response = requests.post(sentiment_url, json=sentiment_payload)
                            sentiment_response.raise_for_status()
                            
                            sentiment_data = sentiment_response.json()
                            final_sentiment = sentiment_data.get('final_sentiment', 'N/A')
                            # 원문: {sentiment_data.get('original_sentiment', 'N/A')}, 
                            print(f"감성 분석 결과: {final_sentiment} (신뢰도: {sentiment_data.get('confidence_score', 'N/A')})")
                            
                            if "긍정" in final_sentiment:
                                sentiment_counts["긍정"] += 1
                            elif "부정" in final_sentiment:
                                sentiment_counts["부정"] += 1
                            elif "중립" in final_sentiment:
                                sentiment_counts["중립"] += 1
                            else:
                                pass

                        except requests.exceptions.RequestException as e:
                            print(f"감성 분석 API 호출 실패: {e}")
                            sentiment_counts["감성 분석 실패"] += 1
                        except json.JSONDecodeError:
                            print("감성 분석 API 응답 디코딩 실패.")
                            sentiment_counts["감성 분석 실패"] += 1
                        except Exception as e:
                            print(f"감성 분석 중 예상치 못한 에러: {e}")
                            sentiment_counts["감성 분석 실패"] += 1

                    else:
                        print(f"요약 실패: {item.get('error', '알 수 없는 오류')}")
                        sentiment_counts["요약 실패"] += 1
            else:
                print(f"요약 API 에러: {summarized_data.get('detail', '알 수 없는 에러')}")
                    
        else:
            print(f"검색어 '{search_term}'에 대한 뉴스 설명을 찾을 수 없습니다.")
    else:
        print(f"검색 API 에러: {search_data.get('detail', '알 수 없는 에러')}")

except requests.exceptions.RequestException as e:
    print(f"요청 실패: {e}")
except json.JSONDecodeError:
    print("JSON 응답 디코딩 실패.")
except Exception as e:
    print(f"예상치 못한 에러 발생: {e}")

finally:
    print("\n\n--- 최종 감성 분석 결과 요약 ---")
    for sentiment, count in sentiment_counts.items():
        if count > 0:
            print(f"{sentiment}: {count}개")
    print("---------------------------------")