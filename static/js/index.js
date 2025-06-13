// NEWSIAI/static/js/index.js
// 전역 변수 선언
let currentFilter = null;  // 현재 선택된 필터 상태 저장
let allNews = [];          // 전체 뉴스 데이터 저장 (백엔드에서 받아온 데이터)

// DOM 요소 참조
const searchInput = document.getElementById('search-input');
const newsListContainer = document.getElementById('news-list');
const positiveCountElement = document.getElementById('positive-count');
const negativeCountElement = document.getElementById('negative-count');
const neutralCountElement = document.getElementById('neutral-count');

/**
 * 초기 데이터 로드 함수 (API 호출로 대체)
 */
async function loadData() {
    // 페이지 로드 시에는 API 호출을 하지 않고, 검색 버튼 클릭 시 호출하도록 변경.
    // 따라서 이 함수는 빈 상태로 두거나 제거해도 무방합니다.
    // 기존의 sampleNews는 더 이상 사용되지 않습니다.
    displayNews([]); // 초기에는 뉴스 목록을 비워둡니다.
    displaySentimentCounts(0, 0, 0); // 초기 감성 카운트도 0으로 설정
}

/**
 * 뉴스 데이터를 화면에 표시하는 함수
 * @param {Array} news - 표시할 뉴스 데이터 배열
 */
function displayNews(news) {
    const container = newsListContainer; // 전역 변수 사용
    // 날짜순으로 정렬 (최신순)
    const sortedNews = [...news].sort((a, b) =>
        new Date(b.published_date) - new Date(a.published_date)
    );

    // 각 뉴스 항목을 카드 형태로 렌더링
    if (sortedNews.length === 0) {
        container.innerHTML = '<p class="text-center text-gray-500 py-10">검색 결과가 없습니다. 새로운 검색어를 입력해주세요.</p>';
        return;
    }
    container.innerHTML = sortedNews.map((item, idx) => `
        <div class="bg-white rounded-lg shadow p-6 mb-4 cursor-pointer" onclick="onNewsClick(${idx})">
            <div class="flex justify-between items-start mb-3">
                <h3 class="font-semibold text-gray-900">${item.company}</h3>
                <span class="px-2 py-1 text-xs rounded-full ${getSentimentColor(item.sentiment_category)}">
                    ${getSentimentText(item.sentiment_category)}
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

// 뉴스 카드 클릭 시 동작 함수 (예시: 전체 정보 alert)
function onNewsClick(idx) {
    const item = allNews[idx];
    alert(`제목: ${item.title}\n회사: ${item.company}\n날짜: ${item.published_date}\n요약: ${item.summary}`);
}

/**
 * 감성별 뉴스 필터링 함수
 * @param {string} sentiment - 필터링할 감성 ('positive', 'negative', 'neutral')
 */
function filterNews(sentiment) {
    currentFilter = sentiment;
    const filteredNews = allNews.filter(item => item.sentiment_category === sentiment); // 백엔드 응답 키에 맞춤
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
 * @param {number} positiveCount - 긍정 뉴스 개수
 * @param {number} negativeCount - 부정 뉴스 개수
 * @param {number} neutralCount - 중립 뉴스 개수
 */
function displaySentimentCounts(positiveCount, negativeCount, neutralCount) {
    positiveCountElement.textContent = `${positiveCount}개`;
    negativeCountElement.textContent = `${negativeCount}개`;
    neutralCountElement.textContent = `${neutralCount}개`;
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
        case 'neutral': return 'bg-gray-100 text-gray-800'; // 중립도 명시적으로 추가
        default: return 'bg-gray-100 text-gray-800'; // 알 수 없는 경우 대비
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
        case 'neutral': return '중립적'; // 중립도 명시적으로 추가
        default: return '알 수 없음';

// 로그인 상태 확인 함수
async function checkLoginStatus() {
    try {
        const response = await fetch('/api/check-login');
        const data = await response.json();
        
        const authButtons = document.getElementById('auth-buttons');
        const userInfo = document.getElementById('user-info');
        const usernameDisplay = document.getElementById('username-display');
        
        if (data.loggedIn) {
            // 로그인된 상태
            authButtons.classList.add('hidden');
            userInfo.classList.remove('hidden');
            usernameDisplay.textContent = data.username;
        } else {
            // 로그인되지 않은 상태
            authButtons.classList.remove('hidden');
            userInfo.classList.add('hidden');
        }
    } catch (error) {
        console.error('로그인 상태 확인 중 오류 발생:', error);
    }
}

// 로그아웃 처리 함수
async function handleLogout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST',
        });
        const result = await response.json();
        
        if (result.success) {
            // 로그아웃 성공 시 로그인 페이지로 리다이렉트
            window.location.href = '/login';
        } else {
            alert('로그아웃에 실패했습니다.');
        }
    } catch (error) {
        console.error('로그아웃 중 오류 발생:', error);
        alert('로그아웃 처리 중 오류가 발생했습니다.');
    }
}


    }
}

/**
 * 뉴스 검색 및 분석을 위한 API 호출 함수
 */
async function searchNews() {
    const query = searchInput.value.trim();
    if (!query) {
        alert('검색어를 입력해주세요.');
        return;
    }

    newsListContainer.innerHTML = '<p class="text-center text-gray-500 py-10">뉴스 검색 및 분석 중...</p>';
    displaySentimentCounts(0, 0, 0); // 새로운 검색 시작 시 카운터 초기화

    try {
        // 1. 검색 API 호출
        const searchResponse = await fetch('/search/', { // prefix에서 /api 삭제됨
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        if (!searchResponse.ok) {
            const errorData = await searchResponse.json();
            throw new Error(`검색 API 에러: ${errorData.detail || searchResponse.statusText}`);
        }
        const searchData = await searchResponse.json();

        // 네이버 뉴스 API 응답 구조를 직접 처리
        const newsItems = searchData.data.items || [];
        if (newsItems.length === 0) {
            newsListContainer.innerHTML = '<p class="text-center text-gray-500 py-10">검색 결과가 없습니다.</p>';
            return;
        }

        const descriptions = newsItems.map(item => item.description);
        const titles = newsItems.map(item => item.title);
        const originalLinks = newsItems.map(item => item.originallink);
        const pubDates = newsItems.map(item => item.pubDate);

        // 2. 요약 API 호출 (모든 description을 한 번에 전송)
        const summarizeResponse = await fetch('/summarize/multiple', { // prefix에서 /api 삭제됨
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texts: descriptions })
        });

        if (!summarizeResponse.ok) {
            const errorData = await summarizeResponse.json();
            throw new Error(`요약 API 에러: ${errorData.detail || summarizeResponse.statusText}`);
        }
        const summarizedData = await summarizeResponse.json();

        if (summarizedData.status !== 'success' || !summarizedData.summaries) {
            throw new Error('요약 결과를 가져오지 못했습니다.');
        }

        let positiveCount = 0;
        let negativeCount = 0;
        let neutralCount = 0;
        allNews = []; // 전역 뉴스 데이터 초기화

        // 3. 각 요약된 텍스트에 대해 감성 분석 API 호출 및 데이터 취합
        for (let i = 0; i < summarizedData.summaries.length; i++) {
            const summarizedItem = summarizedData.summaries[i];
            const originalText = summarizedItem.original_text;
            const summaryText = summarizedItem.summary;
            const newsTitle = titles[i]; // 원본 뉴스 제목
            const newsLink = originalLinks[i]; // 원본 뉴스 링크 (사용하려면 HTML 템플릿에 추가)
            const newsPubDate = pubDates[i]; // 원본 뉴스 발행일 (사용하려면 HTML 템플릿에 추가)

            let sentimentCategory = 'neutral'; // 기본값

            if (summaryText) {
                try {
                    const sentimentResponse = await fetch('/sentiment/analyze', { // prefix에서 /api 삭제됨
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ text: summaryText })
                    });

                    if (!sentimentResponse.ok) {
                        const errorData = await sentimentResponse.json();
                        throw new Error(`감성 분석 API 에러: ${errorData.detail || sentimentResponse.statusText}`);
                    }
                    const sentimentData = await sentimentResponse.json();

                    // Python 백엔드의 'final_sentiment' 키를 사용 (긍정, 부정, 중립 등 한글)
                    const finalSentiment = sentimentData.final_sentiment;

                    // 감성 카운트 및 카테고리 설정
                    if (finalSentiment.includes("긍정")) {
                        positiveCount++;
                        sentimentCategory = 'positive';
                    } else if (finalSentiment.includes("부정")) {
                        negativeCount++;
                        sentimentCategory = 'negative';
                    } else if (finalSentiment.includes("중립")) {
                        neutralCount++;
                        sentimentCategory = 'neutral';
                    }

                } catch (sentimentError) {
                    console.error("감성 분석 실패:", sentimentError);
                    // 감성 분석 실패 시에도 중립으로 처리
                    sentimentCategory = 'neutral';
                }
            } else {
                console.warn("요약 실패로 감성 분석을 수행할 수 없습니다.");
                sentimentCategory = 'neutral'; // 요약 실패 시 중립으로 처리
            }

            // 전역 allNews 배열에 추가할 객체 구성
            allNews.push({
                company: "뉴스 기사", // 회사명 정보가 없으므로 임의로 "뉴스 기사"로 설정
                title: newsTitle.replace(/<\/?b>/g, ''), // 제목에서 <b> 태그 제거
                summary: summaryText || originalText.replace(/<\/?b>/g, ''), // 요약 없으면 원문 사용 (<b> 태그 제거)
                published_date: new Date(newsPubDate).toLocaleDateString(), // 발행일 포맷팅
                sentiment_category: sentimentCategory // 필터링을 위한 카테고리
            });
        }

        displayNews(allNews); // 모든 뉴스 표시
        displaySentimentCounts(positiveCount, negativeCount, neutralCount); // 감성 카운트 업데이트

    } catch (error) {
        console.error("전체 프로세스 에러:", error);
        newsListContainer.innerHTML = `<p class="text-center text-red-500 py-10">오류 발생: ${error.message}</p>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadData(); // 초기 데이터 로드 (현재는 빈 값으로 시작)

    // 검색 입력 필드에 엔터키 이벤트 리스너 추가
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            searchNews();
        }
    });

    // 검색 버튼 클릭 이벤트 리스너
    document.querySelector('button[onclick="searchNews()"]').addEventListener('click', searchNews);
});