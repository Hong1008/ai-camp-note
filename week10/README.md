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

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [06-08.ipynb](06-08.ipynb): 10주차 추천시스템 핵심 알고리즘 및 평가 지표 실습 통합 노트북 (진행 중)
- [06-09.ipynb](06-09.ipynb): google-genai SDK 활용 실습 노트북
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

