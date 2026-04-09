import streamlit as st
import random
import time
import textwrap

def show_fortune_tab():
    st.header("🔮 오늘의 운세 한마디")
    st.write("성함을 입력하고 오늘의 행운을 확인하세요!")

    # 운세 문구 및 점수 (긍정: 3~5점, 부정: 1~2점)
    pos_fortunes = [
        {"text": "오늘은 새로운 도전을 해보기에 좋은 날입니다. 🚀", "score": 5},
        {"text": "작은 실수가 있어도 너무 걱정하지 마세요. 다 잘될 거예요! ✨", "score": 4},
        {"text": "생각지도 못한 곳에서 좋은 아이디어가 떠오를 수 있습니다. 💡", "score": 5},
        {"text": "오늘은 충분한 휴식이 필요한 날입니다. 자신을 돌봐주세요. 🌿", "score": 3},
        {"text": "주변 사람과의 대화에서 뜻밖의 좋은 기회를 얻을 수 있습니다. 🤝", "score": 4},
        {"text": "오늘은 운이 정말 좋네요! 복권을 사보는 건 어떨까요? 🍀", "score": 5},
        {"text": "맛있는 음식을 먹으면 기분이 훨씬 좋아질 거예요. 🍕", "score": 3},
        {"text": "오랫동안 연락하지 못한 친구에게 연락이 올 수도 있습니다. 📱", "score": 4}
    ]

    neg_fortunes = [
        {"text": "오늘은 지갑을 조심하세요. 예상치 못한 지출이 생길 수 있습니다. 💸", "score": 2},
        {"text": "중요한 약속 시간을 다시 한번 확인해보세요. 깜빡할 수도 있어요! ⏰", "score": 2},
        {"text": "오늘은 무리하게 운동하지 마세요. 몸에 무리가 올 수 있습니다. 🤕", "score": 1},
        {"text": "말실수로 인해 주변 사람과 오해가 생길 수 있으니 주의하세요. 🙊", "score": 2},
        {"text": "컴퓨터나 핸드폰이 갑자기 고장 날 수 있으니 미리 백업해두세요. 📱", "score": 1},
        {"text": "오늘은 새로운 일을 시작하기보다 기존의 일을 마무리하는 것이 좋습니다. 📁", "score": 2},
        {"text": "비가 올 수도 있으니 우산을 챙기는 것을 잊지 마세요. ☔", "score": 1},
        {"text": "오늘은 평소보다 일찍 귀가하여 휴식을 취하는 것이 상책입니다. 🏠", "score": 2},
        {"text": "인터넷 쇼핑은 자제하세요. 나중에 후회할 물건을 살 수도 있습니다. 🛒", "score": 1},
        {"text": "복잡한 곳은 피하세요. 기운이 빠질 수 있습니다. 😵‍💫", "score": 1}
    ]

    # 모든 운세를 합친 리스트
    all_fortunes = pos_fortunes + neg_fortunes

    # 별자리 리스트
    zodiac_signs = ["물병자리", "물고기자리", "양자리", "황소자리", "쌍둥이자리", "게자리", 
                    "사자자리", "처녀자리", "천칭자리", "전갈자리", "사수자리", "염소자리"]

    # st.form을 사용하여 엔터키 입력 시 버튼 클릭 효과를 줌
    with st.form(key='fortune_form'):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("성함을 입력해 주세요:", placeholder="예: 홍길동", key="fortune_name")
        with col2:
            zodiac = st.selectbox("별자리를 선택해 주세요:", zodiac_signs, key="fortune_zodiac")
            
        submit_button = st.form_submit_button(label='✨ 운세 보기')

    if submit_button:
        if name:
            with st.spinner('운세를 읽어오는 중입니다...'):
                time.sleep(1)
            
            picked = random.choice(all_fortunes)
            fortune_text = picked["text"]
            fortune_score = picked["score"]
            st.divider()
            
            # 점수를 별점으로 변환
            stars = "⭐" * fortune_score
            
            # 긍정/부정 판단 및 효과 연출
            if picked in pos_fortunes:
                st.balloons()
                st.success(f"### {zodiac}인 {name}님, 오늘의 기분 좋은 운세입니다!")
                st.subheader(f"오늘의 행운 지수: {stars} ({fortune_score}점)")
                st.info(f"**\"{fortune_text}\"**")
            else:
                st.snow()
                st.error(f"### {zodiac}인 {name}님, 오늘은 조금 주의가 필요한 날이네요...")
                st.subheader(f"오늘의 행운 지수: {stars} ({fortune_score}점)")
                st.warning(f"**\"{fortune_text}\"**")
            
            # 1. 포맷팅 함수 정의
            share_text = textwrap.dedent(f"""
                [오늘의 운세] {zodiac} {name}님
                오늘의 행운 지수: {stars} ({fortune_score}점)
                운세 한마디: "{fortune_text}"
            """).strip()

            # 2. 결과 하단에 공유 영역 추가
            with st.expander("✉️ 결과 공유하기"):
                st.write("아래 내용을 복사해서 친구에게 공유해 보세요!")
                st.code(share_text, language=None) # 언어 설정을 None으로 하여 가독성 확보

        else:
            st.warning("이름을 입력해야 운세를 볼 수 있어요! 😅")
