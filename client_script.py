import requests

BASE_URL = "http://localhost:8000"

def test_fetch_urls(keyword: str):
    url = f"{BASE_URL}/url/"
    params = {"keyword": keyword}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"검색어: {data['keyword']}")
        for item in data["results"]:
            print(f"제목: {item['title']}")
            print(f"네이버 링크: {item['link']}")
            print(f"원문 링크: {item['originallink']}")
            print("-" * 60)
    else:
        print(f"에러 발생 (status code: {response.status_code})")
        print(response.text)

if __name__ == "__main__":
    test_keyword = "삼성전자"
    test_fetch_urls(test_keyword)
