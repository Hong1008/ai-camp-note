import json
import logging
import os
import sys
import time
from pathlib import Path
import requests
import numpy as np
from datetime import datetime, timedelta

# 프로젝트 루트를 Python path에 추가하여 config를 가져올 수 있도록 함
sys.path.append(str(Path(__file__).resolve().parents[2]))
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class TossClient:
    """토스증권 Open API (v1.1.5) 시세 및 종목 정보 조회용 클라이언트 클래스.
    OAuth2 토큰을 로컬 JSON 파일에 캐싱하고 만료 시 자동 갱신합니다.
    API 키가 없거나 호출 실패 시 고충실도 시뮬레이션(Mock) 데이터를 반환합니다.
    """
    
    BASE_URL = "https://openapi.tossinvest.com"
    TOKEN_CACHE_FILE = Path(__file__).resolve().parent / ".toss_token.json"

    def __init__(self, api_key: str = None, secret_key: str = None):
        self.api_key = api_key or config.TOSS_API_KEY
        self.secret_key = secret_key or config.TOSS_SECRET_KEY
        
        self.is_mock = False
        if not self.api_key or not self.secret_key or self.api_key == "mock_key":
            logger.warning("TOSS_API_KEY 또는 TOSS_SECRET_KEY가 설정되지 않아 시뮬레이션(MOCK) 모드로 작동합니다.")
            self.is_mock = True
            
        self._access_token = None
        self._token_expires_at = 0

    def _get_headers(self) -> dict:
        """API 요청에 사용할 공통 인증 헤더를 반환합니다."""
        token = self.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def get_access_token(self) -> str:
        """캐싱된 토큰이 유효하면 반환하고, 만료되었거나 없을 경우 신규 발급합니다."""
        if self.is_mock:
            return "mock_simulated_token_12345"
            
        now = time.time()
        
        # 1. 메모리 캐시 확인 (만료 시간 1분 버퍼 적용)
        if self._access_token and self._token_expires_at > now + 60:
            return self._access_token

        # 2. 로컬 파일 캐시 확인
        if self.TOKEN_CACHE_FILE.exists():
            try:
                with open(self.TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
                    cache = json.load(f)
                    
                cached_token = cache.get("access_token")
                expires_at = cache.get("expires_at", 0)
                
                if cached_token and expires_at > now + 60:
                    self._access_token = cached_token
                    self._token_expires_at = expires_at
                    logger.info("로컬 캐시에서 토큰을 로드했습니다.")
                    return self._access_token
            except Exception as e:
                logger.warning(f"로컬 토큰 캐시 파일 읽기 실패: {e}")

        # 3. 토큰 신규 발급
        try:
            logger.info("만료되었거나 유효한 토큰 캐시가 없어 신규 토큰을 요청합니다.")
            token_data = self._request_new_token()
            
            self._access_token = token_data["access_token"]
            self._token_expires_at = now + token_data["expires_in"]
            
            # 신규 발급 토큰 파일 캐싱
            try:
                with open(self.TOKEN_CACHE_FILE, "w", encoding="utf-8") as f:
                    json.dump({
                        "access_token": self._access_token,
                        "expires_at": self._token_expires_at
                    }, f)
                logger.info("신규 토큰을 로컬 캐시 파일에 저장했습니다.")
            except Exception as e:
                logger.warning(f"로컬 토큰 캐시 파일 쓰기 실패: {e}")
                
            return self._access_token
        except Exception as e:
            logger.error(f"실제 토큰 발급 실패. 시뮬레이션 모드로 전환합니다. 에러: {e}")
            self.is_mock = True
            return "mock_simulated_token_12345"

    def _request_new_token(self) -> dict:
        """토스증권 OAuth2 토큰 발급 API를 호출합니다."""
        url = f"{self.BASE_URL}/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            logger.error(f"토큰 발급 실패 (HTTP {response.status_code}): {response.text}")
            response.raise_for_status()
            
        token_res = response.json()
        return {
            "access_token": token_res["access_token"],
            "expires_in": token_res["expires_in"]
        }

    def _handle_response(self, response: requests.Response) -> dict:
        """API 응답 Envelope 규격에 맞춰 성공/실패를 분석하고 실제 결과(result) 데이터를 반환합니다."""
        try:
            res_json = response.json()
        except ValueError:
            logger.error(f"JSON 파싱 실패 (HTTP {response.status_code}): {response.text}")
            response.raise_for_status()

        if response.status_code == 200:
            if "result" in res_json:
                return res_json["result"]
            return res_json
        else:
            error_info = res_json.get("error", {})
            err_code = error_info.get("code", "unknown-error")
            err_msg = error_info.get("message", "알 수 없는 오류가 발생했습니다.")
            req_id = error_info.get("requestId", "N/A")
            
            logger.error(f"API 호출 오류 [Code: {err_code}, Msg: {err_msg}, RequestId: {req_id}]")
            raise requests.HTTPError(
                f"Toss API Error: {err_msg} (Code: {err_code}, RequestId: {req_id})",
                response=response
            )

    def get_prices(self, symbols: list[str]) -> list[dict]:
        """지정된 종목들의 현재가 정보를 조회합니다."""
        if self.is_mock:
            return self._get_mock_prices(symbols)
            
        try:
            url = f"{self.BASE_URL}/api/v1/prices"
            headers = self._get_headers()
            params = {
                "symbols": ",".join(symbols)
            }
            response = requests.get(url, headers=headers, params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.warning(f"실제 현재가 조회 실패. 시뮬레이션 데이터를 반환합니다. 에러: {e}")
            return self._get_mock_prices(symbols)

    def get_candles(self, symbol: str, interval: str = "1d", count: int = 100, before: str = None) -> dict:
        """종목의 캔들(OHLCV) 데이터를 조회합니다. (최대 200개 봉)"""
        if self.is_mock:
            return self._get_mock_candles(symbol, interval, count)
            
        try:
            url = f"{self.BASE_URL}/api/v1/candles"
            headers = self._get_headers()
            params = {
                "symbol": symbol,
                "interval": interval,
                "count": min(count, 200),
                "adjusted": "true"
            }
            if before:
                params["before"] = before
                
            response = requests.get(url, headers=headers, params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.warning(f"실제 캔들 데이터 조회 실패. 시뮬레이션 데이터를 반환합니다. 에러: {e}")
            return self._get_mock_candles(symbol, interval, count)

    def get_orderbook(self, symbol: str) -> dict:
        """종목의 매수/매도 호가 잔량을 조회합니다."""
        if self.is_mock:
            return self._get_mock_orderbook(symbol)
            
        try:
            url = f"{self.BASE_URL}/api/v1/orderbook"
            headers = self._get_headers()
            params = {
                "symbol": symbol
            }
            response = requests.get(url, headers=headers, params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.warning(f"실제 호가 조회 실패. 시뮬레이션 데이터를 반환합니다. 에러: {e}")
            return self._get_mock_orderbook(symbol)

    def get_warnings(self, symbol: str) -> list[dict]:
        """종목의 매수 유의사항 및 VI 발동 정보 등을 조회합니다."""
        if self.is_mock:
            return self._get_mock_warnings(symbol)
            
        try:
            url = f"{self.BASE_URL}/api/v1/stocks/{symbol}/warnings"
            headers = self._get_headers()
            response = requests.get(url, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            logger.warning(f"실제 경고 정보 조회 실패. 시뮬레이션 데이터를 반환합니다. 에러: {e}")
            return self._get_mock_warnings(symbol)

    # --- MOCK DATA GENERATION METHODS ---

    def _get_mock_prices(self, symbols: list[str]) -> list[dict]:
        """시뮬레이션 현재가 생성"""
        results = []
        now_str = datetime.now().isoformat()
        for symbol in symbols:
            if symbol == "005930":  # 삼성전자
                price = "73500"
            elif symbol == "000660":  # SK하이닉스
                price = "181200"
            else:
                price = "50000"
                
            results.append({
                "symbol": symbol,
                "timestamp": now_str,
                "lastPrice": price,
                "currency": "KRW"
            })
        return results

    def _get_mock_candles(self, symbol: str, interval: str, count: int) -> dict:
        """시뮬레이션 캔들 데이터 생성 (정확한 기술적 분석 테스트용 시계열 생성)"""
        # 삼성전자: 70,000~75,000원 횡보/소폭 상승 트렌드
        # SK하이닉스: 160,000~195,000원 변동성이 높은 강한 상승 트렌드
        np.random.seed(hash(symbol) % 1234567)
        
        base_price = 72000.0 if symbol == "005930" else 170000.0
        drift = 0.0002 if symbol == "005930" else 0.0015
        volatility = 0.012 if symbol == "005930" else 0.025
        
        candles = []
        current_time = datetime.now()
        price = base_price
        
        # 이전 200일 치 시뮬레이션 가격 계산 후, 뒤집어 저장 (최신 것부터 앞으로 가도록)
        # 1. 먼저 순차적으로 과거 시점부터 현재 시점까지 주가 경로를 생성
        prices_path = []
        for i in range(count):
            change = np.random.normal(drift, volatility)
            price = price * (1 + change)
            prices_path.append(price)
            
        # 2. 캔들 구조 생성 (인덱스 역순으로 생성하여 최신 데이터가 앞에 오게 함)
        for i in range(count):
            price_idx = count - 1 - i
            close_price = int(prices_path[price_idx])
            
            # Open, High, Low 생성
            open_change = np.random.normal(0, 0.003)
            open_price = int(close_price * (1 + open_change))
            
            high_price = int(max(open_price, close_price) * (1 + abs(np.random.normal(0, 0.005))))
            low_price = int(min(open_price, close_price) * (1 - abs(np.random.normal(0, 0.005))))
            volume = int(np.random.exponential(5000000 if symbol == "005930" else 2000000))
            
            # 일봉 또는 분봉 날짜 차감
            if interval == "1d":
                candle_time = current_time - timedelta(days=i)
            else:
                candle_time = current_time - timedelta(minutes=i)
                
            candles.append({
                "timestamp": candle_time.isoformat(),
                "openPrice": str(open_price),
                "highPrice": str(high_price),
                "lowPrice": str(low_price),
                "closePrice": str(close_price),
                "volume": str(volume),
                "currency": "KRW"
            })
            
        return {
            "candles": candles,
            "nextBefore": candles[-1]["timestamp"] if candles else None
        }

    def _get_mock_orderbook(self, symbol: str) -> dict:
        """시뮬레이션 호가 생성"""
        now_str = datetime.now().isoformat()
        base_price = 73500 if symbol == "005930" else 181200
        tick = 100 if symbol == "005930" else 500
        
        asks = []
        bids = []
        
        # 호가 3단계 생성 (매도/매수 잔량 불균형 시뮬레이션)
        # 매도 호가 (asks)
        for i in range(1, 4):
            price = base_price + (i * tick)
            vol = 5000 + i * 2300 if symbol == "005930" else 800 + i * 150
            asks.append({
                "price": str(price),
                "volume": str(vol)
            })
            
        # 매수 호가 (bids)
        for i in range(0, 3):
            price = base_price - (i * tick)
            vol = 4500 + i * 1500 if symbol == "005930" else 900 + i * 200
            bids.append({
                "price": str(price),
                "volume": str(vol)
            })
            
        return {
            "timestamp": now_str,
            "currency": "KRW",
            "asks": asks,
            "bids": bids
        }

    def _get_mock_warnings(self, symbol: str) -> list[dict]:
        """시뮬레이션 경고 정보 생성"""
        # 삼성전자는 투자주의 없음, SK하이닉스는 최근 단기과열 상태로 시뮬레이션
        if symbol == "005930":
            return []
        else:
            return [
                {
                    "warningType": "OVERHEATED",
                    "exchange": "KRX",
                    "startDate": "2026-06-20",
                    "endDate": "2026-06-27"
                }
            ]
