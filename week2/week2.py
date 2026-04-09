import numpy as np
import streamlit as st
import pandas as pd

st.title("Hello")
st.write("I'm hong")
st.write(":red[streamlit] is :blue-background[best] :sunglasses:")


@st.dialog("인사하기") 
def hello_dialog():
    st.write("반가워요! 다이얼로그 창입니다.")
    
    if st.button("확인"):
        st.rerun()

st.button('다이얼로그', on_click=hello_dialog)


st.checkbox('동의하기', key='isAgree')

if st.session_state.isAgree:
    st.write('동의했습니다.')

st.selectbox(
    '좋아하는 과일은?', 
    ['사과', '바나나', '딸기'],
    key='fruit',
)
st.write(f'{st.session_state.fruit}을 선택하셨습니다.')

st.markdown("""
    # 제목
    ## 제목2
    - 목록
    - 목록
    1. 숫자
    2. 숫자

    **볼드**
    > 인용
    
    ```python
    print("Hello World")
    ```
    [링크](https://www.google.com)
    
""")


st.video('https://www.youtube.com/embed/zDKO6XYXioc?si=BlrIj4YVwrf05d0x')

st.metric(label='온도', value='25도', delta='2도')

df = pd.read_csv('week2/content/data_subway_in_seoul.csv', encoding='cp949')
st.dataframe(df.head(10))

st.dataframe(pd.DataFrame(np.random.randn(10, 2), columns=['a', 'b']).style.highlight_max(axis=1))