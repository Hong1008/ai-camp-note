import streamlit as st
import json
import logging
from pathlib import Path
import plotly.graph_objects as go

from week10.mini_project import config
from week10.mini_project.core.interview import InterviewManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_korean_ordinal(n: int) -> str:
    ordinals = {1: "첫번째", 2: "두번째", 3: "세번째", 4: "네번째", 5: "다섯번째"}
    return ordinals.get(n, f"{n}번째")


# Set Streamlit Page Config
st.set_page_config(
    page_title="AI 면접관 (AI Interviewer)",
    page_icon="🤖",
    layout="wide"
)

# Apply sleek styling (Dark theme compatibility, custom cards, metrics styling)
st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1F77B4;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .subheader {
            font-size: 1.1rem;
            color: #888888;
            margin-bottom: 2rem;
            text-align: center;
        }
        .metric-container {
            background-color: #1E1E1E;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #333333;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #00CC96;
            margin-bottom: 0.5rem;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #AAAAAA;
            text-transform: uppercase;
        }
        .thought-box {
            background-color: #151515;
            border-left: 4px solid #AB47BC;
            padding: 1rem;
            border-radius: 0 5px 5px 0;
            font-family: monospace;
            font-size: 0.85rem;
            color: #CCCCCC;
            margin: 1rem 0;
            white-space: pre-wrap;
        }
        .question-box {
            # background-color: #1F2937;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 5px solid #1F77B4;
            margin-bottom: 1.5rem;
            font-size: 1.15rem;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to load personas for Setup screen
def load_personas() -> dict:
    try:
        with open(config.PERSONA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("personas", {})
    except Exception as e:
        logger.error(f"Failed to load personas: {e}")
        return {}

personas = load_personas()

# Initialize session states
if "phase" not in st.session_state:
    st.session_state.phase = "setup"
if "manager" not in st.session_state:
    st.session_state.manager = None
if "current_text" not in st.session_state:
    st.session_state.current_text = ""
if "question_num" not in st.session_state:
    st.session_state.question_num = 0
if "eval_details" not in st.session_state:
    st.session_state.eval_details = None
if "final_report" not in st.session_state:
    st.session_state.final_report = None
if "current_thinking_history" not in st.session_state:
    st.session_state.current_thinking_history = []


# ---------------------------------------------------------
# Phase 1: Setup Screen
# ---------------------------------------------------------
if st.session_state.phase == "setup":
    st.markdown('<div class="main-header">🤖 AI 면접관 (AI Interviewer)</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">실무급 기술 질문과 꼬리질문으로 당신의 개발 역량을 평가하고 상세 리포트를 제공합니다.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 1. 면접 기본 정보")
        role = st.selectbox(
            "지원 직무 선택",
            options=["ai_engineer", "python_backend"],
            format_func=lambda x: "AI 엔지니어 (AI Engineer)" if x == "ai_engineer" else "Python 백엔드 개발자 (Python Backend)"
        )
        
        interview_type = st.selectbox(
            "면접 유형 선택",
            options=["technical", "project"],
            format_func=lambda x: "기술 개념 면접 (Technical)" if x == "technical" else "프로젝트 경험 면접 (Project)"
        )
        
        max_questions = st.slider(
            "진행할 핵심 질문 개수 선택",
            min_value=1,
            max_value=5,
            value=3
        )
        
        selected_model = st.selectbox(
            "평가 LLM 모델 선택",
            options=config.AVAILABLE_MODELS,
            index=0 if config.MODEL_NAME == "gemini-3.1-flash-lite" else 1,
        )
        
    with col2:
        st.markdown("### 2. 면접관 성향(페르소나) 선택")
        persona_options = list(personas.keys())
        selected_persona_key = st.selectbox(
            "면접관 스타일",
            options=persona_options,
            format_func=lambda x: f"{personas[x].get('label', x)} - {personas[x].get('description', '')}"
        )
        
        # Display selected persona details
        st.info(
            f"**어조**: {personas[selected_persona_key].get('tone', '')}\n\n"
            f"**질문 스타일**:\n" + 
            "\n".join([f"- {d}" for d in personas[selected_persona_key].get('style_directives', [])])
        )

    st.markdown("---")
    
    # Start button centered
    _, mid_col, _ = st.columns([1, 1, 1])
    with mid_col:
        if st.button("🚀 AI 면접 시작하기", use_container_width=True):
            # Instantiate Interview Manager
            st.session_state.manager = InterviewManager(
                role=role,
                persona_key=selected_persona_key,
                interview_type=interview_type,
                max_questions=max_questions,
                model_name=selected_model
            )
            
            # Fetch first question
            first_q = st.session_state.manager.prepare_next_question()
            if first_q:
                st.session_state.current_text = first_q
                st.session_state.question_num = 1
                st.session_state.phase = "asking"
                st.session_state.eval_details = None
                st.session_state.final_report = None
                st.session_state.current_thinking_history = []
                st.rerun()
            else:
                st.error("질문 은행에서 조건에 맞는 질문을 로드하지 못했습니다.")

# ---------------------------------------------------------
# Phase 2: Asking (Chat / Interview screen)
# ---------------------------------------------------------
elif st.session_state.phase == "asking":
    manager = st.session_state.manager
    
    # 두 개의 컬럼으로 화면을 나눔: 왼쪽은 면접 UI, 오른쪽은 생각과정 토글 리스트
    col_main, col_think = st.columns([3, 2], gap="large")
    
    with col_main:
        st.markdown(f"### 💬 질문 {st.session_state.question_num} / {manager.max_questions}")
        st.progress(st.session_state.question_num / manager.max_questions)
        
        # Question text highlighted
        st.markdown(f'<div class="question-box">{st.session_state.current_text}</div>', unsafe_allow_html=True)
        
        # Render chat dialogue history for the current question
        if len(manager.current_turn_history) > 1:
            st.markdown("##### 💬 대화 흐름")
            for turn in manager.current_turn_history[1:]:
                role = turn["role"]
                content = turn["content"]
                with st.chat_message("user" if role == "user" else "assistant"):
                    st.write(content)
                    
        st.markdown("---")
        
        # Initialize submitting state
        if "is_submitting" not in st.session_state:
            st.session_state.is_submitting = False

        # Input Area
        user_answer = st.text_area(
            "답변을 입력해 주세요. (질문당 최소 답변 글자수 충족 필요)", 
            key="user_answer_input", 
            height=150, 
            placeholder="여기에 답변을 기술해 주세요...",
            disabled=st.session_state.is_submitting
        )
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            submit_btn = st.button(
                "📤 답변 제출", 
                use_container_width=True, 
                disabled=st.session_state.is_submitting
            )
            
        if submit_btn and not st.session_state.is_submitting:
            if not user_answer.strip():
                st.warning("답변을 입력해 주세요.")
            else:
                st.session_state.is_submitting = True
                # 생각과정 표시용 placeholder 추가
                if "current_thinking_history" not in st.session_state:
                    st.session_state.current_thinking_history = []
                st.session_state.current_thinking_history.append({
                    "label": "생각 중...",
                    "thinking": "AI 면접관이 답변을 심사하며 채점 기준과 루브릭을 검토하는 중입니다...",
                    "status": "thinking"
                })
                st.rerun()

    with col_think:
        st.markdown("### 🧠 면접관 생각과정 (Thinking)")
        if not st.session_state.current_thinking_history:
            st.info("지원자님의 답변이 제출되면 AI 면접관이 점수를 매기고 꼬리질문을 판단하는 추론 과정(Reasoning)이 실시간으로 여기에 노출됩니다.")
        else:
            for idx, log in enumerate(st.session_state.current_thinking_history):
                # 마지막 생각인 경우 펼쳐두고, 이전 것은 접어둠
                expanded = (log["status"] == "thinking" or idx == len(st.session_state.current_thinking_history) - 1)
                with st.expander(log["label"], expanded=expanded):
                    st.markdown(f'<div class="thought-box">{log["thinking"]}</div>', unsafe_allow_html=True)

    # Process evaluation synchronously when is_submitting is True
    if st.session_state.is_submitting:
        with st.spinner("AI 면접관이 답변을 평가 중입니다... (Thinking ON)"):
            msg, details = manager.process_answer(user_answer)
        
        # Get thinking process
        thinking_process = manager.llm.last_thinking
        
        # Update the thinking history placeholder
        turn_index = len(st.session_state.current_thinking_history)
        st.session_state.current_thinking_history[-1] = {
            "label": f"{get_korean_ordinal(turn_index)} 답변에 대한 생각과정",
            "thinking": thinking_process if thinking_process else "생각 과정을 가져오지 못했거나 모델의 추론 과정이 비어 있습니다.",
            "status": "completed"
        }
        
        st.session_state.is_submitting = False
        
        # Check outcome type
        if details["type"] == "gate_failed":
            # Length gate failed, remove placeholder
            st.session_state.current_thinking_history.pop()
            st.warning(msg)
            st.rerun()
        elif details["type"] == "follow_up":
            # Follow-up generated, stays in asking phase, update current_text
            st.session_state.current_text = msg
            st.success("꼬리질문이 생성되었습니다.")
            st.rerun()
        elif details["type"] == "feedback":
            # Question completed, move to evaluating phase
            st.session_state.eval_details = details["data"]
            st.session_state.phase = "evaluating"
            st.rerun()


# ---------------------------------------------------------
# Phase 3: Evaluating (Intermediate Feedback screen)
# ---------------------------------------------------------
elif st.session_state.phase == "evaluating":
    manager = st.session_state.manager
    eval_data = st.session_state.eval_details["evaluation"]
    model_answer = st.session_state.eval_details["model_answer"]
    feedback = st.session_state.eval_details["feedback"]
    
    st.success("🎉 해당 질문에 대한 면접 및 평가가 완료되었습니다!")
    st.markdown(f"### 📊 질문 {st.session_state.question_num} 채점 리포트")
    
    # 1. Metric Scores
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{eval_data['logic_score']} / 5</div>
                <div class="metric-label">논리성 (Logic)</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{eval_data['detail_score']} / 5</div>
                <div class="metric-label">구체성 (Detail)</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{eval_data['delivery_score']} / 5</div>
                <div class="metric-label">전달력 (Delivery)</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Layout splits Checklist vs Chart
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("##### ✅ 채점 기준 만족 여부")
        q_bank_points = manager.current_question["eval_points"]
        results = eval_data["eval_point_results"]
        
        for i, point in enumerate(q_bank_points):
            satisfied = results[i] if i < len(results) else False
            if satisfied:
                st.write(f"🟢 **충족** - {point}")
            else:
                st.write(f"🔴 **미흡** - {point}")
                
    with col_right:
        # Plotly horizontal bar chart for scores
        categories = ['논리성 (Logic)', '구체성 (Detail)', '전달력 (Delivery)']
        scores = [eval_data['logic_score'], eval_data['detail_score'], eval_data['delivery_score']]
        
        fig = go.Figure(go.Bar(
            x=scores,
            y=categories,
            orientation='h',
            marker_color=['#1F77B4', '#00CC96', '#AB47BC'],
            text=scores,
            textposition='auto',
        ))
        fig.update_layout(
            title="영역별 평가 차트",
            xaxis=dict(range=[0, 5.5], dtick=1),
            margin=dict(l=20, r=20, t=40, b=20),
            height=200,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    # Tabs for Feedback vs Model Answer
    tab1, tab2 = st.tabs(["💡 면접 피드백 (Feedback)", "📘 모범 답안 (Model Answer)"])
    with tab1:
        st.info(feedback)
    with tab2:
        st.write(model_answer)
        
    st.markdown("---")
    
    # Navigation Button
    _, mid_col, _ = st.columns([1, 1, 1])
    with mid_col:
        button_label = "🏁 최종 평가서 생성하기" if st.session_state.question_num >= manager.max_questions else "➡️ 다음 질문으로 이동"
        if st.button(button_label, use_container_width=True):
            if st.session_state.question_num >= manager.max_questions:
                # Compile Final Report
                with st.spinner("전체 면접 데이터를 바탕으로 종합 평가 리포트를 작성 중입니다..."):
                    st.session_state.final_report = manager.generate_final_report()
                st.session_state.phase = "report"
                st.rerun()
            else:
                # Prepare next question
                next_q = manager.prepare_next_question()
                if next_q:
                    st.session_state.current_text = next_q
                    st.session_state.question_num += 1
                    st.session_state.phase = "asking"
                    st.session_state.eval_details = None
                    st.session_state.current_thinking_history = []
                    st.rerun()
                else:
                    st.error("질문을 로드하지 못했습니다.")

# ---------------------------------------------------------
# Phase 4: Final Report Screen
# ---------------------------------------------------------
elif st.session_state.phase == "report":
    manager = st.session_state.manager
    report = st.session_state.final_report
    stats = manager.get_summary_statistics()
    
    st.markdown('<div class="main-header">🏆 종합 면접 평가 결과 보고서</div>', unsafe_allow_html=True)
    st.markdown(
        f"<div class='subheader'>직무: {'AI 엔지니어' if manager.role == 'ai_engineer' else 'Python 백엔드 개발자'} | "
        f"유형: {'기술 면접' if manager.interview_type == 'technical' else '프로젝트 면접'} | "
        f"면접관 스타일: {manager.persona.get('label', '중립형')} | "
        f"사용 모델: {manager.model_name}</div>", 
        unsafe_allow_html=True
    )
    
    # 1. Aggregate Stats Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{stats['avg_total_score']} / 5</div>
                <div class="metric-label">평균 종합 점수</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{stats['avg_logic_score']} / 5</div>
                <div class="metric-label">평균 논리성</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{stats['avg_detail_score']} / 5</div>
                <div class="metric-label">평균 구체성</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{stats['overall_criteria_fulfillment_rate']}%</div>
                <div class="metric-label">채점 기준 충족률</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # 2. Plotly chart representing average scores
    col_chart, col_summary = st.columns([1, 1])
    
    with col_chart:
        categories = ['논리성 (Logic)', '구체성 (Detail)', '전달력 (Delivery)']
        scores = [stats['avg_logic_score'], stats['avg_detail_score'], stats['avg_delivery_score']]
        
        # Build spider/radar chart or bar chart
        fig = go.Figure(data=go.Scatterpolar(
            r=scores + [scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line_color='#00CC96',
            marker=dict(size=8)
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5])
            ),
            title="역량 프로파일 분석",
            template="plotly_dark",
            height=300,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_summary:
        st.markdown("##### 📝 종합 총평")
        st.write(report.summary)
        
    st.markdown("---")
    
    # 3. LLM Report Syntheses (Strengths, Weaknesses, Study roadmap)
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("##### 👍 핵심 강점 (Strengths)")
        for strength in report.strengths:
            st.write(f"🔹 {strength}")
            
        st.markdown("##### ⚠️ 보완점 (Weaknesses)")
        for weakness in report.weaknesses:
            st.write(f"🔸 {weakness}")
            
    with col_r:
        st.markdown("##### 📚 실무 학습 추천 (Recommendations)")
        for rec in report.recommendations:
            st.write(f"📝 {rec}")
            
    st.markdown("---")
    
    # 4. Detailed transcripts accordion/expanders list
    st.markdown("### 💬 문항별 면접 상세 내용 및 채점 추론 과정")
    for i, turn in enumerate(manager.transcript):
        with st.expander(f"질문 {i+1}: {turn['question'][:50]}..."):
            st.write(f"**원본 질문**: {turn['question']}")
            st.write(f"**주제**: {turn['topic']} | **난이도**: {turn['difficulty']}")
            st.write("---")
            
            st.write("**💬 면접 대화록:**")
            for item in turn["candidate_conversation"]:
                speaker = "면접관 (AI)" if item["role"] == "assistant" else "지원자 (본인)"
                st.write(f"**{speaker}**: {item['content']}")
            st.write("---")
            
            st.write("**📊 채점 점수:**")
            st.write(f"논리성: {turn['evaluation']['logic_score']} | 구체성: {turn['evaluation']['detail_score']} | 전달력: {turn['evaluation']['delivery_score']}")
            st.write(f"**피드백**: {turn['feedback']}")
            st.write(f"**모범 답안**: {turn['model_answer']}")
            st.write("---")
            
            # AI's Thinking process visualization (Wow factor!)
            thinking_content = turn.get("thinking", "")
            if thinking_content:
                st.markdown("**🧠 AI의 채점 추론 과정 (Thinking Process):**")
                st.markdown(f'<div class="thought-box">{thinking_content}</div>', unsafe_allow_html=True)
                
    st.markdown("---")
    
    # Restart Button
    _, mid_col, _ = st.columns([1, 1, 1])
    with mid_col:
        if st.button("🔄 처음으로 돌아가기 (새 면접 시작)", use_container_width=True):
            st.session_state.phase = "setup"
            st.session_state.manager = None
            st.session_state.current_text = ""
            st.session_state.question_num = 0
            st.session_state.eval_details = None
            st.session_state.final_report = None
            st.rerun()