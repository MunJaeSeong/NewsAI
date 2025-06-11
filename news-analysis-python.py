"""
NewsMind AI - 뉴스 분석 웹 애플리케이션

이 애플리케이션은 다음과 같은 기능을 제공합니다:
1. 뉴스 데이터 표시 및 필터링
   - 날짜순으로 뉴스 정렬
   - 감성(긍정/부정/중립)별 필터링
2. 회사 정보 관리
   - 관심 회사 목록 조회
3. 검색 기능
   - 뉴스 검색
4. 감성 분석
   - 뉴스의 감성을 긍정/부정/중립으로 분류
   - 감성별 뉴스 개수 표시

사용된 주요 기술:
- FastAPI: 웹 프레임워크
- Jinja2: HTML 템플릿 엔진
- Tailwind CSS: 스타일링
- JavaScript: 프론트엔드 기능 구현
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path

app = FastAPI(title="NewsMind AI", description="뉴스 분석 AI 서비스")

# 정적 파일과 템플릿 설정
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# static 디렉토리 생성
static_dir = BASE_DIR / "static"
static_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# 샘플 데이터
sample_news = {
    "삼성전자": [
        {
            "title": "삼성전자, 새로운 AI 칩 개발 발표",
            "summary": "삼성전자가 새로운 AI 반도체 개발을 발표했습니다.",
            "sentiment": "positive",
            "date": "2024-03-20"
        },
        {
            "title": "삼성전자 실적, 시장 예상치 하회",
            "summary": "삼성전자의 분기 실적이 시장 예상치에 미치지 못했습니다.",
            "sentiment": "negative",
            "date": "2024-03-19"
        },
        {
            "title": "삼성전자, 중립적 이슈 발생",
            "summary": "삼성전자가 새로운 사업을 검토 중입니다.",
            "sentiment": "neutral",
            "date": "2024-03-18"
        }
    ],
    "SK하이닉스": [
        {
            "title": "SK하이닉스, 반도체 가격 하락으로 실적 악화",
            "summary": "글로벌 반도체 시장 침체로 SK하이닉스의 실적이 악화되었습니다.",
            "sentiment": "negative",
            "date": "2024-03-18"
        },
        {
            "title": "SK하이닉스, 친환경 경영 강화",
            "summary": "SK하이닉스가 친환경 경영을 강화한다고 밝혔습니다.",
            "sentiment": "positive",
            "date": "2024-03-17"
        }
    ],
    "네이버": [
        {
            "title": "네이버, AI 번역 서비스 출시",
            "summary": "네이버가 새로운 AI 번역 서비스를 선보였습니다.",
            "sentiment": "positive",
            "date": "2024-03-16"
        },
        {
            "title": "네이버, 서비스 장애 발생",
            "summary": "일부 네이버 서비스에서 장애가 발생했습니다.",
            "sentiment": "negative",
            "date": "2024-03-15"
        }
    ],
    "카카오": [
        {
            "title": "카카오, 신규 게임 출시 예정",
            "summary": "카카오가 신규 모바일 게임 출시를 예고했습니다.",
            "sentiment": "neutral",
            "date": "2024-03-14"
        },
        {
            "title": "카카오, 사회공헌 활동 확대",
            "summary": "카카오가 사회공헌 활동을 확대한다고 밝혔습니다.",
            "sentiment": "positive",
            "date": "2024-03-13"
        }
    ]
}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """메인 페이지"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/news")
async def get_news():
    """뉴스 목록 조회"""
    return sample_news

# HTML 템플릿
html_template = '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsMind AI - 뉴스 분석 서비스</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div id="app" class="min-h-screen">
        <header class="bg-white shadow-sm">
            <div class="max-w-7xl mx-auto px-4 py-4">
                <div class="flex justify-between items-center">
                    <a href="/" class="text-2xl font-bold text-blue-600">NewsMind AI</a>
                </div>
            </div>
        </header>
        
        <main class="max-w-7xl mx-auto px-4 py-8">
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
                <!-- 사이드바 -->
                <div class="lg:col-span-1">
                    <div class="bg-white rounded-lg shadow p-6">
                        <h3 class="text-lg font-semibold mb-4">분석 정리</h3>
                        <div class="space-y-4">
                            <div class="p-3 bg-green-50 rounded-lg cursor-pointer hover:bg-green-100"
                                 onclick="filterNews('positive')">
                                <div class="flex justify-between items-center">
                                    <h4 class="font-medium text-green-800">긍정적 뉴스</h4>
                                    <span id="positive-count" class="text-sm font-medium text-green-800">0개</span>
                                </div>
                            </div>
                            <div class="p-3 bg-red-50 rounded-lg cursor-pointer hover:bg-red-100"
                                 onclick="filterNews('negative')">
                                <div class="flex justify-between items-center">
                                    <h4 class="font-medium text-red-800">부정적 뉴스</h4>
                                    <span id="negative-count" class="text-sm font-medium text-red-800">0개</span>
                                </div>
                            </div>
                            <div class="p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100"
                                 onclick="filterNews('neutral')">
                                <div class="flex justify-between items-center">
                                    <h4 class="font-medium text-gray-800">중립적 뉴스</h4>
                                    <span id="neutral-count" class="text-sm font-medium text-gray-800">0개</span>
                                </div>
                            </div>
                            <button onclick="resetFilter()" 
                                    class="w-full mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                                전체 보기
                            </button>
                        </div>
                    </div>
                </div>
                
                <!-- 메인 컨텐츠 -->
                <div class="lg:col-span-3">
                    <div class="bg-white rounded-lg shadow p-6 mb-6">
                        <div class="flex gap-2">
                            <input type="text" id="search-input" placeholder="회사명을 입력하세요 (예: 삼성전자, SK하이닉스)" 
                                   class="flex-1 px-4 py-2 border rounded-lg">
                            <button onclick="searchNews()" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
                                검색
                            </button>
                        </div>
                    </div>
                    
                    <div id="news-list"></div>
                </div>
            </div>
        </main>
    </div>
    
    <script>
        let currentNews = [];
        let currentFilter = null;

        async function searchNews() {
            const companyName = document.getElementById('search-input').value.trim();
            if (!companyName) {
                alert('회사이름을 입력해주세요');
                return;
            }
            try {
                const response = await fetch('/api/news');
                const newsData = await response.json();
                if (newsData[companyName]) {
                    currentNews = newsData[companyName];
                    displayNews(currentNews);
                    displaySentimentNews(currentNews);
                } else {
                    alert('해당 회사의 뉴스를 찾을 수 없습니다.');
                }
            } catch (error) {
                console.error('검색 중 오류 발생:', error);
            }
        }

        function displayNews(news) {
            const container = document.getElementById('news-list');
            // 날짜순으로 정렬
            const sortedNews = [...news].sort((a, b) => 
                new Date(b.date) - new Date(a.date)
            );
            
            container.innerHTML = sortedNews.map(item => `
                <div class="bg-white rounded-lg shadow p-6 mb-4">
                    <div class="flex justify-between items-start mb-3">
                        <h2 class="text-lg font-bold text-gray-900">${item.title}</h2>
                        <span class="px-2 py-1 text-xs rounded-full ${getSentimentColor(item.sentiment)}">
                            ${getSentimentText(item.sentiment)}
                        </span>
                    </div>
                    <p class="text-gray-700 mb-3">${item.summary}</p>
                    <div class="text-sm text-gray-500">
                        <span>${item.date}</span>
                    </div>
                </div>
            `).join('');
        }

        function filterNews(sentiment) {
            currentFilter = sentiment;
            const filteredNews = currentNews.filter(item => item.sentiment === sentiment);
            displayNews(filteredNews);
        }

        function resetFilter() {
            currentFilter = null;
            displayNews(currentNews);
        }

        function displaySentimentNews(news) {
            const positiveNews = news.filter(item => item.sentiment === 'positive');
            const negativeNews = news.filter(item => item.sentiment === 'negative');
            const neutralNews = news.filter(item => item.sentiment === 'neutral');

            document.getElementById('positive-count').textContent = `${positiveNews.length}개`;
            document.getElementById('negative-count').textContent = `${negativeNews.length}개`;
            document.getElementById('neutral-count').textContent = `${neutralNews.length}개`;
        }
        
        function getSentimentColor(sentiment) {
            switch(sentiment) {
                case 'positive': return 'bg-green-100 text-green-800';
                case 'negative': return 'bg-red-100 text-red-800';
                default: return 'bg-gray-100 text-gray-800';
            }
        }
        
        function getSentimentText(sentiment) {
            switch(sentiment) {
                case 'positive': return '긍정적';
                case 'negative': return '부정적';
                default: return '중립적';
            }
        }
        
        // 검색 입력 시 엔터키 처리
        document.addEventListener('DOMContentLoaded', () => {
            const searchInput = document.getElementById('search-input');
            searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    searchNews();
                }
            });
        });
    </script>
</body>
</html>
'''

# templates 디렉토리와 HTML 파일 생성을 위한 함수
def create_template_file():
    """HTML 템플릿 파일 생성"""
    import os
    
    # templates 디렉토리 생성
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # static 디렉토리 생성
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # index.html 파일 생성
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)

if __name__ == '__main__':
    create_template_file()
    print("뉴스 분석 AI 서비스 시작...")
    print("http://localhost:8000 에서 확인하세요")
    uvicorn.run("news-analysis-python:app", host="0.0.0.0", port=8000, reload=True)