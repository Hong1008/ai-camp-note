from typing import List, Optional
import requests
import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series
from config import SEOUL_API_URL

# --- 1. Pandera Schemas (DataFrame Validation & Column Access) ---

class SubwaySchema(pa.DataFrameModel):
    """지하철 데이터프레임 구조 정의 및 IDE 자동 완성을 지원하는 스키마"""
    USE_YMD: Series[str]
    SBWY_ROUT_LN_NM: Series[str]
    SBWY_STNS_NM: Series[str]
    GTON_TNOPE: Series[int]
    GTOFF_TNOPE: Series[int]
    REG_YMD: Series[str]

    @staticmethod
    def validate_df(data: List[dict]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        return SubwaySchema.validate(df)

    class Config:
        strict = True
        coerce = True

class BikeSchema(pa.DataFrameModel):
    """따릉이 실시간 대여정보 구조 정의 및 IDE 자동 완성을 지원하는 스키마"""
    rackTotCnt: Series[int]
    parkingBikeTotCnt: Series[int]
    shared: Series[int]
    stationLatitude: Series[float]
    stationLongitude: Series[float]
    stationId: Series[str]
    stationName: Series[str]

    @staticmethod
    def validate_df(data: List[dict]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        return BikeSchema.validate(df)

    class Config:
        strict = True
        coerce = True

# --- 2. Client Functions ---

def get_subway_data(use_ymd: str, start_index: int = 1, end_index: int = 5, line_name: str = "", station_name: str = "") -> Optional[List[dict]]:
    """
    서울시 지하철 API 호출 -> 원본 딕셔너리 리스트 반환
    """
    params = [str(start_index), str(end_index), str(use_ymd), line_name, station_name]
    url = "/".join(s for s in [SEOUL_API_URL, "json", "CardSubwayStatsNew"] + params if s)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'CardSubwayStatsNew' in data:
            return data['CardSubwayStatsNew'].get('row', [])
        elif 'RESULT' in data:
            print(f"Subway API Error: {data['RESULT'].get('CODE')} ({data['RESULT'].get('MESSAGE')})")
            
    except Exception as e:
        print(f"Subway Request failed: {e}")
    
    return None

def get_bike_data(start_index: int = 1, end_index: int = 5, station_id: str = "") -> Optional[List[dict]]:
    """
    따릉이 실시간 대여정보 API 호출 -> 원본 딕셔너리 리스트 반환
    """
    params = [str(start_index), str(end_index), station_id]
    url = "/".join(s for s in [SEOUL_API_URL, "json", "bikeList"] + params if s)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'rentBikeStatus' in data:
            return data['rentBikeStatus'].get('row', [])
        elif 'RESULT' in data:
            print(f"Bike API Error: {data['RESULT'].get('CODE')} ({data['RESULT'].get('MESSAGE')})")
            
    except Exception as e:
        print(f"Bike Request failed: {e}")
    
    return None

# --- 실행 예시 ---
if __name__ == "__main__":
    # 1. 지하철 데이터 테스트
    print("--- Testing Subway API ---")
    subway_data = get_subway_data(use_ymd="20260405", line_name="2호선")
    if subway_data:
        subway_df = SubwaySchema.validate_df(subway_data)
        print(f"Subway Success (Rows: {len(subway_df)})")
        print(subway_df[[SubwaySchema.SBWY_STNS_NM, SubwaySchema.GTON_TNOPE]].head())

    # 2. 따릉이 데이터 테스트
    print("\n--- Testing Bike API ---")
    bike_data = get_bike_data(start_index=1, end_index=5)
    if bike_data:
        bike_df = BikeSchema.validate_df(bike_data)
        print(f"Bike Success (Rows: {len(bike_df)})")
        print(bike_df[[BikeSchema.stationName, BikeSchema.parkingBikeTotCnt]].head())
