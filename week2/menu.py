import streamlit as st
import pandas as pd

@st.cache_data
def load_restaurant_data():
    # 필터링된 데이터 로드
    file_path = 'week2/content/식품_일반음식점_필터링결과.csv'
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    return df

def show_menu_tab():
    st.header("🍴 서초구 맛집 탐색기")
    st.write("원하시는 음식 종류를 선택하고 서초구의 식당을 확인해보세요!")

    # 데이터 로드
    with st.spinner('서초구 식당 데이터를 불러오는 중...'):
        df = load_restaurant_data()

    # 가능한 업태 리스트 (중복 제거 및 정렬)
    target_categories = [
        '한식', 
        '패스트푸드', 
        '중국식', 
        '일식', 
        '외국음식전문점(인도,태국등)', 
        '뷔페식', 
        '경양식'
    ]
    # 사용자 입력: 카테고리 선택
    selected_category = st.selectbox("어떤 종류의 음식을 찾으시나요?", target_categories)

    if st.button('🔍 식당 조회하기'):
        # Pandas의 다중 조건을 이용해 서초구(3210000)와 선택된 카테고리를 동시에 필터링
        seocho_filter = (df['개방자치단체코드'] == 3210000)
        category_filter = (df['업태구분명'] == selected_category)
        
        # 필요한 컬럼만 추출
        results = df[seocho_filter & category_filter][['사업장명', '업태구분명', '도로명주소', '지번주소']].copy()
        
        # URL 인코딩 및 링크용 컬럼 생성
        import urllib.parse
        results['식당정보'] = results.apply(
            lambda x: f"https://map.naver.com/p/search/{urllib.parse.quote(str(x['지번주소']))}?name={urllib.parse.quote(str(x['사업장명']))}", 
            axis=1
        )
        
        # 컬럼 순서 재배치: '식당정보'를 맨 앞으로! ('사업장명'은 숨길 예정이므로 제외 가능)
        results = results[['식당정보', '업태구분명', '도로명주소', '지번주소']]
        
        st.divider()
        if not results.empty:
            st.success(f"### 서초구 '{selected_category}' 카테고리에서 {len(results)}개의 식당을 찾았습니다!")
            
            # 리스트 형식으로 보여주기
            st.dataframe(
                results, 
                column_config={
                    "식당정보": st.column_config.LinkColumn(
                        "사업장명 (클릭 시 지도 이동)", 
                        display_text=r"\?name=(.*)"
                    ),
                    "업태구분명": st.column_config.TextColumn("업태구분명", width="small"),
                    "지번주소": st.column_config.TextColumn("지번주소", width="medium"),
                    "도로명주소": st.column_config.TextColumn("도로명주소", width="medium"),
                },
                width=True, 
                hide_index=True
            )
        else:
            st.warning(f"서초구 내 '{selected_category}' 카테고리에 해당하는 식당이 없습니다. 😅")
