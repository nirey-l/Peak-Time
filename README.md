📈 Peak-Time: 실시간 트렌드 분석 및 유행 예측 대시보드
"유행이 정점에 달하는 순간을 데이터로 포착하다"

Peak-Time은 구글 트렌드, 유튜브, 인스타그램 등 다양한 매체의 데이터를 통합 분석하여 2026년 최신 유행의 흐름을 파악하고 시각화하는 데이터 사이언스 프로젝트입니다.

🎯 프로젝트 목표
트렌드 가시화: 산발적인 온라인 데이터를 수집하여 직관적인 유행 지수로 변환.

심층 분석: 특정 키워드(두쫀쿠, 런닝크루 등)의 확산 경로와 대중의 반응을 정밀 분석.

위치 기반 인사이트: 유행이 실제 소비로 이어지는 핫플레이스 밀집도를 지도로 제공.

🛠 기술 스택
Backend & Data Pipeline
언어: Python 3.11+

가상환경: venv (라이브러리 버전 관리)

환경 변수: python-dotenv (.env 파일 보안 관리)

데이터 저장: PyMySQL, SQLAlchemy (선택)

Data Scraping & Analysis
Scraping: Requests, BeautifulSoup, Selenium

Analysis: Pandas, NumPy

API: YouTube Data API v3, Pytrends (Google Trends)

Visualization & Web App
Web App: Streamlit

Visualization: Plotly, Matplotlib, Seaborn, Folium (위치 기반 맵)

💡 주요 기능
1. 실시간 유행어 대시보드 (Real-time Dash)
구글 트렌드 실시간 인기 급상승 검색어 TOP 10 자동 크롤링.

현재 가장 뜨거운 키워드를 메인 화면에 실시간 노출.

2. 키워드 심층 분석 (Deep-dive)
YouTube: API 연동을 통한 조회수, 좋아요, 댓글 수 수집 및 인기도 분석.

Instagram: 셀레니움을 활용한 해시태그 게시물 수 추이 및 확산 속도 분석.

두쫀쿠, 런닝크루, 저당 음식 등 핵심 키워드 사례 연구.

3. 위치 기반 핫플 맵 (Geo-Insights)
심층 분석 내 통합 기능으로 제공.

유행 키워드 관련 매장 및 활동 장소의 데이터 밀집도(Heatmap) 시각화.

특정 지역의 '두쫀쿠' 매장 분포나 '런닝' 주요 코스를 지도에 표시.

📂 시작 가이드
저장소 클론 및 가상환경 설정

Bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
환경 변수(.env) 설정

코드 스니펫
# API Keys
YOUTUBE_API_KEY=발급받은_키

# Database
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=비밀번호
DB_NAME=peak_time_db
애플리케이션 실행

Bash
streamlit run main.py
📅 개발 순서 (Roadmap)
DB 스키마 설계: 데이터 구조 정의 및 MySQL 테이블 생성.

데이터 수집 개발: 매체별(Google, YT, IG) 수집 스크립트 작성.

데이터 전처리: Pandas를 활용한 데이터 정제 및 분석 로직 구현.

UI/UX 구현: Streamlit을 활용한 인터랙티브 대시보드 완성.