# NewsMind AI - 뉴스 분석 서비스

뉴스 데이터를 분석하고 시각화하는 웹 애플리케이션입니다.

## 주요 기능

1. 뉴스 데이터 표시 및 필터링
   - 날짜순으로 뉴스 정렬
   - 감성(긍정/부정/중립)별 필터링
2. 회사 정보 관리
   - 관심 회사 목록 조회
3. 검색 기능
   - 뉴스 검색
   - 검색 기록 관리
4. 감성 분석
   - 뉴스의 감성을 긍정/부정/중립으로 분류
   - 감성별 뉴스 개수 표시

## 기술 스택

- Frontend
  - HTML5
  - Tailwind CSS
  - JavaScript (Vanilla)
- Backend
  - FastAPI
  - Python 3.8+

## 설치 및 실행

1. 저장소 클론
```bash
git clone https://github.com/MunJaeSeong/NewsAI.git
cd NewsAI
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 서버 실행
```bash
python main.py
```

5. 웹 브라우저에서 접속
```
http://localhost:8000
```

## 프로젝트 구조

```
NewsAI/
├── main.py              # 메인 애플리케이션 파일
├── router.py            # 라우터 설정
├── requirements.txt     # Python 의존성
├── static/             # 정적 파일
│   └── js/
│       └── index.js    # 프론트엔드 JavaScript
└── templates/          # HTML 템플릿
    └── index.html      # 메인 페이지
```

## 라이선스

MIT License
