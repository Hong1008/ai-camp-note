# Week 14: 멀티모달 LLM(LMM) 실무 및 멀티모달 RAG 설계 (14주차)

14주차 멀티모달 LLM 실습을 위한 학습 저장소입니다. 이번 주차의 학습 내용과 실습 코드를 기록합니다.

---

## 🗓️ 학습 로드맵 및 수행 결과

### 🟢 Theme 52: 멀티모달 LLM (LMM) API 제어 및 스키마 검증 (2026-07-06) [완료]
- **핵심 키워드**: Large Multimodal Models (LMM), Vision/Video Input, Structured Output, Pydantic Schema Validation, Multimodal RAG, CLIP/SigLIP
- **실습 수행 내용**:
    - **LMM Vision API 호출 및 스키마 기반 정형화**: OpenAI 및 Google GenAI SDK를 활용하여 로컬 이미지 분석을 수행하고, Pydantic으로 출력 스키마를 강제한 뒤 Pandera를 활용해 정규화된 바운딩 박스 데이터의 무결성을 런타임에 검증하는 프로덕션 레벨의 파이프라인 구축 완료.
    - **CLIP 기반 Zero-shot 이미지 분류 및 임베딩 검색**: CLIP(ViT-B/32) 모델을 통해 텍스트-이미지 임베딩 유사도를 구하고, 별도의 재학습 없이 고양이를 분류(97.03% 확률) 및 텍스트 쿼리를 기반으로 유사도가 높은 이미지를 검색하여 시각화하는 Image Search 구현 완료.
    - **LangChain & Chroma 기반 멀티모달 RAG 체인 구축**: Chroma 벡터 DB와 Gemini Embedding 2를 연동하여 이미지 요약 정보를 검색하고, Gemma-4 모델로 질문에 답하는 LCEL RAG 체인을 구축하고 에러 디버깅(Gemma 모델의 system_instruction 호환 에러(500) 분석 및 해결) 완료.


### 🟡 Theme 53: STT 및 TTS 실무와 음성 멀티모달 파이프라인 (2026-07-08) [준비]
- **핵심 키워드**: Speech-to-Text (STT), Text-to-Speech (TTS), Multimodal Audio, Whisper API, google-genai Client, Pandera Validation, Fallback Strategy
- **실습 수행 내용**:
    - **OpenAI Whisper STT 및 TTS 실무**: OpenAI API(whisper-1, tts-1)를 이용해 한국어 음성을 전사하고, tts-1 및 다양한 목소리 톤(nova, shimmer)으로 자연스러운 문장 음성 파일 합성을 수행함.
    - **Gemini Multimodal Audio 직접 이해**: 오디오 파일 bytes를 Gemini 2.0 Flash 모델에 직접 주입(types.Part.from_bytes)하여 별도 STT 단계 없이 목소리 분위기, 어조 및 내용을 종합 분석함.
    - **Production-Level Voice-to-Voice 파이프라인 구축**: 사용자 음성 입력 -> STT -> Pandera 입력 검증 -> Gemini 2.0 추론 -> Pandera 답변 검증 -> TTS 변환으로 이어지는 연쇄 체인을 구현하고, 검증 실패 시 경고 음성 Fallback 가드레일을 적용함.

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- **학습 콘텐츠**:
    - [07-06.ipynb](07-06.ipynb): 멀티모달 LMM Vision API 제어, CLIP 이미지 검색, 멀티모달 RAG 실습 노트북
    - [07-08.ipynb](07-08.ipynb): STT 및 TTS 실무와 음성 멀티모달 파이프라인 실습 노트북
    - [troubleshooting/](troubleshooting/): 실습 과정에서 발생하는 이미지 인코딩, API 제한, 스키마 불일치 등 오류 해결 가이드 기록 폴더
- **트러블슈팅 리포트**:
    - [troubleshooting/README.md](troubleshooting/README.md): 발생한 이슈와 해결 방안 요약

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `openai`, `google-genai`, `anthropic`, `pydantic`, `pandera`, `pillow`, `matplotlib`, `speechrecognition`, `pydub`

