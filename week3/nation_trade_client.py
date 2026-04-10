from typing import List, Optional
import requests
import xmltodict
import urllib.parse
import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series
from config import NATION_TRADE_API_URL, DATA_GO_KR_API_KEY

# --- 1. Pandera Schema (DataFrame Validation & Column Access) ---

class NationTradeSchema(pa.DataFrameModel):
    """
    국가별 수출입 현황 데이터프레임 구조 정의 및 IDE 자동 완성을 지원하는 Pandera 스키마.
    변수명은 실제 API 응답 필드명을 그대로 사용합니다.
    """
    year: Series[str]
    statCdCntnKor1: Series[str]
    statCd: Series[str]
    expCnt: Series[int]
    expDlr: Series[float]
    impCnt: Series[int]
    impDlr: Series[float]
    balPayments: Series[float]

    @staticmethod
    def validate_df(data: List[dict]) -> pd.DataFrame:
        """딕셔너리 리스트를 데이터프레임으로 변환하고 스키마 검증"""
        df = pd.DataFrame(data)
        # XML에서 온 데이터는 모든 값이 문자열일 수 있으므로 타입 변환이 필요할 수 있음
        # Pandera Schema는 타입 검증 시 자동 변환을 시도하도록 설정 가능함
        return NationTradeSchema.validate(df)

    class Config:
        strict = True
        coerce = True # 타입 자동 변환 허용 (XML 문자열 -> 숫자 등)

# --- 2. Client Function ---

def get_nation_trade_data(strt_yymm: str, end_yymm: str, cnty_cd: str = "") -> Optional[List[dict]]:
    """
    공공데이터포털 국가별 수출입 현황 API 호출 -> 원본 딕셔너리 리스트 반환
    """
    decoded_key = urllib.parse.unquote(DATA_GO_KR_API_KEY)
    
    params = {
        "serviceKey": decoded_key,
        "strtYymm": strt_yymm,
        "endYymm": end_yymm,
        "cntyCd": cnty_cd
    }

    try:
        response = requests.get(NATION_TRADE_API_URL, params=params)
        data_dict = xmltodict.parse(response.text)
        
        res = data_dict.get('response', {})
        header = res.get('header', {})
        result_code = header.get('resultCode')
        
        if result_code != "00":
            print(f"API Error: {result_code} ({header.get('resultMsg')})")
            return None

        body = res.get('body', {})
        items_wrapper = body.get('items', {})
        
        if not items_wrapper or 'item' not in items_wrapper:
            print("조회된 데이터가 없습니다.")
            return []

        items = items_wrapper['item']
        if isinstance(items, dict):
            items = [items]
            
        return items

    except Exception as e:
        print(f"Request failed: {e}")
    
    return None

# --- 실행 예시 ---
if __name__ == "__main__":
    print("Fetching Nation Trade Data (202301 ~ 202303, US)...")
    data = get_nation_trade_data(strt_yymm="202301", end_yymm="202303", cnty_cd="US")
    
    if data:
        # 스키마를 사용하여 데이터프레임 변환 및 검증
        df = NationTradeSchema.validate_df(data)
        print(f"\n조회 성공 (총 {len(df)}건)")
        
        S = NationTradeSchema
        print(df[[S.year, S.statCdCntnKor1, S.expDlr, S.impDlr]].head())
    else:
        print("데이터를 가져오는 데 실패했습니다.")
