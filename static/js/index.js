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
 * 이 함수는 초기 상태 설정 용도로만 사용됩니다.
 */
async function loadData() {
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
    
    // 이전에 표시된 뉴스를 지우고 다시 그립니다.
    container.innerHTML = sortedNews.map(item => `
        <div class="bg-white rounded-lg shadow p-6 mb-4">
            <div class="flex justify-between items-start mb-3">
                <h3 class="font-semibold text-gray-900">${item.company}</h3>
                <span class="px-2 py-1 text-xs rounded-full ${getSentimentColor(item.sentiment_category)}">
                    ${getSentimentText(item.sentiment_category)}
                </span>
            </div>
            <h2 class="text-lg font-bold mb-2">${item.title}</h2>
            <p class="text-gray-700 mb-3">${item.summary}</p>
            <p class="text-sm text-gray-500">${item.published_date}</p>
        </div>
    `).join('');
}

/**
 * 감성별 뉴스 개수를 화면에 표시하는 함수
 * @param {number} positiveCount - 긍정적 뉴스 개수
 * @param {number} negativeCount - 부정적 뉴스 개수
 * @param {number} neutralCount - 중립적 뉴스 개수
 */
function displaySentimentCounts(positiveCount, negativeCount, neutralCount) {
    positiveCountElement.textContent = `${positiveCount}개`;
    negativeCountElement.textContent = `${negativeCount}개`;
    neutralCountElement.textContent = `${neutralCount}개`;
}

/**
 * 감성 필터링 함수
 * @param {string} sentiment - 'positive', 'negative', 'neutral' 또는 null (전체)
 */
function filterNews(sentiment) {
    currentFilter = sentiment;
    let filteredNews = [];
    if (sentiment) {
        filteredNews = allNews.filter(item => item.sentiment_category === sentiment);
    } else {
        filteredNews = allNews;
    }
    displayNews(filteredNews);
}

/**
 * 필터 초기화 (전체 보기) 함수
 */
function resetFilter() {
    filterNews(null);
}

/**
 * 감성에 따른 Tailwind CSS 색상 클래스 반환 함수
 * @param {string} sentiment - 감성 ('긍정', '부정', '중립')
 * @returns {string} - Tailwind CSS 클래스 문자열
 */
function getSentimentColor(sentiment) {
    switch(sentiment) {
        case '긍정': return 'bg-green-100 text-green-800';
        case '부정': return 'bg-red-100 text-red-800';
        default: return 'bg-gray-100 text-gray-800';
    }
}

/**
 * 감성에 따른 한글 텍스트 반환 함수
 * @param {string} sentiment - 감성 ('긍정', '부정', '중립')
 * @returns {string} - 한글 감성 텍스트
 */
function getSentimentText(sentiment) {
    switch(sentiment) {
        case '긍정': return '긍정적';
        case '부정': return '부정적';
        default: return '중립적';
    }
}

/**
 * 뉴스 검색 함수 (백엔드 API 호출 포함)
 * 이 함수가 실제로 검색을 수행하고 결과를 화면에 표시합니다.
 */
async function processSearchResults() { // searchTerm 인자를 제거하고 searchInput.value를 직접 사용
    const searchTerm = searchInput.value.trim(); // searchInput 전역 변수 사용
    if (!searchTerm) {
        alert("검색어를 입력해주세요.");
        return;
    }

    newsListContainer.innerHTML = `<p class="text-center text-gray-500 py-10">뉴스 검색 중...</p>`;
    displaySentimentCounts(0, 0, 0); // 검색 시작 시 카운트 초기화
    allNews = []; // 모든 뉴스 배열 초기화 (가장 중요!)

    try {
        // 1. 검색 API 호출
        const searchUrl = `/api/search/`;
        const searchPayload = { query: searchTerm };
        const searchResponse = await fetch(searchUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(searchPayload)
        });

        if (!searchResponse.ok) {
            throw new Error(`검색 API 에러: ${searchResponse.status}`);
        }
        const searchData = await searchResponse.json();

        if (searchData.status === 'success' && searchData.data && searchData.data.items) {
            const naverNewsItems = searchData.data.items;
            const descriptions = naverNewsItems.map(item => item.description);

            if (descriptions.length > 0) {
                // 2. 요약 API 호출
                const summarizeUrl = `/api/summarize/multiple`;
                const summarizePayload = { texts: descriptions };
                const summarizeResponse = await fetch(summarizeUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(summarizePayload)
                });

                if (!summarizeResponse.ok) {
                    throw new Error(`요약 API 에러: ${summarizeResponse.status}`);
                }
                const summarizedData = await summarizeResponse.json();

                let positiveCount = 0;
                let negativeCount = 0;
                let neutralCount = 0;

                if (summarizedData.status === 'success' && summarizedData.summaries) {
                    for (let i = 0; i < naverNewsItems.length; i++) {
                        const newsItem = naverNewsItems[i];
                        const newsTitle = newsItem.title;
                        const originalText = newsItem.description;
                        const newsPubDate = newsItem.pubDate;

                        const summaryItem = summarizedData.summaries[i];
                        const summaryText = summaryItem ? summaryItem.summary : null;

                        let sentimentCategory = '중립'; // 기본값

                        if (summaryText) { // 요약이 성공했을 경우에만 감성 분석
                            // 3. 감성 분석 API 호출 (요약된 텍스트 사용)
                            const sentimentUrl = `/api/sentiment/analyze`;
                            const sentimentPayload = { text: summaryText };
                            const sentimentResponse = await fetch(sentimentUrl, {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify(sentimentPayload)
                            });

                            if (sentimentResponse.ok) {
                                const sentimentData = await sentimentResponse.json();
                                // 백엔드의 final_sentiment 결과값에 따라 카테고리 설정
                                if (sentimentData.final_sentiment.includes('긍정')) { // '긍정 (중립에서 조정됨)' 포함 가능성
                                    sentimentCategory = '긍정';
                                    positiveCount++;
                                } else if (sentimentData.final_sentiment.includes('부정')) { // '부정 (중립에서 조정됨)', '부정 (혼합 감성)' 포함 가능성
                                    sentimentCategory = '부정';
                                    negativeCount++;
                                } else {
                                    sentimentCategory = '중립';
                                    neutralCount++;
                                }
                            } else {
                                console.warn(`감성 분석 API 호출 실패 (${sentimentResponse.status}): 요약된 텍스트에 대해 중립 처리`);
                                neutralCount++;
                            }
                        } else {
                            console.warn(`요약 실패: ${summaryItem ? summaryItem.error : '알 수 없는 오류'}. 원본 텍스트에 대해 중립 처리.`);
                            neutralCount++;
                        }
                        
                        // 전역 allNews 배열에 추가할 객체 구성
                        allNews.push({
                            company: "뉴스 기사", 
                            title: newsTitle.replace(/<\/?b>/g, ''), 
                            summary: summaryText || originalText.replace(/<\/?b>/g, ''), 
                            published_date: new Date(newsPubDate).toLocaleDateString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\. /g, '.').replace(/\.$/, ''), 
                            sentiment_category: sentimentCategory 
                        });
                    }
                } else {
                    console.error("요약 API 응답 형식이 올바르지 않습니다.");
                    newsListContainer.innerHTML = `<p class="text-center text-red-500 py-10">요약 결과를 처리할 수 없습니다.</p>`;
                }
                
                displayNews(allNews); // 모든 뉴스 표시
                displaySentimentCounts(positiveCount, negativeCount, neutralCount); // 감성 카운트 업데이트

            } else {
                newsListContainer.innerHTML = `<p class="text-center text-gray-500 py-10">검색어 '${searchTerm}'에 대한 뉴스를 찾을 수 없습니다.</p>`;
            }
        } else {
            newsListContainer.innerHTML = `<p class="text-center text-red-500 py-10">검색 결과를 가져오는 데 실패했습니다.</p>`;
        }
    } catch (error) {
        console.error("전체 프로세스 에러:", error);
        newsListContainer.innerHTML = `<p class="text-center text-red-500 py-10">오류 발생: ${error.message}</p>`;
    }
}

// 페이지 로드 시 초기화 및 이벤트 리스너 설정
document.addEventListener('DOMContentLoaded', () => {
    loadData(); 
    
    // 검색 버튼 클릭 이벤트 리스너 (processSearchResults 호출로 변경)
    document.getElementById('search-button').addEventListener('click', () => {
        processSearchResults();
    });

    // 엔터 키 이벤트 리스너 (input 필드에서 엔터 입력 시 검색)
    document.getElementById('search-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault(); // 기본 Enter 동작(폼 제출 등) 방지
            processSearchResults();
        }
    });

    // 필터링 버튼 이벤트 리스너 (HTML onclick은 그대로 유지)
    // 예시: document.getElementById('positive-filter-button').addEventListener('click', () => filterNews('긍정'));
    // HTML에 onclick="filterNews('긍정')" 등이 있다면 JS에서 따로 추가할 필요 없음.
});