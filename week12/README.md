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

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- **학습 콘텐츠**:
    - [06-23.ipynb](06-23.ipynb): 로컬 LLM 연동 및 CrewAI 기본 실습 노트북
    - [troubleshooting/](troubleshooting/): 실습 과정에서 발생하는 문제 상황 및 해결 가이드 기록 폴더
- **트러블슈팅 리포트**:
    - [troubleshooting/2026-06-23.md](troubleshooting/2026-06-23.md): 오늘의 트러블슈팅 리포트 (필요 시 작성)

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `crewai`, `crewai-tools`, `litellm`, `rich`

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
