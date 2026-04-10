import os
from dotenv import load_dotenv
from pathlib import Path

# 프로젝트 루트 경로 설정 (.env 파일을 찾기 위함)
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'

# .env 파일 로드
load_dotenv(dotenv_path=env_path)

# 데이터베이스 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'practice_db'),
    'connection_timeout': 10
}

# 서울시 API 설정
SEOUL_API_URL = os.getenv('OPENAPI_SEOUL_URL')

# 공공데이터포털 API 설정
DATA_GO_KR_API_KEY = os.getenv('OPENAPI_DATA_NATION_TRADE_API_KEY')
DATA_GO_KR_URL = os.getenv('OPENAPI_DATA_URL')
NATION_TRADE_API_URL = f"{DATA_GO_KR_URL}{os.getenv('OPENAPI_DATA_NATION_TRADE_PATH')}/getNationtradeList"

# 네이버 API 설정
NAVER_CLIENT_ID = os.getenv('NAVAR_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
NAVER_API_BASE_URL = os.getenv('NAVER_API_URL', 'https://openapi.naver.com/v1')
NAVER_SEARCH_TREND_URL = f"{NAVER_API_BASE_URL}/datalab/search"
