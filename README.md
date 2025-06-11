# NewsMind AI

뉴스 분석 AI 서비스입니다. 실시간으로 뉴스를 검색하고 분석할 수 있는 웹 애플리케이션입니다.

## 주요 기능

- 뉴스 검색 및 분석
- 관심 회사 하이라이트
- 검색 기록 관리
- 감성 분석 및 영향도 평가

## 설치 방법

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
python news-analysis-python.py
```

5. 웹 브라우저에서 접속
```
http://localhost:8000
```

## 기술 스택

- Backend: FastAPI
- Frontend: HTML, JavaScript, TailwindCSS
- Database: SQLite

## 라이선스

MIT License 