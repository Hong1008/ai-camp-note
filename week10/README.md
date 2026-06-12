# Week 10: Recommendation Systems (추천시스템)

10주차 추천시스템 실습을 시작하겠습니다. 이번 주차에는 개인화 추천의 기본 원리인 **콘텐츠 기반 필터링(Content-Based Filtering)**부터 **협업 필터링(Collaborative Filtering)**, **잠재 요인 협업 필터링(Matrix Factorization - SVD)** 및 추천 모델의 성능을 측정하기 위한 **정량 평가지표(Precision@K, Recall@K, NDCG)** 구현까지 추천시스템의 핵심 파이프라인을 깊이 있게 다룹니다.

---

## 🗓️ 학습 로드맵 및 수행 결과

### 🟡 Theme 34: 콘텐츠 기반 필터링 (Content-Based Filtering) (2026-06-08)
아이템 고유의 메타데이터(장르, 키워드, 설명 등)를 분석하여 사용자가 과거에 선호했던 아이템과 유사한 아이템을 추천하는 파이프라인을 구축합니다.
- **핵심 키워드**: Content-Based, TF-IDF, Cosine Similarity, Item Profile, Metadata Extraction
- **주요 실습**:
    - **TMDB 5000 영화 추천**: 줄거리(`overview`), 장르(`genres`), 키워드(`keywords`)를 결합하여 TF-IDF 벡터로 변환하고 코사인 유사도를 활용하여 유사 영화 추천 엔진 구현

### 🟡 Theme 35: 협업 필터링 (Collaborative Filtering) (2026-06-08)
사용자-아이템 평점 행렬을 기반으로 유사한 성향을 가진 사용자(User-Based) 혹은 유사하게 평가받은 아이템(Item-Based)을 탐색하여 추천을 수행합니다.
- **핵심 키워드**: Collaborative Filtering, User-Based CF, Item-Based CF, Rating Matrix, Cosine Similarity
- **주요 실습**:
    - **가중 평점 기반 아이템 기반 협업 필터링**: 결측치가 포함된 평점 행렬에 대해 코사인 유사도를 적용하고, 평점 가중치를 반영한 예측 평점 산출 로직 구현

### 🟡 Theme 36: 잠재 요인 협업 필터링 (Matrix Factorization) (2026-06-08)
고차원의 사용자-아이템 평점 행렬을 저차원의 잠재 요인(Latent Factor) 공간으로 분해하여 데이터의 희소성(Sparsity) 문제를 극복하고 예측 성능을 극대화합니다.
- **핵심 키워드**: Matrix Factorization, Singular Value Decomposition (SVD), Latent Factor, Dimension Reduction
- **주요 실습**:
    - **SciPy/SVD 기반 평점 복원 실습**: 평점 행렬에 SVD(특이값 분해)를 적용하여 저차원 공간으로 사영하고, 복원된 행렬을 바탕으로 사용자가 평가하지 않은 영화에 대한 예측 평점 산출 및 Top-N 추천 수행

### 🟡 Theme 37: 추천 성능 평가 지표 (Recommendation Evaluation Metrics) (2026-06-08)
추천시스템의 품질을 정량적으로 평가하기 위해 정보 검색 및 추천 분야에서 널리 쓰이는 주요 순위 기반 평가지표를 직접 구현하고 분석합니다.
- **핵심 키워드**: Evaluation Metrics, Precision@K, Recall@K, NDCG@K, Mean Average Precision (MAP)
- **주요 실습**:
    - **K개 추천 리스트 평가**: 실제 선호 아이템과 추천된 Top-K 아이템 리스트 간의 Precision@K, Recall@K, NDCG@K 지표를 수학적 수식에 맞추어 직접 Python으로 구현하고 결과 비교

### 🟡 Theme 38: Google GenAI SDK 활용 및 구조화 출력 실습 (2026-06-09)
Google GenAI SDK의 stateless `models` 및 stateful `chats` 인터페이스의 차이를 이해하고, Pydantic을 활용한 구조화된 출력(Structured Output)과 응답 속도 최적화(스트리밍, 비동기, 캐싱)를 실습합니다.
- **핵심 키워드**: Google GenAI, client.models, client.chats, Structured Output, Pydantic, Context Caching, Async
- **주요 실습**:
    - **Pydantic 구조화 응답 매핑**: LLM의 응답 스키마를 Pydantic 객체로 정의하여 구조화된 JSON 데이터로 안전하게 획득

### 🟡 Theme 39: LangChain 기초 및 LCEL 체인 구축 실습 (2026-06-10)
특정 LLM 공급자 종속성을 배제하고 일관된 인터페이스를 제공하는 LangChain 프레임워크를 도입하여, ChatPromptTemplate과 StrOutputParser를 파이프라인(`|`)으로 연결한 LCEL 스트리밍 체인을 구축합니다.
- **핵심 키워드**: LangChain, init_chat_model, ChatPromptTemplate, StrOutputParser, LCEL, Streaming
- **주요 실습**:
    - **LCEL 스트리밍 체인**: 템플릿-모델-파서를 LCEL로 구성하여 실시간 토큰 스트리밍 출력을 지원하는 대화형 체인 구현

### 🟢 Theme 40: LangChain 심화 및 실습 (2026-06-11)
Pydantic을 활용한 구조화된 출력(Structured Output)과 LCEL의 병렬/커스텀 함수 결합을 설계하고 실무 아키텍처(싱글톤/모듈화)를 다룹니다.
- **핵심 키워드**: Structured Output, with_structured_output, RunnableParallel, RunnableLambda, Singleton
- **주요 실습**:
    - **LangChain 심화 실습**: 06-11 노트북을 활용하여 게임 캐릭터 카드 구조화 생성 및 병렬 처리 체인 구축 완수

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [06-08.ipynb](06-08.ipynb): 10주차 추천시스템 핵심 알고리즘 및 평가 지표 실습 통합 노트북
- [06-09.ipynb](06-09.ipynb): google-genai SDK 활용 실습 노트북
- [06-10.ipynb](06-10.ipynb): LangChain 기초 개념 학습 및 LCEL 체인 구축 실습 노트북
- [06-11.ipynb](06-11.ipynb): LangChain 심화 및 응용 실습 노트북
- **트러블슈팅 리포트**:
    - [troubleshooting/](./troubleshooting/): 10주차 실습 과정에서 발생하는 문제 상황 및 해결 가이드 기록 폴더

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `pandas`, `numpy`, `scikit-learn` (`TfidfVectorizer`, `cosine_similarity`), `scipy` (`scipy.sparse.linalg.svds`), `transformers`, `langchain-huggingface`, `google-genai`, `pydantic`
- **Dataset**: `content/tmdb_5000_movies.csv` (TMDB 5000 Movies Dataset)

---

## 📝 2026-06-08 실습 및 피드백 정리 (추천 및 LLM 추가 실습)

### 1. 추천시스템 평가 지표 검증 결과
* **현상**: 임의 작성한 테스트 셋(선호 4개, 추천 5개 중 2개 매칭)에서 Precision@5: 0.4000, Recall@5: 0.5000, NDCG@5: 0.4415 기록.
* **배움**:
  * **Precision & Recall**: 추천 목록 크기와 실제 선호 아이템 개수 간의 비율 연산을 정량적으로 이해함.
  * **NDCG**: 가장 중요한 1순위(1st Rank) 추천 자리에 비선호 제품이 올 경우, 비록 하위 순위에서 적중하더라도 할인가(Discount)가 크게 작용하여 점수가 대폭 깎인다는 지표 고유의 특성을 수학적으로 검증함.

### 2. Zero-shot Text Classification (BART-Large-MNLI)
* **실습**: Michael Jackson의 "Billie Jean" 가사를 분류하는 실습 진행.
* **교훈**:
  * NLI(Natural Language Inference) 기반의 제로샷 모델은 엔시클로피디아성 상식(World Knowledge)을 갖추지 못했기 때문에 가사에 이름이 명시되지 않으면 'Michael Jackson'이라는 가수를 직접 연결하지 못함을 이해함.
  * 텍스트에 부정 표현(`not my lover`)이 존재해도, 단어 임베딩의 유사성(`'lover'` $\rightarrow$ `'love'`)에 쏠리는 어휘 바이어스(Lexical Bias)의 실무적 영향을 확인하고 라벨(Candidate Labels) 재설계의 중요성을 깨달음.

### 3. Local LLM vs Cloud Inference API
* **Local LLM (`pipeline`, `AutoModel`)**: 모델 가중치를 로컬 메모리(VRAM)에 직접 로드하므로 데이터 보안에 우수하며 완벽한 오프라인 작동을 지원함.
  * **초경량 모델 (Qwen3-0.6B)**: 약 1.2GB 크기로 일반 CPU 및 오피스용 노트북 환경에서도 빠른 속도로 문장을 생성함을 테스트함.
  * **양자화 (Quantization)**: 12B 파라미터 수준의 MoE 모델(예: Mellum2)을 개인 GPU에서 돌리기 위해선 `bitsandbytes` 등을 활용한 4-bit 양자화 기법이 필수적임을 이해함.
* **Cloud API (`HuggingFaceEndpoint`)**: Hugging Face 서버가 연산을 처리하므로 로컬 자원 소모가 전혀 없으나, 클라우드 호스팅 여부 및 네트워크 가용성이 필요함.

### 4. Chat Prompt 구조와 소형 모델의 한계
* **지침**: 대화형 프롬프트 구성 시 `system` 역할(페르소나 지정)은 항상 대화의 최상단(Index 0)에 와야 함.
* **분석**: 순서가 `[User] -> [System]` 형태로 꼬였을 때, 0.6B 크기의 극소형 모델은 지시 사항의 선후 흐름을 놓치고 마지막 메시지를 그대로 복사(Echoing)하는 오작동 패턴을 분석 및 입증함.


---

## 📝 2026-06-09 실습 및 피드백 정리 (Google GenAI SDK 실습)

### 1. `client.models`와 `client.chats` 인터페이스 차이
* **models (Stateless)**: 이전 대화 상태를 누적하지 않고 단발성 요청(요약, 분류, 정보 추출)을 처리하여 토큰 낭비와 응답 지연을 방지함.
* **chats (Stateful)**: 내부적으로 대화 히스토리를 유지하며 관리하여 멀티턴 대화형 UX를 구현하기에 유용함.

### 2. 구조화된 출력 (Structured Output) 및 Pydantic 매핑
* **실습**: `types.GenerateContentConfig`의 `response_mime_type="application/json"`과 `response_schema`에 Pydantic 클래스를 등록하여, LLM 응답을 바로 검증된 Python 객체(`response.parsed`)로 얻는 방법을 구현함.

### 3. API 응답 속도 최적화 전략
* **스트리밍**: `generate_content_stream` 및 `send_message_stream`을 사용하여 첫 번째 토큰 속도(TTFT)를 줄임.
* **토큰 한도와 우회**: 한국어 토큰 특성으로 인해 `max_output_tokens`를 낮게 설정하면 답변이 중간에 잘려 `response.text`가 `None`으로 변환될 수 있으며, 이때 `response.candidates[0].content.parts[0].text`로 원본 잘린 텍스트에 직접 접근하여 안전하게 회수하는 기법을 이해함.
* **비동기 처리 & 캐싱**: `client.aio` 비동기 요청을 병렬화하여 처리 성능을 올리고, 32k 토큰 이상의 대형 참고자료에는 컨텍스트 캐싱(Context Caching)을 적용해 연산 오버헤드와 비용을 줄임.

### 4. 모델 라벨별 특성 및 인프라 제약 조건
* **gemma-4-26b-a4b-it**: MoE(Mixture of Experts) 기반 모델로, 로컬에서 구동할 때 활성화되는 파라미터는 4B급 수준으로 줄여 VRAM을 극도로 아끼며 뛰어난 성능을 보임.
* **gemma-4-31b-it**: 31B 단일 Dense 모델로, 추론 시 VRAM 소모가 크나 더욱 정교하고 안정적인 추론이 가능함.
* **gemini-3.1-flash-lite**: 상용 API 모델로서 극단적인 속도와 경제성을 확보한 경량화 모델로 로컬 GPU 하드웨어에 구속받지 않는 챗봇 배포에 최적화됨.

---

## 📝 2026-06-10 실습 및 피드백 정리 (LangChain 기초 및 체인 구축 실습)

### 1. LangChain 도입 목적과 추상화
* **개념**: 특정 LLM 공급자(Gemini, OpenAI 등) API 종속성을 배제하고 통일된 인터페이스(`invoke`, `stream`)를 보장하기 위해 LangChain 도입.
* **배움**: `init_chat_model`을 활용하여 `'google_genai:gemma-4-31b-it'` 등의 다양한 백엔드 모델을 표준 객체로 즉시 전환 및 생성하는 방법을 실습함.

### 2. PromptTemplate vs ChatPromptTemplate
* **PromptTemplate**: 단일 텍스트(String)를 입력값으로 채우는 템플릿으로 주로 텍스트 완성형 및 RAG 텍스트 결합에 사용.
* **ChatPromptTemplate**: `System`, `Human`, `AI` 등의 대화 역할이 바인딩된 메시지 리스트를 생성. 역할 인지가 중요한 현대 Chat API(Gemini 등) 모델 구동에 적합.

### 3. StrOutputParser 및 LCEL 스트리밍 체인
* **StrOutputParser**: LLM 반환 복잡한 `AIMessage` 객체로부터 순수 텍스트 내용만 추출.
* **LCEL**: 프롬프트, 모델, 파서를 파이프(`|`) 연산자로 선언적으로 엮는 기법.
* **실습**: `chat_prompt | model | StrOutputParser()` 형태의 체인을 설계하여 스트리밍(`stream()`) 방식으로 텍스트를 실시간 터미널에 흘려보내는(flush) 로직을 완수함.

---

## 📝 2026-06-11 실습 및 피드백 정리 (LangChain 심화 및 실무 아키텍처 실습)

### 1. `with_structured_output`을 이용한 구조화된 출력
* **원리**: Pydantic `BaseModel`로 출력 데이터 스키마를 정의하고, `model.with_structured_output`에 전달하면 LLM 응답을 파라미터가 검증된 파이썬 객체로 즉시 획득할 수 있습니다. 
* **효과**: 개발 시 별도의 파싱 로직(`json.loads` 등) 없이 안정적으로 키값과 타입이 보장된 데이터를 다룰 수 있어 타입 안정성이 크게 상승합니다.

### 2. LCEL의 파이프라인 연산자(`|`)의 작동 원리
* **이유**: LangChain 구성 요소가 상속받는 `Runnable` 추상 클래스가 파이썬 매직 메서드인 `__or__`와 `__ror__`를 오버로딩하여 구현했기 때문입니다.
* **결과**: `concept_prompt | model | parser`를 실행하면 각 단계의 출력이 다음 단계의 입력으로 순차 전송되는 `RunnableSequence` 객체를 형성하게 됩니다.

### 3. 일반 함수의 체인 결합 (`RunnableLambda`)
* **원리**: `Runnable` 인터페이스를 상속하지 않는 일반 파이썬 함수도 `RunnableLambda(func)`로 래핑하거나 파이프 기호 우측에 직접 연결(Type Coercion)하여 체인 내에서 입출력을 가공할 수 있습니다.

### 4. `RunnableParallel`을 활용한 동시성 제어
* **효과**: 하나의 입력값을 받아 여러 체인을 병렬로 동시 수행하고, 결과들을 하나의 딕셔너리로 결합해 줍니다. 병렬 API 호출을 통해 실행 시간을 획기적으로 낮출 수 있습니다.

### 5. 실무용 싱글톤(Singleton) 아키텍처 설계
* **모듈 기반 싱글톤**: 파이썬은 임포트된 모듈이 최초 한 번만 메모리에 올라가는 특성을 이용하여 `chains.py`에 체인을 미리 빌드해 두고 필요한 모듈에서 호출하는 방식을 권장합니다.
* **클래스 기반 싱글톤**: 웹 API 서버(FastAPI 등)에서는 LLMChainManager와 같은 인스턴스 싱글톤을 구축하거나 DI 컨테이너를 활용하여 자원을 중앙 집약적으로 통제합니다.
