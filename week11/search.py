import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from config import GOOGLE_AI_API_KEY

# PDF 문서들에서 텍스트 및 메타데이터 추출 (Document 객체 구조 보존)
def get_pdf_documents(pdf_docs):
    all_documents = []
    for pdf in pdf_docs:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf.getvalue())
            temp_file_path = temp_file.name
        try:
            # extract_images=True 옵션을 제공하여 RapidOCR 엔진 기반 이미지 속 텍스트 추출 지원
            loader = PyPDFLoader(temp_file_path)
            documents = loader.load()
            
            # 임시 파일 경로가 아닌 업로드된 실제 파일명으로 source 메타데이터 덮어쓰기
            for doc in documents:
                doc.metadata["source"] = pdf.name
                # 페이지 번호를 1-indexed로 보정하여 직관성 확보
                if "page" in doc.metadata:
                    doc.metadata["page"] = doc.metadata["page"] + 1
            all_documents.extend(documents)
        finally:
            os.remove(temp_file_path)
    return all_documents

# 문서 청킹
def split_documents(documents, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

# 임베딩 & 벡터DB 생성
def get_vectorstore(documents):
    embeddings = GoogleGenerativeAIEmbeddings(
        model='gemini-embedding-2',
        output_dimensionality=256,
        api_key=GOOGLE_AI_API_KEY
    ) 
    # 기존 Chroma 컬렉션 중복 방지를 위해 유니크한 컬렉션명 할당
    import uuid
    collection_name = f"pdf_search_{uuid.uuid4().hex[:8]}"
    vectorstore = Chroma.from_documents(
        documents=documents, 
        embedding=embeddings,
        collection_name=collection_name
    )
    return vectorstore

# 검색된 문서들을 하나의 문자열로 합치는 함수
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG 체인 정의 (출처 보존형 LCEL 구조)
def get_conversation_chain(vectorstore, k=4):
    CHAT_MODEL = 'google_genai:gemma-4-31b-it'  
    llm = init_chat_model(CHAT_MODEL, api_key=GOOGLE_AI_API_KEY, temperature=0.1)

    prompt = PromptTemplate.from_template(
    """
    당신은 사내 문서 검색 및 분석 전문가입니다. 제공된 참고 자료(Context)만을 활용하여 질문에 친절하고 상세하게 답하세요.
    참고 자료에서 확인할 수 없는 내용은 거짓으로 지어내지 말고, 모른다고 명확히 답하세요. 한국어로 답변하세요.

    # Question : {question}
    # Context : {context}
    
    # Answer:
    """
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    # RunnableParallel과 assign을 활용해 답변과 검색된 원본 문서 목록을 동시에 회수
    rag_chain = RunnableParallel(
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
    ).assign(
        answer=(
            RunnablePassthrough.assign(
                context=lambda x: format_docs(x["context"])
            )
            | prompt
            | llm
            | StrOutputParser()
        )
    )

    return rag_chain

# PDF 전체 요약 생성 함수
def generate_summary(documents):
    CHAT_MODEL = 'google_genai:gemma-4-31b-it'
    llm = init_chat_model(CHAT_MODEL, api_key=GOOGLE_AI_API_KEY, temperature=0.2)
    
    # 문서 전체의 텍스트 병합 (메모리 제어를 위해 최대 80,000자 슬라이싱)
    full_text = "\n\n".join(doc.page_content for doc in documents)[:80000]
    
    prompt = PromptTemplate.from_template(
    """
    제공된 문서를 상세히 분석하고 핵심 요약본을 작성해 주세요.
    요약은 다음 형식을 지켜주세요:
    1. **핵심 요지 (3줄 요약)**
    2. **주요 주제별 요약 정리 (불릿 기호 활용)**
    3. **핵심 결론 및 인사이트**

    # Document Content:
    {text}
    
    # Summary:
    """
    )
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"text": full_text})

# Streamlit 페이지 설정
st.set_page_config(page_title="PDF RAG & Summary Assistant", layout="wide")
st.title("📕📝🔍 PDF 검색 & 요약 서비스")

# Streamlit 세션 상태 초기화
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "documents" not in st.session_state:
    st.session_state.documents = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_summary" not in st.session_state:
    st.session_state.pdf_summary = None

# 사이드바 설정 영역
st.sidebar.header("⚙️ RAG 설정")
chunk_size = st.sidebar.slider("청크 크기 (Chunk Size)", min_value=100, max_value=2000, value=400, step=50)
chunk_overlap = st.sidebar.slider("청크 오버랩 (Chunk Overlap)", min_value=0, max_value=500, value=40, step=10)
k_value = st.sidebar.slider("검색 문서 개수 (k)", min_value=1, max_value=10, value=4, step=1)

st.sidebar.write("---")

# PDF 파일 업로드
user_uploads = st.file_uploader("PDF 파일을 업로드해 주세요~~😁", accept_multiple_files=True)

if user_uploads:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("업로드 & 분석 🤪", use_container_width=True):
            with st.spinner("PDF 파싱 및 OCR 수행 중..."):
                documents = get_pdf_documents(user_uploads)
                if not documents:
                    st.error("텍스트를 추출하지 못했습니다.")
                else:
                    st.session_state.documents = documents
                    text_chunks = split_documents(documents, chunk_size, chunk_overlap)
                    if not text_chunks:
                        st.error("청킹 분할 실패")
                    else:
                        st.session_state.vectorstore = get_vectorstore(text_chunks)
                        st.session_state.chat_history = []  # 새 문서 로드 시 대화 초기화
                        st.session_state.pdf_summary = None  # 요약 초기화
                        st.success(f"완료! ({len(documents)}p, {len(text_chunks)} chunks)")
    with col2:
        if st.session_state.documents is not None:
            if st.button("📝 PDF 요약", use_container_width=True):
                with st.spinner("요약 작성 중..."):
                    try:
                        summary = generate_summary(st.session_state.documents)
                        st.session_state.pdf_summary = summary
                    except Exception as e:
                        st.error(f"요약 중 오류: {e}")
        else:
            st.button("📝 PDF 요약", disabled=True, use_container_width=True)

# 1. 요약 보고서 노출
if st.session_state.pdf_summary is not None:
    with st.expander("📄 PDF 전체 요약 보고서", expanded=True):
        st.markdown(st.session_state.pdf_summary)

# 2. 이전 대화 렌더링
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])
        if chat["role"] == "assistant" and chat.get("sources"):
            with st.expander("🔍 출처 및 참고 페이지 확인"):
                for idx, src in enumerate(chat["sources"]):
                    st.write(f"**[{idx+1}] {src['source']}** (Page {src['page']})")
                    st.caption(f"참고 문맥: {src['content']}")

# 3. 신규 질문 입력창 및 답변 처리
if user_question := st.chat_input("업로드된 문서에 대해 질문하세요!"):
    # 3.1. 사용자 질문 렌더링 및 세션 추가
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    
    # 3.2. 답변 추론
    if st.session_state.vectorstore is not None:
        with st.spinner("답변을 작성하고 있습니다..."):
            try:
                rag_chain = get_conversation_chain(st.session_state.vectorstore, k=k_value)
                response = rag_chain.invoke(user_question)
                
                answer = response["answer"]
                context_docs = response["context"]
                
                # 출처 메타데이터 추출 및 정리
                sources = []
                for doc in context_docs:
                    sources.append({
                        "source": doc.metadata.get("source", "알 수 없음"),
                        "page": doc.metadata.get("page", "알 수 없음"),
                        "content": doc.page_content[:200].strip() + "..."
                    })
                
                # 어시스턴트 응답 렌더링 및 기록 추가
                with st.chat_message("assistant"):
                    st.markdown(answer)
                    with st.expander("🔍 출처 및 참고 페이지 확인"):
                        for idx, src in enumerate(sources):
                            st.write(f"**[{idx+1}] {src['source']}** (Page {src['page']})")
                            st.caption(f"참고 문맥: {src['content']}")
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
            except Exception as e:
                st.error(f"답변 처리 에러: {e}")
    else:
        st.warning("먼저 PDF 파일을 사이드바에서 '업로드 & 분석 🤪' 한 뒤 질문을 입력하세요.")