# Week 3: API 통합 클라이언트 및 에이전트 협업 체계 구축

Week 3에서는 다양한 공공 데이터 및 소셜 데이터 API를 통합 관리할 수 있는 가벼운 아키텍처를 구축하고, 효율적인 학습 및 협업을 위한 AI 에이전트/스킬 시스템을 도입했습니다.

## 📋 학습 및 실습 성과 (2026-04-10)

### 1. 통합 API 클라이언트 아키텍처 수립
기존의 파편화된 API 호출 방식을 고성능/유지보수 중심의 통합 구조로 리팩토링했습니다.
- **다중 서비스 지원**: 서울시(지하철, 따릉이), 관세청(전국 무역통계), 네이버(데이터랩 검색어 트렌드) API 통합 연동.
- **Pandera 기반 데이터 검증**: Pydantic DTO의 오버헤드를 제거하고, Pandera `DataFrameModel`을 사용하여 데이터 검증과 Pandas 변환을 최적화했습니다. (중첩 데이터 평탄화 로직 포함)
- **설정 중앙화**: `config.py`와 `.env`를 연동하여 인증 키와 URL을 안전하고 체계적으로 관리합니다.

### 2. AI 에이전트 및 스킬 협업 시스템 도입
AI 어시스턴트(Antigravity)를 단순한 도구가 아닌 시니어 멘토 에이전트로 정의하고, 반복되는 핵심 지식을 **Skills**로 자산화했습니다.
- **[Agents.md](../agents.md)**: AI의 역할(Senior Mentor)과 책임 범위 정의.
- **[Skills.md](../skills.md)**: 프로젝트 표준 가이드 인덱스 구축.
- **핵심 기술 정의**: 
    - [API 수집 전문가 기술](../skills/api_clients.md): 클라이언트 구축 표준 패턴 명문화.
    - [트러블슈팅 로그 관리 기술](../skills/troubleshooting.md): 디버깅 과정 자산화 규칙 수립.
    - [학습 중심 Git 워크플로우](../skills/git_workflow.md): 학습 이력 보존을 위한 브랜치/커밋 전략 수립.

### 3. 트러블슈팅 및 지식 자산화
실습 중 발생한 기술적 난관을 [Troubleshooting Log](./troubleshooting/2026-04-10.md)에 상세히 기록하여 동일한 실수를 방지하고 문제 해결 역량을 강화했습니다.
- **핵심 디버깅**: Pydantic-Pandera 메타클래스 충돌 이슈, 환경 변수 명령 오타 매핑 해결 등.

---

## 💻 주요 소스 코드
- [seoul_client.py](seoul_client.py): 서울시 지하철 및 따릉이 통합 클라이언트
- [nation_trade_client.py](nation_trade_client.py): 공공데이터포털 전국 무역통계 클라이언트
- [naver_client.py](naver_client.py): 네이버 검색어 트렌드 API 클라이언트
- [openapi_practice.ipynb](openapi_practice.ipynb): 인터랙티브 데이터 분석 및 지도 시각화(Folium) 실습

## 🛠 사용된 기술 스택
- **Language**: Python 3.13+
- **Environment Management**: `uv`, `python-dotenv`
- **Data Analysis**: `pandas`, `pandera`, `folium` (지도 시각화)
- **Project Structure**: Centralized Config, Functional API Clients
