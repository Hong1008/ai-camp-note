# Week 13: 파인튜닝 실습 (13주차)

13주차 파인튜닝 실습을 위한 학습 저장소입니다. 이번 주차의 학습 내용과 실습 코드를 기록합니다.

---

## 🗓️ 학습 로드맵 및 수행 결과

### 🟡 Theme 51: LM Studio API 스트리밍 제어, LangChain 연동 및 파인튜닝 생태계 이해 (2026-06-29)
- **핵심 키워드**: LM Studio, SSE Streaming, Reasoning Model, LangChain Integration, Fine-Tuning Libraries (unsloth, trl, etc.), RunPod Deployment
- **주요 실습**:
    - **LM Studio API 스트리밍 파싱 및 토큰 끊김 문제 해결**: `max_output_tokens` 한계로 인해 생각 과정(Reasoning) 출력 이후 최종 답변 출력이 잘리는 원인을 규명하고, SSE(Server-Sent Events) 규격에 맞춘 `reasoning.delta` / `message.delta` 실시간 분기 처리 파이썬 코드 구현
    - **LangChain 연동 및 생각과정 추출**: `langchain-openai`의 `ChatOpenAI`를 통해 LM Studio를 연동하고 `additional_kwargs.get("reasoning_content")`를 통해 모델의 생각 프로세스를 추출하는 기법 학습
    - **파인튜닝 핵심 6대 라이브러리 역할 매핑**: `datasets`, `transformers`, `bitsandbytes`, `accelerate`, `trl`, `unsloth` 각각의 기능 및 상호 유기적 연동 구조 분석
    - **RunPod 클라우드 환경 결과물 관리 이해**: SSH 연동 학습 시 데이터 유실 방지를 위한 `/workspace` 영구 볼륨의 중요성 및 Hugging Face Hub 업로드, SCP 다운로드 등 모델 외부 반출 방법 파악

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- **학습 콘텐츠**:
    - [content/](content/): 파인튜닝 실습 소스 코드 및 데이터셋 준비 폴더 (Jupyter Notebook 포함)
    - [troubleshooting/](troubleshooting/): 실습 과정에서 발생하는 문제 상황 및 해결 가이드 기록 폴더
- **트러블슈팅 리포트**:
    - [troubleshooting/2026-06-29.md](troubleshooting/2026-06-29.md): LM Studio API 연동 시 Reasoning 출력으로 인한 최종 답변 끊김 및 LangChain 동기 Hanging 트러블슈팅 리포트

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `langchain-openai`, `requests`, `transformers`, `peft`, `datasets`, `trl`, `accelerate`, `bitsandbytes`

---

## 📝 2026-06-29 실습 및 피드백 정리

### 1. LM Studio SSE API 스트리밍 및 Reasoning/Content 분리
* **배움**:
  * Gemma 4와 같은 추론형 모델을 로컬 API로 호출할 때, 모델의 생각 과정(Reasoning)과 최종 답변(Content)이 분리되어 응답 스키마로 들어오는 구조를 파악했습니다.
  * 특히 `max_output_tokens` 제한이 작을 때 생각 과정에서만 대부분의 토큰을 소모하여 최종 답변이 빈 문자열(`""`)로 반환되는 조기 중단(Truncation) 문제를 `stats` 분석을 통해 발견하고, 토큰 제한을 크게 늘리거나(1000 이상) 혹은 생각 과정을 비활성화하여 대처하는 현실적인 해결 방안을 학습했습니다.
  * Server-Sent Events(SSE) 파싱을 위해 `requests` 패키지에서 `stream=True` 옵션을 활용하여 `event: reasoning.delta`와 `event: message.delta`를 분류하여 실시간 스트리밍 터미널을 구현했습니다.

### 2. LangChain을 활용한 로컬 추론 모델 연동 및 `additional_kwargs` 활용
* **배움**:
  * LM Studio의 OpenAI 호환 규격을 사용하여 `ChatOpenAI` 클래스에 `base_url`과 더미 `api_key`를 넘김으로써 간단히 LangChain에 local LLM을 바인딩하는 구조를 완성했습니다.
  * 비표준인 생각 과정(`reasoning_content`)은 LangChain 내에서 `additional_kwargs` 속성에 딕셔너리로 저장된다는 점을 실증하여, 에이전트 개발 시 모델의 생각을 별도로 추출 및 렌더링하는 기법을 습득했습니다.

### 3. 파인튜닝 핵심 라이브러리 조합 및 클라우드(RunPod) 지속성 설계
* **배움**:
  * 대용량 데이터 로드(`datasets`), 오픈소스 LLM 뼈대(`transformers`), 4/8-bit 저정밀도 양자화(`bitsandbytes`), 멀티 GPU 분산 학습 가속(`accelerate`), 간결한 학습 API(`trl`), Triton 기반 커널 가속(`unsloth`) 등 6개 핵심 라이브러리의 유기적인 관계를 이해했습니다.
  * RunPod 등 클라우드 GPU 인프라에서 파인튜닝 시 컨테이너 재설정 시 모든 임시 폴더가 유실될 위험을 대비하여, 반드시 지속성 볼륨 경로인 `/workspace` 하위로 `output_dir`을 마운트하고 최종 가중치는 Hugging Face Hub에 `push_to_hub` 하거나 `scp`를 이용해 오프라인 백업을 구성해야 함을 확인했습니다.
