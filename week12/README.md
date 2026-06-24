# Week 12: 실습 저장소 (12주차)

12주차 실습을 위한 학습 저장소입니다. 이번 주차의 학습 내용과 실습 코드를 기록합니다.

---

## 🗓️ 학습 로드맵 및 수행 결과

### 🟡 Theme 47: CrewAI 프레임워크 스킬 정립 및 로컬 LLM 연동 (2026-06-23)
- **핵심 키워드**: CrewAI, Local LLM, Ollama, Rich Logging, Agent Scaffolding, SKILL.md
- **주요 실습**:
    - **CrewAI 스킬 체계 리팩토링 및 셋업**: `getting-started`, `ask-doc` 스킬 파일들을 구조화하고 인덱스([SKILLS.md](file:///home/hong/project/ai-camp-note/SKILLS.md))에 정식 등록
    - **로컬 LLM (Ollama) 연동 구조 설계**: CrewAI `LLM` 모듈을 활용하여 로컬 구동 중인 Ollama 모델(`ollama/gemma-...`)을 연결하는 속성 설정 구현 및 WSL2 네트워크 게이트웨이 연동 분석
    - **CrewAI Rich Logger 분석**: 크루 실행 시 터미널을 장식하는 Rich Panel 출력 원리(`verbose` 모드) 및 로그 제어 옵션 파악

### 🟡 Theme 48: 실시간 토스증권 API 연동 및 CrewAI 반도체/IT 2사 비교 대시보드 구축 (2026-06-24)
- **핵심 키워드**: Toss Securities API, CrewAI, Pydantic Structured Output, Streamlit, Candlestick Chart, Exception Propagation
- **주요 실습**:
    - **토스증권 Client SDK 구현**: OAuth2 인증 정보 캐싱 및 실시간 시세/캔들/호가 조회. API 오작동 및 Key 유실 대응을 위한 모의 시뮬레이션 모드 설계
    - **에이전트 기술 지표 내재화**: LLM 환각 차단을 위해 툴 내부에서 Pandas를 사용해 MA5, MA20, RSI를 연산하여 반환
    - **Pydantic 구조화 출력 바인딩**: `StrategyReport` 모델 기반으로 CrewAI 출력을 JSON 규격화하여 UI 렌더링 시 HTML 및 CSS 컴포넌트 조합으로 시각화 구현
    - **예외 전파 설계**: list 파싱 에러 및 JSONDecodeError를 감지하여 조용히 묻히지 않도록 Streamlit 상위 수준에서 명시적 예외를 전파(raise)해 디버깅 생산성 증대

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- **학습 콘텐츠**:
    - [06-24.ipynb](06-24.ipynb): 토스증권 API 실습 노트북
    - [mini-project/](mini-project/): 반도체 IT 대표 종목 투자 전략 비교 분석 대시보드 패키지
        - [app.py](mini-project/app.py): 10개 IT 반도체 대표 종목 상호 배타적 선택, 탭 구조 및 Plotly 차트, AI 결과 HTML/CSS 대시보드
        - [agent.py](mini-project/agent.py): 시세 분석가 및 투자 수석 전략가 CrewAI 에이전트(Pydantic 구조화 출력 적용)
        - [toss_client.py](mini-project/toss_client.py): 토스증권 Open API 데이터 수집 및 캐싱 처리 SDK 클라이언트
        - [tests/test_toss_client.py](mini-project/tests/test_toss_client.py): requests mocking 단위 테스트 스크립트
    - [troubleshooting/](troubleshooting/): 실습 과정에서 발생하는 문제 상황 및 해결 가이드 기록 폴더
- **트러블슈팅 리포트**:
    - [troubleshooting/2026-06-23.md](troubleshooting/2026-06-23.md): Ollama 로컬 연동 및 Rich Logger 트러블슈팅 리포트
    - [troubleshooting/2026-06-24.md](troubleshooting/2026-06-24.md): Streamlit & CrewAI Pydantic 출력 JSON 파싱 예외 처리 트러블슈팅 리포트

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `crewai`, `streamlit`, `pandas`, `plotly`, `pydantic`, `requests`, `pytest`

---

## 📝 2026-06-23 실습 및 피드백 정리

### 1. CrewAI 내 로컬 Ollama 모델 연동을 위한 규격 설계
* **배움**:
  * CrewAI의 `LLM` 클래스는 내부적으로 LiteLLM을 프로바이더 인터페이스로 사용합니다. 따라서 로컬 Ollama 모델 호출 시 `'ollama/'` 접두사(Prefix)를 모델 이름에 필수로 할당해주어야 프로바이더를 정확하게 식별합니다.
  * 또한, 로컬 API 게이트웨이인 `base_url='http://localhost:11434'`를 추가 인자로 명시해야 합니다. WSL2 환경의 경우, 윈도우 호스트에 실행 중인 Ollama에 접근하기 위해서는 윈도우 가상 IP 게이트웨이(`http://<windows-host-ip>:11434`) 지정과 `OLLAMA_HOST=0.0.0.0` 환경 변수 설정을 통해 로컬 라우팅 바인딩을 완료해야 함을 실증했습니다.

### 2. CrewAI Rich Logging과 Verbose 모드의 메커니즘
* **배움**:
  * 크루 구동 시 터미널에 렌더링되는 화려한 박스는 CrewAI 내부에서 실행 시작, 에이전트의 Reasoning Loop, 도구 호출 상세 및 최종 응답을 `rich` 패키지로 그리는 시각화 패널입니다.
  * `verbose=True`(또는 1, 2)는 복잡한 멀티 에이전트 시스템 디버깅 시 사고 흐름 추적에 필수적이나, 단순 파이프라인 출력 제어나 성능 테스트 시에는 `verbose=False`(또는 0)로 오버헤드를 제어하여 터미널 출력을 깔끔하게 정돈할 수 있습니다.

---

## 📝 2026-06-24 실습 및 피드백 정리

### 1. 토스증권 API 기반의 모의 시뮬레이션 및 데이터 무결성 설계
* **배움**:
  * 금융 도메인 API 연동 시, API 인증 정보 누락이나 게이트웨이 지연 등으로 데이터 로드가 불가능할 때 애플리케이션 전체가 다운되는 것은 실무 관점에서 비효율적입니다.
  * 토스증권 SDK 내부에 정상 키가 부재할 경우 자동으로 작동하는 `is_mock` 플래그와 난수 엔진(시뮬레이션 모드)을 구축하여, 프론트엔드와 백엔드가 데이터 연결 장애 상황에서도 독립적으로 동작할 수 있도록 결합도를 낮추는 기법을 습득했습니다.

### 2. LLM 구조화 출력 설계 시 에러 전파(Exception Propagation)의 중요성
* **배움**:
  * CrewAI `output_pydantic` 파라미터를 사용하여 에이전트의 정성적 출력 데이터를 Pydantic 규격에 맞추더라도, 모델의 성능 제약이나 컨텍스트 윈도우 한계로 인해 JSON 문자열 대신 리스트(`list`)나 일반 텍스트가 리턴될 가능성이 항상 존재합니다.
  * 기존에는 이런 형식 에러가 발생 시 예외를 무조건 삼키거나 기본 객체를 반환하여 UI에 빈 화면이 렌더링되는 조용한 실패(Silent Failure) 현상이 있었습니다.
  * 파이썬의 `isinstance(data, dict)` 체크를 활용해 잘못된 스키마가 들어올 때 명확하게 상위 스택으로 예외(`TypeError`, `ValueError`)를 던져줌으로써 디버깅 생산성과 전체 시스템의 데이터 신뢰도를 높여야 함을 확인했습니다.
