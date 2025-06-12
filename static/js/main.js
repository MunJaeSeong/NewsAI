// 전역 변수 선언
let currentFilter = null;  // 현재 선택된 필터 상태 저장
let allNews = [];          // 전체 뉴스 데이터 저장
/**
 * 초기 데이터 로드 함수
 */
async function loadData() {
    try {
        allNews = sampleNews;
        displayNews(sampleNews);
        displaySentimentNews(sampleNews);
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
    // 날짜순으로 정렬 (최신순)
    const sortedNews = [...news].sort((a, b) => 
        new Date(b.published_date) - new Date(a.published_date)
    );
    
    // 각 뉴스 항목을 카드 형태로 렌더링
    container.innerHTML = sortedNews.map(item => `
        <div class="bg-white rounded-lg shadow p-6 mb-4">
            <div class="flex justify-between items-start mb-3">
                <h3 class="font-semibold text-gray-900">${item.company}</h3>
                <span class="px-2 py-1 text-xs rounded-full ${getSentimentColor(item.sentiment)}">
                    ${getSentimentText(item.sentiment)}
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
 * 모든 뉴스를 다시 표시
 */
function resetFilter() {
    currentFilter = null;
    displayNews(allNews);
}

/**
 * 감성별 뉴스 개수를 계산하고 표시하는 함수
 * @param {Array} news - 뉴스 데이터 배열
 */
function displaySentimentNews(news) {
    const positiveNews = news.filter(item => item.sentiment === 'positive');
    const negativeNews = news.filter(item => item.sentiment === 'negative');
    const neutralNews = news.filter(item => item.sentiment === 'neutral');

    document.getElementById('positive-count').textContent = `${positiveNews.length}개`;
    document.getElementById('negative-count').textContent = `${negativeNews.length}개`;
    document.getElementById('neutral-count').textContent = `${neutralNews.length}개`;
}

/**
 * 감성에 따른 CSS 클래스 반환 함수
 * @param {string} sentiment - 감성 ('positive', 'negative', 'neutral')
 * @returns {string} - Tailwind CSS 클래스 문자열
 */
function getSentimentColor(sentiment) {
    switch(sentiment) {
        case 'positive': return 'bg-green-100 text-green-800';
        case 'negative': return 'bg-red-100 text-red-800';
        default: return 'bg-gray-100 text-gray-800';
    }
}

/**
 * 감성에 따른 한글 텍스트 반환 함수
 * @param {string} sentiment - 감성 ('positive', 'negative', 'neutral')
 * @returns {string} - 한글 감성 텍스트
 */
function getSentimentText(sentiment) {
    switch(sentiment) {
        case 'positive': return '긍정적';
        case 'negative': return '부정적';
        default: return '중립적';
    }
}

/**
 * 뉴스 검색 함수
 */
function searchNews() {
    const keyword = document.getElementById('search-input').value.trim().toLowerCase();
    if (keyword) {
        const filteredNews = allNews.filter(item => 
            item.company.toLowerCase().includes(keyword) ||
            item.title.toLowerCase().includes(keyword) ||
            item.summary.toLowerCase().includes(keyword)
        );
        displayNews(filteredNews);
    } else {
        displayNews(allNews);
    }
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 초기 데이터 로드
    loadData();
    
    // 검색 입력 필드에 엔터키 이벤트 리스너 추가
    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            searchNews();
        }
    });
}); 