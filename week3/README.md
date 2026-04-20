# Week 3: External Data Integration & Web Scraping

3주차에서는 **OpenAPI(정형 데이터)**와 **Web Scraping(비정형 데이터)**을 결합하여, 외부 데이터를 체계적으로 수집하고 정제하는 데이터 파이프라인 구조를 학습했습니다.

---

## 📋 주요 실습 및 기술적 현황

### 🔵 Theme 1: API 통합 클라이언트 구조 (2026-04-10)
파편화된 API 호출 방식을 유지보수와 확장성을 고려한 통합 구조로 재설계했습니다.
- **다중 서비스 연동**: 서울시(지하철, 따릉이), 관세청(전국 무역통계), 네이버 데이터랩 검색어 트렌드 API 구축.
- **Pandera 기반 데이터 검증**: `DataFrameModel`을 활용하여 데이터 수집 시 타입 검증과 Pandas 변환 과정을 단일화.
- **설정 중앙 관리**: `config.py`와 `.env`를 연동하여 인증 키와 엔드포인트를 규격화된 방식으로 관리.
- **[4/10 트러블슈팅 리포트](./troubleshooting/2026-04-10.md)**: 메타클래스 충돌 및 API 형식 불일치 해결 기록.

### 🔴 Theme 2: 멀티 사이트 웹 스크래핑 아키텍처 (2026-04-13)
사이트별 구조와 데이터 렌더링 방식에 따른 대응 전략을 수립하고 구현했습니다.
- **Hybrid Automation**: `Playwright`의 브라우저 로직과 `BeautifulSoup`의 HTML 파싱을 결합하여 동적 정렬(네이버 웹툰) 데이터 수집 처리.
- **Internal API 활용**: 네트워크 패킷 분석으로 멜론 좋아요 API를 식별하고, **Batch Request**(다중 ID 일괄 요청)를 통해 데이터 수집 단계를 효율화.
- **계층 구조 기반 선택자**: 빌보드와 같이 클래스명이 유동적인 사이트에서 안정적인 데이터 추출을 위해 **DOM 계층 선후 관계**를 활용한 선택자 설계.
- **[4/13 트러블슈팅 리포트](./troubleshooting/2026-04-13.md)**: Jupyter 이벤트 루프 충돌 대응, 봇 탐지 우회 헤더 설정, Bare except 지양(PEP 8) 등.

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북
- [openapi_practice.ipynb](openapi_practice.ipynb): API 클라이언트 구현, 데이터 평탄화 및 Folium 시각화.
- [web_scraping_practice.ipynb](web_scraping_practice.ipynb): YES24, 멜론, 빌보드, 네이버 웹툰 스크래핑 구현체.

### 🛠️ API 클라이언트 모듈
- [seoul_client.py](seoul_client.py): 서울시 데이터 수집 모듈.
- [nation_trade_client.py](nation_trade_client.py): 공공데이터포털 무역통계 수집 모듈.
- [naver_client.py](naver_client.py): 네이버 검색어 트렌드 수집 모듈.

---

## 🛠️ 사용 기술 및 의존성
- **Data Engineering**: `Pandas`, `Pandera`, `NumPy`
- **Web Scraping**: `Playwright`, `BeautifulSoup4`, `Requests`
- **Management**: `uv` (Package Manager), `python-dotenv`
- **Visualization**: `Folium`, `Matplotlib`, `Seaborn`

---
> [!NOTE]
> 본 주차의 학습 목표는 데이터의 수집 방식(API vs Scraping)에 따른 기술적 특징을 이해하고, 실무에서 마주할 수 있는 구조적 변화에 대응하는 '견고한 수집 환경'을 구축하는 데 있습니다.
