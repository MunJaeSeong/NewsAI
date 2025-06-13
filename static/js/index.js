// // NEWSIAI/static/js/index.js
// // 전역 변수 선언
// let currentFilter = null;  // 현재 선택된 필터 상태 저장
// let allNews = [];          // 전체 뉴스 데이터 저장 (백엔드에서 받아온 데이터)

// // DOM 요소 참조
// const searchInput = document.getElementById('search-input');
// const newsListContainer = document.getElementById('news-list');
// const positiveCountElement = document.getElementById('positive-count');
// const negativeCountElement = document.getElementById('negative-count');
// const neutralCountElement = document.getElementById('neutral-count');

// /**
//  * 초기 데이터 로드 함수 (API 호출로 대체)
//  */
// async function loadData() {
//     // 페이지 로드 시에는 API 호출을 하지 않고, 검색 버튼 클릭 시 호출하도록 변경.
//     // 따라서 이 함수는 빈 상태로 두거나 제거해도 무방합니다.
//     // 기존의 sampleNews는 더 이상 사용되지 않습니다.
//     displayNews([]); // 초기에는 뉴스 목록을 비워둡니다.
//     displaySentimentCounts(0, 0, 0); // 초기 감성 카운트도 0으로 설정
// }

// /**
//  * 뉴스 데이터를 화면에 표시하는 함수
//  * @param {Array} news - 표시할 뉴스 데이터 배열
//  */
// function displayNews(news) {
//     const container = newsListContainer; // 전역 변수 사용
//     // 날짜순으로 정렬 (최신순)
//     const sortedNews = [...news].sort((a, b) =>
//         new Date(b.published_date) - new Date(a.published_date)
//     );

//     // 각 뉴스 항목을 카드 형태로 렌더링
//     if (sortedNews.length === 0) {
//         container.innerHTML = '<p class="text-center text-gray-500 py-10">검색 결과가 없습니다. 새로운 검색어를 입력해주세요.</p>';
//         return;
//     }

//     container.innerHTML = sortedNews.map(item => `
//         <div class="bg-white rounded-lg shadow p-6 mb-4">
//             <div class="flex justify-between items-start mb-3">
//                 <h3 class="font-semibold text-gray-900">${item.company}</h3>
//                 <span class="px-2 py-1 text-xs rounded-full ${getSentimentColor(item.sentiment_category)}">
//                     ${getSentimentText(item.sentiment_category)}
//                 </span>
//             </div>
//             <h2 class="text-lg font-bold mb-2">${item.title}</h2>
//             <p class="text-gray-700 mb-3">${item.summary}</p>
//             <div class="text-sm text-gray-500">
//                 <span>${item.published_date}</span>
//             </div>
//         </div>
//     `).join('');
// }

// /**
//  * 감성별 뉴스 필터링 함수
//  * @param {string} sentiment - 필터링할 감성 ('positive', 'negative', 'neutral')
//  */
// function filterNews(sentiment) {
//     currentFilter = sentiment;
//     const filteredNews = allNews.filter(item => item.sentiment_category === sentiment); // 백엔드 응답 키에 맞춤
//     displayNews(filteredNews);
// }

// /**
//  * 필터 초기화 함수
//  * 모든 뉴스를 다시 표시
//  */
// function resetFilter() {
//     currentFilter = null;
//     displayNews(allNews);
// }

// /**
//  * 감성별 뉴스 개수를 계산하고 표시하는 함수
//  * @param {number} positiveCount - 긍정 뉴스 개수
//  * @param {number} negativeCount - 부정 뉴스 개수
//  * @param {number} neutralCount - 중립 뉴스 개수
//  */
// function displaySentimentCounts(positiveCount, negativeCount, neutralCount) {
//     positiveCountElement.textContent = `${positiveCount}개`;
//     negativeCountElement.textContent = `${negativeCount}개`;
//     neutralCountElement.textContent = `${neutralCount}개`;
// }


// /**
//  * 감성에 따른 CSS 클래스 반환 함수
//  * @param {string} sentiment - 감성 ('positive', 'negative', 'neutral')
//  * @returns {string} - Tailwind CSS 클래스 문자열
//  */
// function getSentimentColor(sentiment) {
//     switch(sentiment) {
//         case 'positive': return 'bg-green-100 text-green-800';
//         case 'negative': return 'bg-red-100 text-red-800';
//         case 'neutral': return 'bg-gray-100 text-gray-800'; // 중립도 명시적으로 추가
//         default: return 'bg-gray-100 text-gray-800'; // 알 수 없는 경우 대비
//     }
// }

// /**
//  * 감성에 따른 한글 텍스트 반환 함수
//  * @param {string} sentiment - 감성 ('positive', 'negative', 'neutral')
//  * @returns {string} - 한글 감성 텍스트
//  */
// function getSentimentText(sentiment) {
//     switch(sentiment) {
//         case 'positive': return '긍정적';
//         case 'negative': return '부정적';
//         case 'neutral': return '중립적'; // 중립도 명시적으로 추가
//         default: return '알 수 없음';
//     }
// }

// /**
//  * 뉴스 검색 및 분석을 위한 API 호출 함수
//  */
// async function searchNews() {
//     const query = searchInput.value.trim();
//     if (!query) {
//         alert('검색어를 입력해주세요.');
//         return;
//     }

//     newsListContainer.innerHTML = '<p class="text-center text-gray-500 py-10">뉴스 검색 및 분석 중...</p>';
//     displaySentimentCounts(0, 0, 0); // 새로운 검색 시작 시 카운터 초기화

//     try {
//         // 1. 검색 API 호출
//         const searchResponse = await fetch('/api/search/', { // main.py에서 prefix가 /api/search로 변경됨
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ query: query })
//         });

//         if (!searchResponse.ok) {
//             const errorData = await searchResponse.json();
//             throw new Error(`검색 API 에러: ${errorData.detail || searchResponse.statusText}`);
//         }
//         const searchData = await searchResponse.json();

//         // 네이버 뉴스 API 응답 구조를 직접 처리
//         const newsItems = searchData.data.items || [];
//         if (newsItems.length === 0) {
//             newsListContainer.innerHTML = '<p class="text-center text-gray-500 py-10">검색 결과가 없습니다.</p>';
//             return;
//         }

//         const descriptions = newsItems.map(item => item.description);
//         const titles = newsItems.map(item => item.title);
//         const originalLinks = newsItems.map(item => item.originallink);
//         const pubDates = newsItems.map(item => item.pubDate);

//         // 2. 요약 API 호출 (모든 description을 한 번에 전송)
//         const summarizeResponse = await fetch('/api/summarize/multiple', { // main.py에서 prefix가 /api/summarize로 변경됨
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ texts: descriptions })
//         });

//         if (!summarizeResponse.ok) {
//             const errorData = await summarizeResponse.json();
//             throw new Error(`요약 API 에러: ${errorData.detail || summarizeResponse.statusText}`);
//         }
//         const summarizedData = await summarizeResponse.json();

//         if (summarizedData.status !== 'success' || !summarizedData.summaries) {
//             throw new Error('요약 결과를 가져오지 못했습니다.');
//         }

//         let positiveCount = 0;
//         let negativeCount = 0;
//         let neutralCount = 0;
//         allNews = []; // 전역 뉴스 데이터 초기화

//         // 3. 각 요약된 텍스트에 대해 감성 분석 API 호출 및 데이터 취합
//         for (let i = 0; i < summarizedData.summaries.length; i++) {
//             const summarizedItem = summarizedData.summaries[i];
//             const originalText = summarizedItem.original_text;
//             const summaryText = summarizedItem.summary;
//             const newsTitle = titles[i]; // 원본 뉴스 제목
//             const newsLink = originalLinks[i]; // 원본 뉴스 링크 (사용하려면 HTML 템플릿에 추가)
//             const newsPubDate = pubDates[i]; // 원본 뉴스 발행일 (사용하려면 HTML 템플릿에 추가)

//             let sentimentCategory = 'neutral'; // 기본값

//             if (summaryText) {
//                 try {
//                     const sentimentResponse = await fetch('/api/sentiment/analyze', { // main.py에서 prefix가 /api/sentiment로 변경됨
//                         method: 'POST',
//                         headers: { 'Content-Type': 'application/json' },
//                         body: JSON.stringify({ text: summaryText })
//                     });

//                     if (!sentimentResponse.ok) {
//                         const errorData = await sentimentResponse.json();
//                         throw new Error(`감성 분석 API 에러: ${errorData.detail || sentimentResponse.statusText}`);
//                     }
//                     const sentimentData = await sentimentResponse.json();

//                     // Python 백엔드의 'final_sentiment' 키를 사용 (긍정, 부정, 중립 등 한글)
//                     const finalSentiment = sentimentData.final_sentiment;

//                     // 감성 카운트 및 카테고리 설정
//                     if (finalSentiment.includes("긍정")) {
//                         positiveCount++;
//                         sentimentCategory = 'positive';
//                     } else if (finalSentiment.includes("부정")) {
//                         negativeCount++;
//                         sentimentCategory = 'negative';
//                     } else if (finalSentiment.includes("중립")) {
//                         neutralCount++;
//                         sentimentCategory = 'neutral';
//                     }

//                 } catch (sentimentError) {
//                     console.error("감성 분석 실패:", sentimentError);
//                     // 감성 분석 실패 시에도 중립으로 처리
//                     sentimentCategory = 'neutral';
//                 }
//             } else {
//                 console.warn("요약 실패로 감성 분석을 수행할 수 없습니다.");
//                 sentimentCategory = 'neutral'; // 요약 실패 시 중립으로 처리
//             }

//             // 전역 allNews 배열에 추가할 객체 구성
//             allNews.push({
//                 company: "뉴스 기사", // 회사명 정보가 없으므로 임의로 "뉴스 기사"로 설정
//                 title: newsTitle.replace(/<\/?b>/g, ''), // 제목에서 <b> 태그 제거
//                 summary: summaryText || originalText.replace(/<\/?b>/g, ''), // 요약 없으면 원문 사용 (<b> 태그 제거)
//                 published_date: new Date(newsPubDate).toLocaleDateString(), // 발행일 포맷팅
//                 sentiment_category: sentimentCategory // 필터링을 위한 카테고리
//             });
//         }

//         displayNews(allNews); // 모든 뉴스 표시
//         displaySentimentCounts(positiveCount, negativeCount, neutralCount); // 감성 카운트 업데이트

//     } catch (error) {
//         console.error("전체 프로세스 에러:", error);
//         newsListContainer.innerHTML = `<p class="text-center text-red-500 py-10">오류 발생: ${error.message}</p>`;
//     }
// }

// // 페이지 로드 시 초기화
// document.addEventListener('DOMContentLoaded', () => {
//     loadData(); // 초기 데이터 로드 (현재는 빈 값으로 시작)

//     // 검색 입력 필드에 엔터키 이벤트 리스너 추가
//     searchInput.addEventListener('keydown', (e) => {
//         if (e.key === 'Enter') {
//             searchNews();
//         }
//     });

//     // 검색 버튼 클릭 이벤트 리스너
//     document.querySelector('button[onclick="searchNews()"]').addEventListener('click', searchNews);
// });

// NEWSIAI/static/js/index.js
// 전역 변수 선언
let currentFilter = null;  // 현재 선택된 필터 상태 저장
let allNews = [];          // 전체 뉴스 데이터 저장 (백엔드에서 받아온 데이터)

// DOM 요소 참조
const searchInput = document.getElementById('search-input');
const newsListContainer = document.getElementById('news-list');
const positiveCountElement = document.getElementById('positive-count');
const negativeCountElement = document.getElementById('negative-count');
const neutralCountElement = document.getElementById('neutral-count');
const searchButton = document.getElementById('search-button'); // 검색 버튼 ID 추가

/**
 * 초기 데이터 로드 함수 (API 호출로 대체)
 * 페이지 로드 시에는 API 호출을 하지 않고, 검색 버튼 클릭 시 호출하도록 변경.
 * 따라서 이 함수는 초기 UI 설정만 담당합니다.
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
    // 네이버 뉴스 API의 pubDate는 "Wed, 12 Jun 2024 10:00:00 +0900" 형식입니다.
    // Date 객체로 직접 변환 가능합니다.
    const sortedNews = [...news].sort((a, b) =>
        new Date(b.published_date) - new Date(a.published_date)
    );
    
    // 이전에 표시된 뉴스를 지우고 다시 그립니다.
    container.innerHTML = sortedNews.map(item => `
        <div class="bg-white rounded-lg shadow p-6 mb-4">
            <div class="flex justify-between items-start mb-3">
                <h3 class="font-semibold text-gray-900">${item.company || '출처 불명'}</h3>
                <span class="px-2 py-1 text-xs rounded-full ${getSentimentColor(item.sentiment_category)}">
                    ${getSentimentText(item.sentiment_category)}
                </span>
            </div>
            <h2 class="text-lg font-bold mb-2">
                <a href="${item.original_link || '#'}" target="_blank" class="text-blue-600 hover:underline">
                    ${item.title}
                </a>
            </h2>
            <p class="text-gray-700 mb-3">${item.summary}</p>
            <div class="text-sm text-gray-500">
                <span>${new Date(item.published_date).toLocaleDateString()}</span>
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
    // allNews 배열에는 sentiment_category가 'positive', 'negative', 'neutral'로 저장됩니다.
    const filteredNews = allNews.filter(item => item.sentiment_category === sentiment);
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
 * 뉴스 검색 및 분석을 위한 API 호출 함수 (핵심 수정 부분)
 */
async function processSearchResults() { // searchTerm 인자를 제거하고 searchInput.value를 직접 사용
    const searchTerm = searchInput.value.trim(); // searchInput 전역 변수 사용
    if (!searchTerm) {
        alert("검색어를 입력해주세요.");
        return;
    }

    newsListContainer.innerHTML = '<p class="text-center text-gray-500 py-10">뉴스 검색 및 분석 중...</p>';
    displaySentimentCounts(0, 0, 0); // 새로운 검색 시작 시 카운터 초기화
    allNews = []; // 새로운 검색 시작 시 전역 뉴스 데이터 초기화
    currentFilter = null; // 필터 초기화

    try {
        // 1. 검색 API 호출
        // 네이버 검색 API 응답 구조가 `{ "data": { "items": [...] } }` 형태이므로 `searchData.data.items`로 접근
        const searchResponse = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(searchPayload)
        });

        if (!searchResponse.ok) {
            throw new Error(`검색 API 에러: ${searchResponse.status}`);
        }
        const searchData = await searchResponse.json();
        const newsItems = searchData.data.items || []; // `searchData.data` 아래에 `items`가 있다고 가정

        if (newsItems.length === 0) {
            newsListContainer.innerHTML = '<p class="text-center text-gray-500 py-10">검색 결과가 없습니다.</p>';
            return;
        }

        const descriptions = newsItems.map(item => item.description);
        const titles = newsItems.map(item => item.title);
        const originalLinks = newsItems.map(item => item.originallink);
        const pubDates = newsItems.map(item => item.pubDate); // 네이버 API pubDate 형식: "Thu, 13 Jun 2025 05:34:16 +0900"

        // 2. 요약 API 호출 (모든 description을 한 번에 전송)
        const summarizeResponse = await fetch('/api/summarize/multiple', {
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

        // 3. 요약된 텍스트들을 모아 **배치 감성 분석 API** 호출 (여기서 성능 개선!)
        const textsForSentiment = summarizedData.summaries.map(s => s.summary || s.original_text);
        let sentimentBatchResults = [];

        if (textsForSentiment.length > 0) {
            const sentimentBatchResponse = await fetch('/api/sentiment/analyze/batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ texts: textsForSentiment })
            });

            if (!sentimentBatchResponse.ok) {
                const errorData = await sentimentBatchResponse.json();
                throw new Error(`감성 분석 배치 API 에러: ${errorData.detail || sentimentBatchResponse.statusText}`);
            }
            const sentimentBatchData = await sentimentBatchResponse.json();
            sentimentBatchResults = sentimentBatchData.results || [];
        }

        let positiveCount = 0;
        let negativeCount = 0;
        let neutralCount = 0;

        // 4. 모든 데이터를 통합하고 전역 allNews 배열에 저장
        for (let i = 0; i < newsItems.length; i++) {
            const newsItem = newsItems[i]; // 원본 네이버 뉴스 아이템
            const summarizedItem = summarizedData.summaries[i]; // 해당 인덱스의 요약 결과
            const sentimentResult = sentimentBatchResults[i]; // 해당 인덱스의 감성 분석 배치 결과

            const newsTitle = newsItem.title ? newsItem.title.replace(/<\/?b>/g, '') : '제목 없음';
            const newsSummary = summarizedItem ? (summarizedItem.summary || summarizedItem.original_text.replace(/<\/?b>/g, '')) : newsItem.description.replace(/<\/?b>/g, '');
            const newsLink = newsItem.originallink || newsItem.link || '#'; // originallink 우선, 없으면 link 사용
            const newsPubDate = newsItem.pubDate || '';

            let sentimentCategory = 'neutral';
            if (sentimentResult && sentimentResult.sentiment) {
                // 백엔드에서 받은 감성 라벨에 따라 카테고리 설정 (예: '긍정', '부정', '중립')
                switch (sentimentResult.sentiment) {
                    case '긍정':
                        positiveCount++;
                        sentimentCategory = 'positive';
                        break;
                    case '부정':
                        negativeCount++;
                        sentimentCategory = 'negative';
                        break;
                    case '중립':
                        neutralCount++;
                        sentimentCategory = 'neutral';
                        break;
                    default:
                        neutralCount++; // 알 수 없는 감성은 중립으로 처리
                        sentimentCategory = 'neutral';
                        break;
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
                neutralCount++; // 감성 결과가 없는 경우도 중립으로 처리
            }
            
            // `allNews` 배열에 저장할 데이터 형식 일치시키기
            allNews.push({
                company: getNewsCompany(newsLink), // 링크에서 회사명 추출 (추가 함수 필요)
                title: newsTitle,
                summary: newsSummary,
                original_link: newsLink, // 원본 링크 추가
                published_date: newsPubDate, // 원본 pubDate 유지 (displayNews에서 포맷팅)
                sentiment_category: sentimentCategory
            });
        }
    } catch (error) {
        console.error("전체 프로세스 에러:", error);
        newsListContainer.innerHTML = `<p class="text-center text-red-500 py-10">오류 발생: ${error.message}</p>`;
    }
}

/**
 * 뉴스 링크에서 회사 이름을 추론하는 헬퍼 함수
 * 실제 언론사 이름을 정확히 매핑하려면 더 복잡한 로직이 필요합니다.
 * 여기서는 간단하게 도메인에서 이름을 추출하거나 '출처 불명'으로 표시합니다.
 * @param {string} link - 뉴스 원본 링크
 * @returns {string} - 추정된 회사 이름
 */
function getNewsCompany(link) {
    try {
        const url = new URL(link);
        const hostname = url.hostname;
        // 일반적으로 도메인에서 '.co.kr', '.com', '.net' 등을 제거하고 앞 부분 사용
        // 예: 'news.naver.com' -> '네이버 뉴스'
        //    'www.yonhapnews.co.kr' -> '연합뉴스'
        if (hostname.includes('naver.com')) return '네이버 뉴스';
        if (hostname.includes('daum.net')) return '다음 뉴스';
        if (hostname.includes('yonhapnews.co.kr')) return '연합뉴스';
        if (hostname.includes('chosun.com')) return '조선일보';
        if (hostname.includes('joongang.co.kr')) return '중앙일보';
        if (hostname.includes('donga.com')) return '동아일보';
        // 기타 언론사 추가 가능
        const parts = hostname.split('.');
        if (parts.length >= 2) {
            return parts[parts.length - 2].charAt(0).toUpperCase() + parts[parts.length - 2].slice(1);
        }
        return '출처 불명';
    } catch (e) {
        return '출처 불명';
    }
}


// 페이지 로드 시 초기화 및 이벤트 리스너 추가
document.addEventListener('DOMContentLoaded', () => {
    loadData(); 
    
    // 검색 버튼 클릭 이벤트 리스너 (processSearchResults 호출로 변경)
    document.getElementById('search-button').addEventListener('click', () => {
        processSearchResults();
    });

    // 검색 입력 필드에 엔터키 이벤트 리스너 추가
    if (searchInput) {
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                searchNews();
            }
        });
    }
    
    // 검색 버튼 클릭 이벤트 리스너
    // HTML에 `<button id="search-button" onclick="searchNews()">검색</button>` 또는
    // `<button onclick="searchNews()">검색</button>` 형태로 있을 수 있습니다.
    // 여기서는 ID가 'search-button'인 요소를 직접 찾거나, 없을 경우 기존 onclick 속성 활용을 가정합니다.
    if (searchButton) {
        searchButton.addEventListener('click', searchNews);
    } else {
        // ID가 없는 경우, DOMContentLoaded 전에 이미 onclick 속성이 설정되어 있을 수 있습니다.
        // 또는 HTML에 직접 onclick="searchNews()"가 붙어있다면, 별도 리스너 추가 불필요
        console.warn("Search button with ID 'search-button' not found. Ensure it has the correct ID or onclick attribute.");
    }

    // 필터링 버튼 이벤트 리스너 추가 (예시)
    // HTML에 다음과 같은 버튼들이 있다고 가정합니다:
    // <button id="filter-positive" onclick="filterNews('positive')">긍정</button>
    // <button id="filter-negative" onclick="filterNews('negative')">부정</button>
    // <button id="filter-neutral" onclick="filterNews('neutral')">중립</button>
    // <button id="filter-all" onclick="resetFilter()">전체</button>

    document.getElementById('filter-positive')?.addEventListener('click', () => filterNews('positive'));
    document.getElementById('filter-negative')?.addEventListener('click', () => filterNews('negative'));
    document.getElementById('filter-neutral')?.addEventListener('click', () => filterNews('neutral'));
    document.getElementById('filter-all')?.addEventListener('click', resetFilter);

});