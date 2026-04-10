from typing import List, Optional, Dict, Any
import requests
import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series
from config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, NAVER_SEARCH_TREND_URL

# --- 1. Pandera Schema (DataFrame Validation & Column Access) ---

class NaverSearchTrendSchema(pa.DataFrameModel):
    """
    네이버 검색어 트렌드 데이터프레임 구조 정의 및 IDE 자동 완성을 지원하는 스키마.
    중첩된 응답 데이터를 평탄화(Flatten)한 구조를 따릅니다.
    """
    title: Series[str]
    period: Series[str]
    ratio: Series[float]

    @staticmethod
    def validate_df(data: List[dict]) -> pd.DataFrame:
        """딕셔너리 리스트를 데이터프레임으로 변환하고 스키마 검증"""
        df = pd.DataFrame(data)
        return NaverSearchTrendSchema.validate(df)

    class Config:
        strict = True
        coerce = True

# --- 2. Client Function ---

def get_naver_search_trend(start_date: str, end_date: str, time_unit: str, keyword_groups: List[Dict[str, Any]], 
                           device: str = "", gender: str = "", ages: List[str] = None) -> Optional[List[dict]]:
    """
    네이버 통합 검색어 트렌드 조회 API 호출 -> 평탄화된 딕셔너리 리스트 반환
    """
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        "Content-Type": "application/json"
    }

    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "keywordGroups": keyword_groups,
        "device": device if device else None,
        "gender": gender if gender else None,
        "ages": ages if ages else []
    }

    # 불필요한 None 항목 제거
    body = {k: v for k, v in body.items() if v is not None}

    try:
        response = requests.post(NAVER_SEARCH_TREND_URL, headers=headers, json=body)
        response.raise_for_status()
        res_data = response.json()
        
        # 중첩된 응답 데이터를 평탄화 (results -> data)
        flattened_rows = []
        for result in res_data.get('results', []):
            title = result.get('title')
            for entry in result.get('data', []):
                flattened_rows.append({
                    "title": title,
                    "period": entry.get('period'),
                    "ratio": entry.get('ratio')
                })
        
        return flattened_rows

    except Exception as e:
        print(f"Naver API Request failed: {e}")
        if 'response' in locals():
            print(f"Response: {response.text}")
    
    return None

# --- 실행 예시 ---
if __name__ == "__main__":
    # 1. 주제어 그룹 설정
    keyword_groups = [
        {"groupName": "한글", "keywords": ["한글", "korean"]},
        {"groupName": "영어", "keywords": ["영어", "english"]}
    ]

    # 2. 클라이언트를 통해 데이터 수집
    print("Fetching Naver Search Trend Data...")
    data = get_naver_search_trend(
        start_date="2023-01-01",
        end_date="2023-03-31",
        time_unit="month",
        keyword_groups=keyword_groups
    )
    
    if data:
        # 3. 스키마를 사용하여 데이터프레임 변환 및 검증
        df = NaverSearchTrendSchema.validate_df(data)
        
        print(f"조회 성공 (총 행수: {len(df)})")
        
        # 4. 필드명 속성으로 데이터 확인
        S = NaverSearchTrendSchema
        print(df[[S.title, S.period, S.ratio]].head())
    else:
        print("데이터 수집에 실패했습니다.")
