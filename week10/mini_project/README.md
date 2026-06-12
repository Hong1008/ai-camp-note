# AGENTS.md

AI 면접관(AI Interviewer) 프로젝트를 구현·수정하는 코딩 에이전트를 위한 안내 문서입니다.
작업 전에 이 문서를 끝까지 읽고, 특히 "핵심 원칙"과 "하지 말 것"을 위반하지 마세요.

---

## 1. 프로젝트 개요

로컬 sLLM(`gemma-4-31B-it`)을 사용해, 사용자가 지원 직무를 선택하면 AI가 면접관이 되어 질문하고
답변을 평가(점수 + 피드백 + 모범답안)하며, 이전 답변을 바탕으로 꼬리질문을 이어가는 Streamlit 앱입니다.

- 대상 지원자: **신입 (0~1년)**
- 지원 직무(선택): `ai_engineer`(AI 엔지니어), `python_backend`(Python 백엔드)
- 면접 유형: `technical`(기술 면접), `project`(프로젝트 경험 면접)
- 입력 방식: 텍스트 기반 구술 면접 (음성/코드 실행 없음)

## 2. 핵심 원칙 (위반 금지)

1. **UI와 로직을 분리한다.** `app.py`(Streamlit)는 렌더링과 상태머신 진행만 담당한다.
   모든 면접 로직은 `core/`에 두며, `core/`는 Streamlit에 의존하지 않고 단독으로 `pytest`로 검증 가능해야 한다.
2. **하나의 모델, 여러 역할.** 모델 인스턴스는 하나만 띄운다. 질문 생성·평가·꼬리질문·모범답안·리포트는
   서로 다른 system 프롬프트와 파라미터로 같은 모델을 호출한다.
3. **LLM 호출을 작게 쪼갠다.** 한 번의 호출에서 "평가 + 점수 + 피드백 + 모범답안 + 꼬리질문"을 모두 시키지 않는다.
   작은 로컬 모델은 거대 프롬프트에서 JSON이 깨지고 항목을 빠뜨린다. 단계별로 분리한다(섹션 5 참고).
4. **규칙으로 할 수 있는 일에 LLM을 쓰지 않는다.** 답변 길이 게이트, 점수 집계, 질문 추출은 코드로 처리한다.
5. **질문 은행을 grounding으로 쓴다.** 모델이 질문/평가기준을 창작하게 두지 말고, `data/question_bank.json`의
   `eval_points`·`follow_up_hints`·`model_answer_key`를 프롬프트에 주입한다. 이것이 품질 일관성의 핵심이다.

## 3. 기술 스택 & 제약

- **언어**: Python 3.13+
- **UI**: Streamlit
- **모델**: `google/gemma-4-31B-it` (31B Dense, 256K 컨텍스트, 네이티브 system role, thinking 모드 지원)
<!-- - **서빙(로컬)**: 기본은 **Ollama**(OpenAI 호환 `http://localhost:11434/v1`). 속도/동시성이 필요하면 **vLLM**(`http://localhost:8000/v1`)으로 교체. 둘 다 OpenAI 호환이라 클라이언트 코드는 동일하다. -->
- **서빙**: google-ai-api-key
- **LLM 클라이언트**: `openai` 파이썬 SDK (`base_url`만 로컬로 변경)
- **출력 검증**: `pydantic`
- **재시도**: `tenacity` (JSON 파싱 실패 시 repair 재시도)

### 모델 호출 기본값
- 권장 샘플링: `temperature=1.0`, `top_p=0.95`, `top_k=64` (Gemma 4 공식 권장값)
- **평가 호출은 thinking 모드를 켠다**(일관성↑). 낮은 temperature가 아니라 thinking이 일관성 레버다.
- **멀티턴 히스토리에 thinking 출력을 넣지 않는다.** 다음 턴 입력을 만들 때 thinking 블록은 제거한다(모델 카드 지침).
- 구조화 출력은 서버의 JSON 스키마/`format` 기능으로 강제한다. Ollama/vLLM 버전에 따라 thinking 플래그 노출 방식이 다를 수 있으니 실제 서버에서 한 번 확인하고 `core/llm_client.py`에 캡슐화한다.

## 4. 프로젝트 구조

```
ai-interviewer/
├── app.py                  # Streamlit 진입점: UI + 상태머신 진행만
├── config.py               # 모델명, 엔드포인트, 샘플링 파라미터, 상수
├── data/
│   ├── question_bank.json  # 질문 은행 (이미 작성됨, 섹션 6)
│   └── personas.json       # 면접관 성격 설정 (섹션 7)
├── core/                   # Streamlit 비의존 순수 로직
│   ├── llm_client.py       # LLM 호출 추상화 (generate, thinking, JSON 스키마, repair)
│   ├── prompts.py          # 프롬프트 템플릿 (평가·꼬리질문·모범답안·리포트)
│   ├── schemas.py          # Pydantic 모델 (평가 결과 등 구조화 출력)
│   ├── question_bank.py    # 질문 로드/필터/샘플링
│   ├── text_utils.py       # 입력 정규화, 길이 게이트, 토큰 추정
│   └── interview.py        # 면접 상태머신 + 턴 파이프라인 (오케스트레이션)
├── tests/
│   └── test_*.py           # core/ 단위 테스트
├── requirements.txt
└── README.md
```

## 5. 아키텍처: 한 턴(turn)의 처리 파이프라인

`core/interview.py`가 다음 순서로 답변 하나를 처리한다. 각 단계의 책임을 지켜라.

1. **입력 정규화** (`text_utils.normalize`) — 공백 정리.
2. **길이 게이트** (`text_utils`, 규칙 기반, LLM 미호출) — 답변 토큰/글자 수가 해당 질문의
   `min_answer_tokens` 미만이면 즉시 "조금 더 구체적으로" 재질문을 반환하고 종료(LLM 호출 안 함).
3. **평가** (LLM 호출, thinking ON, JSON 스키마) — `질문 + eval_points + 루브릭 + 답변`을 주고
   논리성/구체성/전달력 점수(1~5, 앵커 기준)와 각 `eval_point` 충족 여부를 JSON으로 받는다.
   결과는 `schemas.EvaluationResult`로 검증한다.
4. **꼬리질문 판단** (규칙 기반) — 충족되지 않은 핵심 `eval_point`가 있고
   `followup_count < MAX_FOLLOWUP`(기본 1~2)이면 꼬리질문으로 분기.
   - 분기 시: **꼬리질문 생성**(LLM) — 미충족 포인트에 매핑된 `follow_up_hints` 중 하나로 1개만 생성.
     `followup_count += 1` 후, 지원자 답변을 다시 받으면 1번(게이트)부터 반복.
   - 아니면: **모범답안 + 피드백 생성**(LLM) — `model_answer_key`를 신입 눈높이로 확장하고,
     지원자 답변과의 차이를 짚는다. 그 후 다음 질문으로 이동(`followup_count = 0`).
5. **transcript 누적** — `(질문, 답변, 평가결과 JSON)`을 `session_state`에 쌓는다(thinking 제거 상태로).
6. **면접 종료 시 리포트** — 누적 평가 JSON으로 점수 집계는 **코드로** 계산하고, LLM은 서술 요약에만 쓴다.

## 6. 데이터: 질문 은행 (`data/question_bank.json`)

이미 작성되어 있다. 구조는 `_meta.schema`에 정의돼 있으며, 각 질문 항목의 핵심 필드:

- `role`: `ai_engineer | python_backend | both`
- `type`: `technical | project`
- `topic`, `difficulty`
- `question`: 출제 텍스트 (모델에게 창작이 아니라 "자연스럽게 다듬어 출제"만 시킬 것)
- `eval_points`: 채점 포인트 배열 → **평가 프롬프트에 그대로 주입** (점수 일관성의 핵심)
- `follow_up_hints`: 꼬리질문 방향 → 미충족 `eval_point`에 매핑해 꼬리질문 생성에 사용
- `model_answer_key`: 모범답안 생성용 골자
- `min_answer_tokens`: 이 값 미만이면 길이 게이트에서 재질문 트리거

`core/question_bank.py`는 JSON을 메모리에 로드해 `role`/`type`/`topic`으로 필터·랜덤 추출하고,
`asked_ids`로 중복 출제를 막는다.

## 7. 데이터: 면접관 페르소나 (`data/personas.json`)

페르소나는 **톤과 꼬리질문 공격성에만** 영향을 준다. **채점 루브릭은 페르소나와 무관하게 고정**한다(공정성·안정성).
페르소나를 자유 서술이 아니라 구조화된 설정으로 둔다. 예:

```json
{
  "pressure":  { "label": "압박형",  "tone": "...", "followup_threshold": "low",  "encouragement": "low" },
  "friendly":  { "label": "친근형",  "tone": "...", "followup_threshold": "high", "encouragement": "high" },
  "neutral":   { "label": "중립형",  "tone": "...", "followup_threshold": "mid",  "encouragement": "mid" }
}
```

`tone`/`encouragement`는 질문·피드백 프롬프트의 system 메시지에만 반영하고, 평가 점수 산출에는 절대 반영하지 않는다.

## 8. 상태 관리 (Streamlit)

Streamlit은 매 상호작용마다 스크립트를 처음부터 재실행한다. 면접 진행 상태는 전부 `st.session_state`에 명시적으로 보관한다.

```python
st.session_state.interview = {
    "phase": "asking",            # setup | asking | evaluating | report
    "role": "ai_engineer",
    "persona": "pressure",
    "current_question": {...},     # 질문 은행 항목
    "followup_count": 0,           # 현재 질문의 꼬리질문 횟수 (MAX_FOLLOWUP 이하)
    "asked_ids": [],               # 중복 출제 방지
    "transcript": [                # 리포트 재료
        {"q": "...", "a": "...", "eval": {...}}
    ],
}
```

`transcript`에 각 턴의 평가 JSON을 처음부터 구조화해 쌓아두면 리포트는 집계만으로 거의 완성된다.

## 9. 코드 컨벤션

- `core/`는 Streamlit/`st` 임포트 금지. UI 상태는 인자로 주고받는다.
- LLM 호출은 반드시 `core/llm_client.py`를 통해서만 한다. `app.py`나 다른 모듈에서 직접 `openai`를 호출하지 않는다.
- 프롬프트 문자열은 `core/prompts.py`에 모은다. 코드 곳곳에 인라인 프롬프트를 흩뿌리지 않는다.
- LLM이 반환하는 JSON은 항상 `pydantic` 모델로 검증한다. 검증 실패 시 `tenacity`로 1회 repair 재시도("JSON만 다시 출력") 후, 그래도 실패하면 안전한 기본값으로 폴백한다.
- 타입 힌트를 사용한다. 함수는 작고 한 가지 일만 한다.
- 한국어 사용자 대상이므로 사용자에게 보이는 모든 텍스트(질문·피드백·리포트)는 한국어로 생성한다.

## 10. 하지 말 것 (안티패턴)

- ❌ **벡터DB / RAG 도입 금지.** 질문이 33개뿐이다. JSON을 메모리에 올려 필터·랜덤 추출하면 충분하다.
- ❌ **LangChain 등 무거운 오케스트레이션 프레임워크 금지.** `openai` SDK 직접 호출이 디버깅하기 훨씬 쉽다.
- ❌ **거대 단일 프롬프트 금지.** 평가/꼬리질문/모범답안을 한 호출에 몰아넣지 않는다.
- ❌ **길이 게이트·점수 집계를 LLM에 맡기지 말 것.** 규칙/코드로 처리한다.
- ❌ **페르소나가 채점 점수에 영향을 주게 하지 말 것.** 루브릭은 고정이다.
- ❌ **멀티턴 히스토리에 thinking 블록을 남기지 말 것.**
- ❌ **`transformers`를 토큰 카운팅 용도로 무겁게 로드하지 말 것.** 게이트는 글자/단어 휴리스틱이면 충분하다.
- ❌ **`core/`에서 Streamlit을 임포트하지 말 것.**
- ❌ **모델 인스턴스를 역할별로 여러 개 띄우지 말 것.**

## 11. 명령어

```bash
# 의존성 설치
pip install -r requirements.txt

# 모델 서빙 (Ollama 예시 — 정확한 태그/GGUF는 Ollama 라이브러리에서 확인)
ollama serve
ollama run hf.co/google/gemma-4-31B-it   # 양자화 GGUF 권장 (Q4 기준 약 18~20GB VRAM)

# (대안) vLLM 서빙
# vllm serve "google/gemma-4-31B-it"

# 앱 실행
streamlit run app.py

# 테스트 (core/ 로직)
pytest tests/
```

## 12. 권장 구현 순서 (마일스톤)

1. **M1 — 스캐폴딩 & 모델 연결**: `config.py`, `core/llm_client.py`(generate + thinking + JSON 스키마 + repair),
   로컬 모델에 "ping" 호출 성공시키기. `core/`만 `pytest`로 검증 가능하게.
2. **M2 — 질문 은행 & 단일 질문 흐름**: `question_bank.py`(로드/필터/추출), `app.py`에서 직무·페르소나 선택 →
   첫 질문 출제 → 답변 입력까지. 아직 평가 없음.
3. **M3 — 평가 파이프라인**: `schemas.py`, `prompts.py`(평가), `text_utils.py`(정규화·길이 게이트),
   `interview.py`의 1~3단계. 점수(논리성/구체성/전달력) + 피드백 + 모범답안 표시.
4. **M4 — 꼬리질문**: 4단계 분기 로직 + 꼬리질문 생성 프롬프트. `followup_count` 관리.
5. **M5 — 리포트**: 면접 종료 → `transcript` 집계(코드) + 서술 요약(LLM) → 전체 평가 리포트.
6. **M6 — 페르소나 차별화 강화**: `personas.json` 반영을 톤/꼬리질문 공격성에 한정해 적용.

각 마일스톤마다 `core/` 단위 테스트를 먼저 통과시키고 UI를 붙인다.