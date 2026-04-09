import streamlit as st
from .fortune import show_fortune_tab
from .menu import show_menu_tab
from .test import show_test_tab

# --- 공통 설정 ---
def setup_page():
    st.set_page_config(page_title="실습 앱", page_icon="🌟")

# --- 메인 실행부 ---
def main():
    setup_page()
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs(["🔮 오늘의 운세", "🍴 메뉴 추천", "🧠 성향 테스트"])
    
    with tab1:
        show_fortune_tab()
        
    with tab2:
        show_menu_tab()

    with tab3:
        show_test_tab()

    # 푸터
    st.divider()
    st.caption("© 2026 파이썬 실습.")

if __name__ == "__main__":
    main()
