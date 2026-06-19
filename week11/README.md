# Week 11: Advanced LLM Applications & Agents (11주차: 고급 LLM 응용 및 에이전트)

11주차 실습을 위한 학습 저장소입니다. 이번 주차에는 LangChain의 심화 활용, Tool Calling 기반의 대화형 에이전트 설계, 그리고 흐름 제어 프레임워크(예: LangGraph) 등을 다루며 단순 질의응답을 넘어 스스로 문제를 해결하는 실무 중심의 AI 시스템 아키텍처를 학습하고 구현합니다.

---

## 🗓️ 학습 로드맵 및 수행 결과

### 🟡 Theme 42: 가변 차원(Matryoshka) 임베딩 실습 및 검증 (2026-06-15)
- **핵심 키워드**: GoogleGenerativeAIEmbeddings, gemini-embedding-2, output_dimensionality, Matryoshka Representation Learning, RapidOCR, Vector Metrics, Text Chunking
- **주요 실습**:
    - **차원 압축에 따른 유사도 판별력 비교**: `gemini-embedding-2` 모델의 기본 3072차원과 축소된 256차원의 임베딩 벡터 생성 및 코사인 유사도 판별 격차 비교 테스트
    - **PDF 내 이미지 OCR 기반 텍스트 로드**: `PyPDFLoader`와 `RapidOCRBlobParser`를 결합하여 PDF 내부 이미지의 글자를 텍스트로 자동 파싱하는 실습
    - **수학적 유사도 지표 및 청커 메커니즘 학습**: 코사인 유사도, 내적, L2 거리의 상관관계와 `RecursiveCharacterTextSplitter`의 작동 과정 분석

### 🟡 Theme 43: Vector Store 구축 및 유사도 검색 실습 (2026-06-16)
- **핵심 키워드**: VectorStore, Chroma, Document & Metadatas, Similarity Search, Metadata Filtering, Upsert, RDB vs Vector DB, Hybrid Search
- **주요 실습**:
    - **행렬 연산 기반의 수동 벡터 검색 구현**: L2 정규화 후 내적이 곧 코사인 유사도가 됨을 이해하고 NumPy `@` 연산으로 고속 벡터 검색 함수(`search`) 구현
    - **Vector Store (Chroma) 연동 및 metadata filter 실습**: 문서와 메타데이터를 저장 및 인덱싱하고, 복수의 조건을 통한 하이브리드 필터링 쿼리 적용
    - **중복 ID 적재 정책 검증**: 동일한 `ids`를 갖는 문서를 다시 `add_documents` 할 시, 에러가 아닌 기존 데이터를 덮어쓰는 `Upsert` 동작 메커니즘 실증

### 🟡 Theme 44: Ensemble Retriever 및 하이브리드 검색(Hybrid Search) 실습 (2026-06-17)
- **핵심 키워드**: Hybrid Search, EnsembleRetriever, BM25Retriever, Reciprocal Rank Fusion(RRF), Keyword Matching, Semantic Search
- **주요 실습**:
    - **이종 Retriever 구축 및 결합**: 키워드 매칭(BM25)과 밀집 벡터 검색(Chroma)의 상반된 장단점을 분석하고 두 시스템을 결합
    - **RRF 알고리즘 기반 순위 융합**: 가중치를 적용한 EnsembleRetriever의 동작을 파악하고 최적의 가중치 Trade-off 탐색
    - **하이브리드 RAG 파이프라인 검증**: 고유명사 품번 매칭과 문맥 이해를 모두 만족시키는 복합 질의를 통한 RAG 품질 실증

### 🟡 Theme 45: Tool Calling 기반 ReAct 에이전트 및 STT 연동 실습 (2026-06-18)
- **핵심 키워드**: Tool Calling, @tool, bind_tools, ReAct Agent, AgentExecutor, SpeechRecognition, PyDub, Voice Agent
- **주요 실습**:
    - **LangChain Tool 정의 및 모델 바인딩**: `@tool` 데코레이터를 이용한 커스텀 도구 정의 및 `bind_tools()`를 통한 모델 연동
    - **ReAct 에이전트 흐름 구축**: `create_react_agent`와 `AgentExecutor`를 활용하여 사내 규정 RAG 및 계산기 도구를 유기적으로 선택하고 실행하는 ReAct 아키텍처 설계
    - **STT 음성 비서 프로토타입 구현**: 음성 파일(`stt_test.wav`)을 로드하여 텍스트로 변환(STT)하고, 이를 에이전트의 입력값으로 전달하여 도구를 활용해 응답을 도출하는 전체 파이프라인 실증

### 🟢 Theme 46: LangGraph 기반 StateGraph 에이전트 설계 및 제어 실습 (2026-06-19)
- **핵심 키워드**: LangGraph, StateGraph, TypedDict State, Nodes & Edges, Conditional Edge, Router, Recursion Limit
- **주요 실습**:
    - **기본 StateGraph 흐름 구축**: 전역 상태(SimpleState)를 정의하고 각 노드와 엣지를 등록하여 비순환 에이전트 그래프 작동 원리 실증
    - **Conditional Edge 기반 스마트 라우팅**: LLM 구조화 출력을 사용하여 DB 검색 필요성을 판단하고 조건부 엣지를 통해 검색/답변 노드로 동적 분기하는 에이전트 아키텍처 설계
    - **Recursion Limit을 통한 폭주 방어**: 에이전트의 무한 루프 상황을 시뮬레이션하고 `recursion_limit` 설정을 통해 가드가 정상 작동함을 입증

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- **학습 콘텐츠**:
    - [content/](content/): 일자별 실습 코드 및 분석 자료 저장 폴더
    - [06-15.ipynb](06-15.ipynb): 가변 차원 임베딩 성능 비교 및 문서 로딩/청킹 실습 노트북
    - [06-16.ipynb](06-16.ipynb): Vector Store 구축 및 유사도 검색 실습 노트북
    - [06-17.ipynb](06-17.ipynb): Ensemble Retriever 및 하이브리드 검색 실습 노트북
    - [06-18.ipynb](06-18.ipynb): Tool Calling 기반 ReAct 에이전트 및 STT 연동 실습 노트북
    - [06-19.ipynb](06-19.ipynb): LangGraph 기반 StateGraph 에이전트 설계 및 제어 실습 노트북
- **트러블슈팅 리포트**:
    - [troubleshooting/](troubleshooting/): 실습 과정에서 발생하는 문제 상황 및 해결 가이드 기록 폴더
    - [2026-06-17.md](troubleshooting/2026-06-17.md): Chroma 중복 적재 및 ParentDocumentRetriever 타입 검증 에러 해결 리포트
    - [2026-06-18.md](troubleshooting/2026-06-18.md): Tool Calling 에이전트 에러 핸들링 및 STT 연동 트러블슈팅 리포트
    - [2026-06-19.md](troubleshooting/2026-06-19.md): LangGraph 상태 불일치, Reducer 충돌 및 Recursion Limit 초과 해결 리포트

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `langchain`, `langchain-google-genai`, `langgraph`, `scikit-learn`, `numpy`, `rapidocr`, `onnxruntime`, `speechrecognition`, `pydub`

---

## 📝 2026-06-15 실습 및 피드백 정리

### 1. 가변 차원(Matryoshka) 임베딩 차원 축소 성능 실증
* **현상**: `gemini-embedding-2` 모델을 사용하여 기본 3072차원에서 256차원으로 축소(약 1/12 용량)하여 코사인 유사도를 평가한 결과:
  * **3072차원**: 유사 문장(`0.7442`) vs 무관 문장(`0.4361`) $\rightarrow$ 판별 격차 **`0.3082`**
  * **256차원**: 유사 문장(`0.7708`) vs 무관 문장(`0.4847`) $\rightarrow$ 판별 격차 **`0.2860`**
* **배움**:
  * 차원을 대폭 축소하더라도 문장의 의미론적 구별 능력을 보여주는 판별 격차는 약 7.2%(`0.0222`) 정도만 감소하는 것을 확인하였습니다.
  * 이는 저장 공간 및 유사도 연산 속도에서 12배에 달하는 리소스 이득을 취하면서도 검색 모델의 정밀함(RAG retrieval 성능 등)은 상당 부분 그대로 보존할 수 있음을 나타내며, 실무 아키텍처 설계 시 비용 대비 성능을 최적화(Trade-off)하는 강력한 설계 옵션이 될 수 있음을 학습했습니다.

### 2. PDF 내 이미지 OCR 텍스트 추출 방식과 실무적 한계
* **현상**: `PyPDFLoader`에 `RapidOCRBlobParser`를 연결하여 구동한 결과, 이미지 내의 텍스트가 마크다운 이미지 링크 형식(`![인식된 글자들](#)`)으로 본문에 삽입되어 파싱됨을 확인했습니다.
* **배움**:
  * 단순 OCR 기법은 복잡한 그래프의 축 이름, 연도, 수치를 파편화된 줄바꿈 문자로 변환하므로 데이터 간 관계 구조(예: 트렌드)를 전혀 이해하지 못하며, 이로 인해 RAG 시스템에 투입 시 심각한 정보 왜곡 및 LLM 할루시네이션을 유발할 수 있음을 관찰했습니다.
  * 실무 프로덕션 환경에서는 이를 극복하기 위해 멀티모달 비전 모델(Gemini, GPT-4o 등) 기반의 이미지 캡셔닝 또는 전문 클라우드 파서(LlamaParse) 등을 적용하여 전처리하는 아키텍처의 필요성을 체감했습니다.

### 3. 벡터 유사도/거리 측정 지표의 기하학적 비교
* **배움**:
  * **내적(Dot Product)**: 방향성과 스케일(벡터의 크기)을 모두 반영하므로 단어 수나 문서 길이에 크게 영향을 받습니다.
  * **코사인 유사도(Cosine Similarity)**: 벡터의 크기를 1로 강제 정규화한 뒤 사잇각만 측정하므로, 문서 길이에 무관하게 순수 주제(의미)만 비교하는 장점이 있습니다.
  * **L2 거리(Euclidean Distance)**: 두 점 사이의 최단 직선 거리를 나타냅니다.
  * **핵심 인사이트**: 벡터가 L2 정규화(L2 Normalized)되어 있는 경우, 코사인 유사도가 최대가 되는 조건과 L2 거리가 최소가 되는 조건은 수학적으로 완벽히 동일하며 내적과 코사인 유사도도 일치하게 됩니다. 이에 따라 실무에서는 연산 속도가 가장 빠른 내적을 주로 검색 인덱스용 지표로 사용합니다.

### 4. RecursiveCharacterTextSplitter의 재귀적 청킹 메커니즘
* **배움**:
  * 본 분할기는 지정한 구분자(separators) 리스트를 우선순위대로 탐색하면서 재귀적으로 쪼갭니다.
  * `chunk_size` 임계값을 300으로 설정했을 때 문서 내 각 문단이 250~280자 내외의 크기를 가지고 있으면, 첫 번째 구분자(`\n\n`)만으로 쪼갠 결과물이 이미 300자 이하 조건에 만족하여 후속 구분자(`\n`, `.`, ` ` 등)가 적용되지 않고 완벽하게 문단 단위로 깔끔히 보존되어 분할됩니다.
  * 텍스트 구조(의미적 자립성)와 목표 청크 사이즈의 기하학적 매칭이 RAG 시스템의 데이터 정밀도를 결정함을 이해했습니다.

---

## 📝 2026-06-16 실습 및 피드백 정리

### 1. 정규화된 벡터 공간의 기하학적 성질을 활용한 고속 검색
* **현상**: 임베딩 벡터를 미리 L2 Norm으로 나누어 단위 벡터로 만들어 두면, 분모 연산(크기 계산)이 생략되어 단순 내적(Dot Product, NumPy `@` 연산)만으로 코사인 유사도를 전수 계산할 수 있음을 실증했습니다.
* **배움**: 1:1 선형 대조 방식($O(N)$)은 데이터가 커질수록 병목이 되므로, 실무 대용량 검색 환경에서는 그래프 계층을 타고 빠르게 탐색하는 HNSW나 클러스터링 기반의 IVF 등의 ANN(근사 최근접 이웃) 인덱싱 적용이 왜 필수적인지 이론적으로 학습했습니다.

### 2. LangChain 추상화 레이어의 설계 구조와 타입 안정성 문제
* **현상**: `as_retriever` 메서드에서 `kwargs={'k':3}`로 파라미터를 넘겼을 때, 에러 없이 묵묵히 무시된 채 디폴트값(`k=4`)이 작동하여 4개의 결과가 출력되는 오동작을 겪었습니다.
* **배움**:
  * LangChain은 다양한 Vector DB(Chroma, Pinecone 등)의 이종 파라미터를 통합하기 위해 만능 `**kwargs`나 딕셔너리(`search_kwargs`) 방식을 사용하는데, 이로 인해 오타 발생 시 정적 분석이나 런타임 에러로 잡히지 않고 조용히 씹히는 구조적 단점이 존재함을 파악했습니다.
  * 실무에서는 이를 방어하기 위해 Pydantic이나 데이터 클래스를 활용하여 파라미터를 래핑하는 방식으로 타입 안정성을 강제할 필요가 있음을 깨달았습니다.

### 3. RDB와 Vector DB의 아키텍처적 차이 및 스키마 설계
* **배움**:
  * **스키마 유연성**: Chroma나 Pinecone 같은 Schema-less DB는 벡터 차원 정도만 정하고 메타데이터를 NoSQL처럼 동적으로 집어넣을 수 있으나, Milvus나 Qdrant 같은 엔터프라이즈급 DB는 필드명과 타입을 명시하는 Schema-full 형태를 취합니다.
  * **인덱싱 비용**: RDB는 인덱싱이 단순하고 가벼운 반면, Vector DB의 HNSW 등은 고차원 공간 지도를 빌드해야 하므로 메모리와 CPU를 비정상적으로 높게 점유하는 특징이 있습니다.

### 4. 전통 NLP와 LLM/RAG의 실무적 융합 및 시너지
* **배움**: LLM 임베딩의 의미론적(Semantic) 검색의 한계를 극복하기 위해, 전통적인 형태소 분석(문장 분리)을 통한 청크 전처리, 고유명사 매칭을 위한 BM25와의 하이브리드 검색, NER(개체명 인식)을 통한 메타데이터 필터 조건 자동 추출 등을 융합해야 비로소 프로덕션 수준의 RAG가 완성됨을 배웠습니다.

---

## 📝 2026-06-17 실습 및 피드백 정리

### 1. 하이브리드 RAG 및 중복 적재 방지 설계
* **현상**: Chroma DB에 동일한 데이터가 반복 적재(Append)되어 상위 유사도 결과가 중복 문서로 가득 차 정작 R&D 센터 보안 지침과 같은 다른 핵심 유관 문서가 밀려나는 오동작을 겪었습니다.
* **배움**:
  * RAG의 최종 성능은 Retriever가 LLM에 집어넣는 Context의 유일성과 정보 밀도에 좌우되므로, 적재 단계에서의 중복 데이터 제거(Deduplication)와 `delete_collection()` 등을 활용한 데이터 무결성 초기화 파이프라인 구축이 필수적임을 실증했습니다.
  * 키워드 기반 BM25(희소 벡터)와 Chroma(밀집 벡터)의 유사도 점수 스케일 격차를 해결하기 위해 순위 기반 융합 공식인 RRF(Reciprocal Rank Fusion)를 사용하여 하이브리드 검색을 오케스트레이션했습니다.

### 2. Parent-Document Retriever의 상속 오류 해결 및 계층화 검색
* **현상**: `ParentDocumentRetriever`에 `SemanticChunker`를 주입하자 Pydantic 타입 불일치 에러(`ValidationError`)를 겪었습니다.
* **배움**:
  * `SemanticChunker`가 `TextSplitter`가 아닌 `BaseDocumentTransformer`를 상속하기 때문임을 파악하고, `parent_splitter=None`으로 우회 선언한 뒤 직접 의미론적으로 자른 부모 청크 목록을 `add_documents()`에 주입하여 수동 매핑(Direct Mapping) 방식으로 문제를 정교하게 해결했습니다.
  * 이 과정을 통해 검색 정밀도를 위한 작은 자식 청크(150자)와 풍부한 답변 품질을 위한 큰 부모 청크(300~700자)의 계층적 맵 구조가 어떻게 작동하는지 원리를 이해했습니다.

### 3. 출처(Source) 보존형 LCEL 및 LLM-as-a-Judge 평가기 구축
* **배움**:
  * RAG 답변 도출 시 원본 문서의 소실을 막기 위해 `RunnableParallel`과 `.assign()` 문법을 활용하여 `{"answer": ..., "documents": [...]}` 형태로 출처를 동시 리턴하는 표준 LCEL 체인을 완성했습니다.
  * Ragas 프레임워크의 RAG 삼각측량 검증 원리(Faithfulness, Answer Relevance, Context Precision)를 분석했으며, 나아가 Pydantic `with_structured_output` API를 활용하여 사내 비즈니스 감사 규정에 맞춤 대응할 수 있는 순수 LLM 기반의 가드레일 평가기를 직접 제작하고 연동에 성공했습니다.

---

## 📝 2026-06-18 실습 및 피드백 정리

### 1. LangChain Hub 보안 패치에 따른 ValueError 대응
* **현상**: `hub.pull("hwchase17/react")` 호출 시 외부 원격 리포지토리로부터 검증되지 않은 객체가 직렬화되어 풀링되는 것을 차단하는 Pydantic 보안 규정으로 인해 `ValueError`가 발생했습니다.
* **배움**:
  * 이를 해결하기 위해 `dangerously_pull_public_prompt=True` 인수를 활용할 수 있지만, 현업 배포 관점에서는 네트워크 지연 및 외부 API 가용성 이슈를 해소하기 위해 ReAct용 프롬프트를 로컬 `PromptTemplate`으로 정의하여 외부 의존성을 제거하는 것이 훨씬 견고한 설계임을 이해했습니다.

### 2. ReAct 에이전트의 단일 텍스트 입력 한계 및 Pydantic ValidationError
* **현상**: 도구 함수 정의 시 복수의 float 인자(`a: float, b: float`)를 명시했을 때, ReAct 에이전트의 문자열 입력 포맷(`Action Input: 354.2, 12.8`)을 Pydantic이 적절히 캐스팅하지 못하고 유효성 에러를 일으켰습니다.
* **배움**:
  * ReAct 아키텍처는 에이전트 루프 상에서 단일 텍스트 인자를 전달하는 데 특화되어 있으므로, 복수 파라미터가 필요한 도구는 **단일 문자열 입력(Single-string Input)**을 받게 한 후 내부 파싱(split)을 수행하는 것이 시스템적 충돌을 예방하는 정석적인 우회책임을 배웠습니다.

### 3. Streamlit 상태 관리(Session State) 및 RAG 예외 방어선 구축
* **현상**: 질문을 입력할 때마다 Streamlit 전체 스크립트가 재실행되며 로컬 변수 `vectorstore`가 메모리에서 휘발하는 버그와, 스캔본 PDF 업로드 시 텍스트 파싱 실패로 빈 리스트가 Chroma에 주입되어 `ValueError`가 발생하는 문제를 확인했습니다.
* **배움**:
  * 리로딩 시 상태 지속성을 확보하기 위해 `st.session_state`를 도입하여 해결했으며, 빈 텍스트 유입을 사전에 차단하기 위한 **Guard Clause(예외 방어선)**를 구현하여 프로덕션 수준의 예외 처리를 체감했습니다.

### 4. 대규모 RAG 아키텍처 이원화 및 벡터 DB 설계 원칙
* **배움**:
  * 부하 격리(Fault Isolation)를 위해 무거운 배치 처리인 **데이터 적재(Ingestion) 파이프라인**과 실시간 서빙용 **검색/추론(Serving) API**를 물리적/논리적으로 완전히 이원화하는 설계 원칙을 학습했습니다.
  * 또한, HNSW 인덱스가 차지하는 극심한 RAM 비용 오버헤드를 고려할 때 무분별한 다중 컬렉션 분해보다는 **단일 컬렉션 적재 후 메타데이터 사전 필터링(Pre-filtering)**을 걸어주는 것이 실무적으로 가장 가성비 높고 정확한 설계 기법임을 파악했습니다.

---

## 📝 2026-06-19 실습 및 피드백 정리

### 1. LangGraph 기반 StateGraph 흐름 제어 및 안정성 방어선 설계
* **배움**:
  * 단순 선형 구조(LCEL 체인)를 넘어서는 순환성 루프 및 분기형 에이전트 구현을 위해, 전역 상태(State) 데이터를 노드 간에 전달하고 업데이트하는 LangGraph 프레임워크의 구조를 실증했습니다.
  * 루프 탐색 시 발생할 수 있는 무한 폭주 위험을 차단하고 런타임을 보호하기 위한 **`recursion_limit`** 기반 예외 차단 가드레일을 구축하여 프로덕션 수준의 시스템 안정성 장치를 학습했습니다.

### 2. 하이브리드 Reranker 결합을 통한 고정밀 Retrieval 설계
* **배움**:
  * 고유명사 키워드에 뛰어난 **BM25**와 자연어 문맥적 의미에 강한 **Chroma Vector Store**의 결과를 **Ensemble(RRF 융합)**하고, 이를 2차적으로 **Cross-Encoder Reranker(bge-reranker-base)**에 투입하는 고정밀 RAG 구조를 완성했습니다.
  * 이 하이브리드 조합이 Ragas 평가 결과 상에서 `Context Precision = 1.0`, `Context Recall = 1.0`이라는 완벽한 지표 성능을 도출해 내는 것을 실증함으로써, 정보 유실 방지와 핵심 정보 정렬이라는 두 마리 토끼를 모두 잡는 RAG의 설계 원칙을 정립했습니다.

### 3. Ragas RAG 정량 평가 프레임워크의 연동 및 트러블슈팅
* **배움**:
  * Ragas v0.2.x 이상에서 과도기적 컴포넌트 아키텍처 전환으로 인해 발생하는 `evaluate` 러너와 신규 `SimpleBaseMetric` 간의 타입 불일치 오류를 추적하여, 경고 제어 및 소문자 인스턴스 맵핑을 활용한 실무형 우회법으로 해결했습니다.
  * 답변 팩트가 일치함에도 마크다운 격자 기호(`|`) 형식의 테이블 구조를 NLI 추론기가 판별하지 못해 `Faithfulness` 점수가 낮게 잡히는 가짜 실패(False Negative) 현상을 관찰하고, 이를 극복하기 위해 **표의 자연어 서술화(Textualization)** 등 표 전처리 전략의 필수성을 이해했습니다.


