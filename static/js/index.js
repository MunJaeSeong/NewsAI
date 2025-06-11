// 전역 변수 선언
let currentFilter = null;  // 현재 선택된 필터 상태 저장
let allNews = [];          // 전체 뉴스 데이터 저장

// 감성별 CSS 클래스와 텍스트 매핑
const sentimentConfig = {
    positive: {
        color: 'bg-green-100 text-green-800',
        text: '긍정적'
    },
    negative: {
        color: 'bg-red-100 text-red-800',
        text: '부정적'
    },
    neutral: {
        color: 'bg-gray-100 text-gray-800',
        text: '중립적'
    }
};

/**
 * 초기 데이터 로드 함수
 */
async function loadData() {
    try {
        // TODO: 실제 API 호출로 대체
        // const response = await fetch('/api/news');
        // allNews = await response.json();
        allNews = [];
        displayNews(allNews);
        updateSentimentCounts(allNews);
    } catch (error) {
        console.error('데이터 로딩 오류:', error);
    }
}

/**
 * 뉴스 데이터를 화면에 표시하는 함수
 * @param {Array} news - 표시할 뉴스 데이터 배열
 */
function displayNews(news) {
    const container = document.getElementById('news-list');
    if (!container) return;

    // 날짜순으로 정렬 (최신순)
    const sortedNews = [...news].sort((a, b) => 
        new Date(b.published_date) - new Date(a.published_date)
    );
    
    // 각 뉴스 항목을 카드 형태로 렌더링
    container.innerHTML = sortedNews.map(item => `
        <div class="bg-white rounded-lg shadow p-6 mb-4">
            <div class="flex justify-between items-start mb-3">
                <h3 class="font-semibold text-gray-900">${item.company}</h3>
                <span class="px-2 py-1 text-xs rounded-full ${sentimentConfig[item.sentiment].color}">
                    ${sentimentConfig[item.sentiment].text}
                </span>
            </div>
            <h2 class="text-lg font-bold mb-2">${item.title}</h2>
            <p class="text-gray-700 mb-3">${item.summary}</p>
            <div class="text-sm text-gray-500">
                <span>${item.published_date}</span>
            </div>
        </div>
    `).join('');
}

/**
 * 감성별 뉴스 필터링 함수
 * @param {string} sentiment - 필터링할 감성 ('positive', 'negative', 'neutral')
 */
function filterNews(sentiment) {
    currentFilter = sentiment;
    const filteredNews = allNews.filter(item => item.sentiment === sentiment);
    displayNews(filteredNews);
}

/**
 * 필터 초기화 함수
 */
function resetFilter() {
    currentFilter = null;
    displayNews(allNews);
}

/**
 * 감성별 뉴스 개수를 계산하고 표시하는 함수
 * @param {Array} news - 뉴스 데이터 배열
 */
function updateSentimentCounts(news) {
    const counts = {
        positive: 0,
        negative: 0,
        neutral: 0
    };

    news.forEach(item => {
        counts[item.sentiment]++;
    });

    Object.entries(counts).forEach(([sentiment, count]) => {
        const element = document.getElementById(`${sentiment}-count`);
        if (element) {
            element.textContent = `${count}개`;
        }
    });
}

/**
 * 뉴스 검색 함수
 */
function searchNews() {
    const keyword = document.getElementById('search-input')?.value.trim().toLowerCase();
    if (!keyword) {
        displayNews(allNews);
        return;
    }

    const filteredNews = allNews.filter(item => 
        item.company.toLowerCase().includes(keyword) ||
        item.title.toLowerCase().includes(keyword) ||
        item.summary.toLowerCase().includes(keyword)
    );
    displayNews(filteredNews);
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 초기 데이터 로드
    loadData();
    
    // 검색 입력 필드에 엔터키 이벤트 리스너 추가
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                searchNews();
            }
        });
    }

    // 필터 버튼 이벤트 리스너 추가
    const filterButtons = document.querySelectorAll('[data-filter]');
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const sentiment = button.getAttribute('data-filter');
            if (sentiment) {
                filterNews(sentiment);
            }
        });
    });

    // 필터 초기화 버튼 이벤트 리스너 추가
    const resetButton = document.getElementById('reset-filter');
    if (resetButton) {
        resetButton.addEventListener('click', resetFilter);
    }
}); 