import streamlit as st
import time

def show_test_tab():
    st.header("🧠 MBTI 성향 테스트")
    st.write("각 단계의 질문에 답하고 당신의 MBTI 유형을 확인해보세요!")

    # 세션 상태 초기화 (단계 및 답변 저장용)
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'mbti_answers' not in st.session_state:
        st.session_state.mbti_answers = {}

    # 성향 테스트 데이터 구조화 (딕셔너리)
    questions_data = {
        "1. 에너지 방향 (E vs I)": [
            {"id": "e1", "q": "Q1. 주말에 에너지를 얻는 방법은?", "options": ["집에서 편안하게 휴식", "밖에서 친구들과 만남"], "types": ["I", "E"]},
            {"id": "e2", "q": "Q2. 새로운 사람을 만날 때 나는?", "options": ["상대가 먼저 말을 걸 때까지 기다림", "내가 먼저 활발하게 말을 검"], "types": ["I", "E"]},
            {"id": "e3", "q": "Q3. 여러 명이 모인 파티나 모임에서?", "options": ["금방 지쳐서 빨리 집에 가고 싶음", "즐겁게 놀며 오히려 에너지를 얻음"], "types": ["I", "E"]}
        ],
        "2. 인식 방식 (N vs S)": [
            {"id": "s1", "q": "Q4. 영화를 볼 때 더 끌리는 장르는?", "options": ["현실적인 실화 바탕의 이야기", "상상력이 풍부한 판타지나 SF"], "types": ["S", "N"]},
            {"id": "s2", "q": "Q5. 새로운 가전제품의 설명서를 읽을 때?", "options": ["처음부터 끝까지 꼼꼼하게 읽음", "대충 훑어보고 감으로 일단 시작"], "types": ["S", "N"]},
            {"id": "s3", "q": "Q6. 미래에 대해 생각할 때 나의 모습은?", "options": ["현재의 구체적인 계획을 세우는 편", "다양한 가능성과 상상의 나래를 폄"], "types": ["S", "N"]}
        ],
        "3. 판단 기준 (T vs F)": [
            {"id": "t1", "q": "Q7. 친구가 고민을 털어놓을 때 나의 반응은?", "options": ["실질적인 해결책을 제시함", "진심으로 공감해주고 위로함"], "types": ["T", "F"]},
            {"id": "t2", "q": "Q8. 일을 처리할 때 더 중요하게 생각하는 것?", "options": ["객관적인 사실과 논리적인 근거", "주변 사람들의 기분과 상황"], "types": ["T", "F"]},
            {"id": "t3", "q": "Q9. 타인에게 비판을 들었을 때 나는?", "options": ["그 내용이 맞는지 논리적으로 따져봄", "서운하거나 속상한 감정이 먼저 듦"], "types": ["T", "F"]}
        ],
        "4. 생활 양식 (J vs P)": [
            {"id": "j1", "q": "Q10. 여행을 갈 때 나의 스타일은?", "options": ["시간 단위로 철저하게 계획을 세움", "목적지만 정하고 발길 닿는 대로 다님"], "types": ["J", "P"]},
            {"id": "j2", "q": "Q11. 업무나 과제를 할 때 나의 모습은?", "options": ["마감 기한보다 훨씬 미리 끝내는 편", "마지막까지 미루다 벼락치기로 끝냄"], "types": ["J", "P"]},
            {"id": "j3", "q": "Q12. 주변 정리를 할 때 나는?", "options": ["정해진 자리에 항상 두려고 노력함", "그때그때 편한 곳에 두는 편"], "types": ["J", "P"]}
        ]
    }

    # MBTI 유형별 설명 데이터
    mbti_info = {
        "ISTJ": {"title": "청렴결백한 논리주의자", "desc": "사실에 근거하여 사고하며, 맡은 바 책임을 다하는 현실 주의자입니다. 📋"},
        "ISFJ": {"title": "용감한 수호자", "desc": "주변 사람들을 보호하고 헌신하며, 따뜻한 마음을 가진 수호자입니다. 🛡️"},
        "INFJ": {"title": "선의의 옹호자", "desc": "조용하고 신비로우며 샘솟는 영감으로 가득 찬 이상주의자입니다. ✨"},
        "INTJ": {"title": "용의주도한 전략가", "desc": "상상력이 풍부하며 철저한 계획을 세우는 전략가입니다. ♟️"},
        "ISTP": {"title": "만능 재주꾼", "desc": "대담하고 현실적인 성향으로 다양한 도구 사용에 능숙한 재주꾼입니다. 🛠️"},
        "ISFP": {"title": "호기심 많은 예술가", "desc": "항상 새로운 것을 찾아 도전하는 융통성 있는 예술가입니다. 🎨"},
        "INFP": {"title": "열정적인 중재자", "desc": "상냥하고 이타주의적인 성향으로 더 나은 세상을 꿈꾸는 중재자입니다. 🧚"},
        "INTP": {"title": "논리적인 사색가", "desc": "끊임없이 새로운 지식을 갈구하는 혁신적인 사색가입니다. 🔍"},
        "ESTP": {"title": "모험을 즐기는 사업가", "desc": "벼랑 끝의 아슬아슬한 삶을 즐기는 명석하고 에너지 넘치는 사업가입니다. 🏎️"},
        "ESFP": {"title": "자유로운 영혼의 연예인", "desc": "주변에 있으면 지루할 틈이 없는 즉흥적이고 에너지 넘치는 연예인입니다. 💃"},
        "ENFP": {"title": "재기발랄한 활동가", "desc": "창의적이며 항상 웃을 거리를 찾아다니는 열정적인 활동가입니다. 🌈"},
        "ENTP": {"title": "뜨거운 논쟁을 즐기는 변론가", "desc": "지적인 도전을 두려워하지 않는 영리하고 호기심 많은 변론가입니다. 🗣️"},
        "ESTJ": {"title": "엄격한 관리자", "desc": "사물이나 사람을 관리하는 데 타의 추종을 불허하는 관리자입니다. 🏛️"},
        "ESFJ": {"title": "사교적인 외교관", "desc": "타인에게 관심이 많고 사교성이 풍부하며 친절한 외교관입니다. 🤝"},
        "ENFJ": {"title": "정의로운 사회운동가", "desc": "카리스마와 열정을 지닌 영향력 있는 사회운동가입니다. 📢"},
        "ENTJ": {"title": "대담한 통솔자", "desc": "대담하고 상상력이 풍부하며 의지가 강한 리더입니다. 👑"}
    }

    categories = list(questions_data.keys())

    # --- 페이지 렌더링 시작 ---
    if st.session_state.step < len(categories):
        # 진행 중인 단계의 질문 표시
        current_category = categories[st.session_state.step]
        st.subheader(current_category)
        
        # 현재 단계의 답변 임시 저장용
        temp_answers = {}
        for item in questions_data[current_category]:
            # index=None을 설정하여 초기 선택값을 없앰
            temp_answers[item["id"]] = st.radio(item["q"], item["options"], key=f"radio_{item['id']}", index=None)
        
        st.divider()
        
        # 모든 질문에 답했는지 확인
        all_answered = all(val is not None for val in temp_answers.values())

        # 단계 제어 버튼
        if st.session_state.step < len(categories) - 1:
            if st.button("다음 단계로 ➡️"):
                if all_answered:
                    # 현재 선택한 답변을 세션 상태에 저장
                    st.session_state.mbti_answers.update(temp_answers)
                    st.session_state.step += 1
                    st.rerun()
                else:
                    st.warning("⚠️ 해당 섹션의 모든 질문에 답해 주세요!")
        else:
            if st.button("📊 결과 보기"):
                if all_answered:
                    # 마지막 단계의 답변 저장 및 결과 모드 진입
                    st.session_state.mbti_answers.update(temp_answers)
                    st.session_state.step = 99 # 결과 페이지용 임의의 값
                    st.rerun()
                else:
                    st.warning("⚠️ 모든 질문에 답해 주셔야 결과를 분석할 수 있습니다!")

    else:
        # --- 결과 화면 ---
        with st.spinner('MBTI 성향 분석 중...'):
            time.sleep(1.0)
        
        # 지표별 점수 계산
        counts = {"E": 0, "I": 0, "N": 0, "S": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        
        # 저장된 전체 답변을 기반으로 채점
        for category, q_list in questions_data.items():
            for item in q_list:
                selected_answer = st.session_state.mbti_answers.get(item["id"])
                if selected_answer:
                    answer_index = item["options"].index(selected_answer)
                    mbti_type = item["types"][answer_index]
                    counts[mbti_type] += 1
        
        # 최종 MBTI 유형 결정
        mbti_result = ""
        mbti_result += "E" if counts["E"] > counts["I"] else "I"
        mbti_result += "N" if counts["N"] > counts["S"] else "S"
        mbti_result += "T" if counts["T"] > counts["F"] else "F"
        mbti_result += "J" if counts["J"] > counts["P"] else "P"

        st.balloons()
        result_info = mbti_info.get(mbti_result, {"title": "신비로운 유형", "desc": "정의할 수 없는 독특한 매력을 가진 분이시네요!"})
        
        st.subheader(f"당신의 MBTI 유형은? **[{mbti_result}]**")
        st.markdown(f"### **\"{result_info['title']}\"**")
        st.info(result_info['desc'])
        
        with st.expander("📊 상세 분석 지표 보기"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"- 에너지 방향: E({counts['E']}) vs I({counts['I']})")
                st.write(f"- 인식 방식: N({counts['N']}) vs S({counts['S']})")
            with col2:
                st.write(f"- 판단 기준: T({counts['T']}) vs F({counts['F']})")
                st.write(f"- 생활 양식: J({counts['J']}) vs P({counts['P']})")
        
        st.divider()
        if st.button("🔄 테스트 다시 하기"):
            st.session_state.step = 0
            st.session_state.mbti_answers = {}
            st.rerun()
