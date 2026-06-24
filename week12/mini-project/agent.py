import json
import os
import sys
from pathlib import Path
from typing import List
import pandas as pd
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# 프로젝트 루트 및 mini-project 폴더를 Python path에 추가
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import config
# pyrefly: ignore [missing-import]
from toss_client import TossClient

# Toss SDK 클라이언트 초기화
toss_client = TossClient()

# --- PYDANTIC SCHEMAS FOR STRUCTURED STRATEGY OUTPUT ---
class StockSummary(BaseModel):
    symbol: str = Field(description="종목 코드")
    name: str = Field(description="종목명")
    price: str = Field(description="현재가 (예: '1,959,000원')")
    ma5: str = Field(description="5일 이동평균 (예: '2,123,600원')")
    ma20: str = Field(description="20일 이동평균 (예: '1,927,050원')")
    rsi: str = Field(description="RSI (14일) 값 (예: '57.39')")
    orderbook_ratio: str = Field(description="호가 불균형 비율 (예: '0.30')")
    sentiment: str = Field(description="수급 심리 상태 (예: 'BUY_SUPPORT')")
    warning_status: str = Field(description="투자 경고 상태 (예: '특이사항 없음')")

class StrategyReport(BaseModel):
    title: str = Field(description="보고서 제목 (예: '반도체/IT 대표 2사 투자 전략 보고서')")
    date: str = Field(description="작성일자 (예: '2026년 06월 24일')")
    summary_table: List[StockSummary] = Field(description="두 종목의 핵심 시세 요약 데이터 리스트 (총 2개 원소)")
    technical_analysis: str = Field(description="기술적 지표 분석 결과 (RSI 및 이동평균선 추세)")
    supply_demand_analysis: str = Field(description="수급 강도 및 투자 심리 분석 결과")
    top_pick_short: str = Field(description="단기(1~2주) 관점 최선호주 및 근거")
    top_pick_mid: str = Field(description="중기(1개월) 관점 최선호주 및 근거")
    top_pick_selection: str = Field(description="종합 최선호주 (Top Pick) 종목명")
    strategy_a: str = Field(description="첫 번째 종목 대응 전략 및 리스크 요인")
    strategy_b: str = Field(description="두 번째 종목 대응 전략 및 리스크 요인")

# --- CUSTOM TOOLS DEFINITION ---

@tool("GetTechnicalIndicators")
def get_technical_indicators(symbol: str, interval: str = "1d", count: int = 50) -> str:
    """지정된 종목(예: 삼성전자 '005930', SK하이닉스 '000660')의 캔들 데이터를 조회하고, 
    Pandas를 사용하여 MA5, MA20 이동평균선과 RSI(14) 값을 계산하여 분석용 JSON 데이터로 반환합니다.
    """
    try:
        res = toss_client.get_candles(symbol, interval=interval, count=count)
        candles_data = res.get("candles", [])
        if not candles_data:
            return json.dumps({"error": f"종목 {symbol}에 대한 캔들 데이터가 없습니다."}, ensure_ascii=False)
            
        df = pd.DataFrame(candles_data)
        # 데이터 타입 변환
        df["close"] = df["closePrice"].astype(float)
        df["open"] = df["openPrice"].astype(float)
        df["high"] = df["highPrice"].astype(float)
        df["low"] = df["lowPrice"].astype(float)
        df["volume"] = df["volume"].astype(float)
        
        # 최신 순에서 과거 순으로 정렬되어 있으므로 뒤집음 (과거 -> 최신)
        df = df.iloc[::-1].reset_index(drop=True)
        
        # 이동평균선 계산
        df["ma5"] = df["close"].rolling(5).mean()
        df["ma20"] = df["close"].rolling(20).mean()
        
        # RSI(14) 계산
        delta = df["close"].diff()
        up = delta.clip(lower=0)
        down = -delta.clip(upper=0)
        ema_up = up.ewm(com=13, adjust=False).mean()
        ema_down = down.ewm(com=13, adjust=False).mean()
        rs = ema_up / (ema_down + 1e-10)
        df["rsi"] = 100 - (100 / (1 + rs))
        
        # 최근 3개 캔들의 분석 결과를 직관적으로 반환
        recent_df = df.tail(3)
        results = []
        for _, row in recent_df.iterrows():
            results.append({
                "timestamp": row["timestamp"].split("T")[0] if "T" in row["timestamp"] else row["timestamp"],
                "close": int(row["close"]),
                "open": int(row["open"]),
                "high": int(row["high"]),
                "low": int(row["low"]),
                "volume": int(row["volume"]),
                "ma5": round(row["ma5"], 2) if not pd.isna(row["ma5"]) else None,
                "ma20": round(row["ma20"], 2) if not pd.isna(row["ma20"]) else None,
                "rsi": round(row["rsi"], 2) if not pd.isna(row["rsi"]) else None,
            })
            
        # 최신 상태 기반 크로스오버 체크
        latest = results[-1]
        prev = results[-2] if len(results) > 1 else None
        
        trend = "UP (Bullish)" if latest["ma5"] and latest["ma20"] and latest["ma5"] > latest["ma20"] else "DOWN (Bearish)"
        crossover = "NONE"
        if prev and prev["ma5"] and prev["ma20"] and latest["ma5"] and latest["ma20"]:
            if prev["ma5"] <= prev["ma20"] and latest["ma5"] > latest["ma20"]:
                crossover = "GOLDEN_CROSS"
            elif prev["ma5"] >= prev["ma20"] and latest["ma5"] < latest["ma20"]:
                crossover = "DEAD_CROSS"
                
        # 10대 반도체 종목 한글명 매핑
        KOSPI_NAMES = {
            "005930": "삼성전자",
            "000660": "SK하이닉스",
            "009150": "삼성전기",
            "006400": "삼성SDI",
            "042700": "한미반도체",
            "036930": "주성엔지니어링",
            "007660": "이수페타시스",
            "240810": "원익IPS",
            "353200": "대덕전자",
            "000990": "DB하이텍"
        }
        
        summary = {
            "symbol": symbol,
            "name": KOSPI_NAMES.get(symbol, "기타"),
            "trend": trend,
            "crossover": crossover,
            "latest_price": latest["close"],
            "latest_rsi": latest["rsi"],
            "latest_ma5": latest["ma5"],
            "latest_ma20": latest["ma20"],
            "recent_candles": results
        }
        return json.dumps(summary, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"기술적 지표 계산 중 오류 발생: {str(e)}"}, ensure_ascii=False)

@tool("GetMarketOrderbook")
def get_market_orderbook(symbol: str) -> str:
    """지정된 종목의 실시간 매수/매도 호가 잔량을 조회하고, 
    매수 잔량 대비 매도 잔량 비율(호가 불균형 비율) 등을 계산하여 수급 상황 데이터를 반환합니다.
    """
    try:
        res = toss_client.get_orderbook(symbol)
        asks = res.get("asks", [])
        bids = res.get("bids", [])
        
        total_ask_vol = sum(int(ask["volume"]) for ask in asks)
        total_bid_vol = sum(int(bid["volume"]) for bid in bids)
        ratio = round(total_ask_vol / total_bid_vol, 4) if total_bid_vol > 0 else 0
        
        # 호가 불균형 기반 단기 수급 강도 해석
        sentiment = "SELL_PRESSURE (매도 잔량 우위)" if ratio > 1.2 else ("BUY_SUPPORT (매수 잔량 우위)" if ratio < 0.8 else "NEUTRAL")
        
        summary = {
            "symbol": symbol,
            "top_ask_price": int(asks[0]["price"]) if asks else None,
            "top_bid_price": int(bids[0]["price"]) if bids else None,
            "total_ask_volume": total_ask_vol,
            "total_bid_volume": total_bid_vol,
            "ask_to_bid_ratio": ratio,
            "orderbook_sentiment": sentiment
        }
        return json.dumps(summary, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"호가 잔량 분석 중 오류 발생: {str(e)}"}, ensure_ascii=False)

@tool("GetStockWarningStatus")
def get_stock_warning_status(symbol: str) -> str:
    """지정된 종목의 투자 유의 정보 및 VI 발동 여부를 조회합니다."""
    try:
        res = toss_client.get_warnings(symbol)
        return json.dumps(res, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"투자 유의 정보 조회 중 오류 발생: {str(e)}"}, ensure_ascii=False)

# --- CREWAI AGENTS AND TASKS SETUP ---

def run_crew_analysis(symbol_a: str = "005930", name_a: str = "삼성전자", symbol_b: str = "000660", name_b: str = "SK하이닉스") -> str:
    """두 종목을 비교 분석하는 CrewAI 워크플로우를 실행하고 마크다운 보고서를 반환합니다."""
    
    # 1. LLM 초기화
    if config.GOOGLE_AI_API_KEY:
        # Gemini LLM 설정 (Fallback)
        llm = LLM(
            model="gemini/gemini-3.1-flash-lite",
            temperature=0.3,
            api_key=config.GOOGLE_AI_API_KEY
        )
    elif config.OPENAI_API_KEY:
        # OpenAI LLM 설정
        llm = LLM(
            model="openai/gpt-4o-mini",
            temperature=0.3,
            api_key=config.OPENAI_API_KEY
        )
    else:
        # Default LLM
        llm = LLM(
            model="gpt-4o-mini",
            temperature=0.3
        )

    # 2. 에이전트 정의
    market_data_specialist = Agent(
        role="시세 데이터 분석 전문가",
        goal="대상 종목의 시세 캔들 정보, 호가 잔량, 경고 사항을 수집하고 연산하여 현재 시장에서의 기술적/수급 상태를 파악합니다.",
        backstory=(
            "토스증권 API와 Pandas 분석 라이브러리를 자유자재로 사용하여 종목의 이동평균선 크로스, RSI 과매수/과매도 여부, "
            "호가 불균형 비율 등 시장의 즉각적인 수급 상태를 수집하고 정량적 분석 데이터를 제공합니다."
        ),
        llm=llm,
        tools=[get_technical_indicators, get_market_orderbook, get_stock_warning_status],
        verbose=True
    )

    investment_strategist = Agent(
        role="반도체 섹터 투자 전략 수석 분석가",
        goal="시세 분석가가 수집한 기술적 데이터와 시장 추세를 비교하여 두 종목 중 단기/중기 투자 관점에서 더 매력적인 종목을 평가하고 투자 전략 보고서를 작성합니다.",
        backstory=(
            "수년간 반도체 섹터의 시장 트렌드와 차트 기술적 흐름을 분석해 온 전문가입니다. "
            "복잡한 차트 정보를 결합하여 어떤 종목이 현재 시장 대비 강세를 보이는지 비교 설명하고 최적의 진입 시점과 전략을 명확하게 도출하는 리포트를 작성합니다."
        ),
        llm=llm,
        verbose=True
    )

    # 3. 태스크 정의
    collect_data_task = Task(
        description=(
            f"{name_a}(단축코드: {symbol_a})와 {name_b}(단축코드: {symbol_b})의 최근 일봉 캔들 기술적 지표(MA5, MA20, RSI), 호가 정보, 투자 경고 상태를 수집하고 요약하세요.\n"
            f"**주의**: 각 종목의 올바른 코드를 반드시 사용하십시오. {name_a}는 '{symbol_a}', {name_b}는 '{symbol_b}'입니다. 절대 다른 코드를 사용하지 마십시오.\n"
            f"각 종목에 대해 제공된 도구들(GetTechnicalIndicators, GetMarketOrderbook, GetStockWarningStatus)을 모두 호출하여 분석용 원본 데이터를 얻어야 합니다. "
            f"도구 호출 시 {name_a}는 '{symbol_a}', {name_b}는 '{symbol_b}'를 인자값으로 명확히 지정하여 전달하십시오.\n"
            "수집한 지표들을 분석하여 두 종목의 가격 및 거래량 상태를 대조할 수 있는 정돈된 형태의 요약 리포트를 구성하십시오."
        ),
        expected_output=f"두 종목({name_a}, {name_b})의 시세 정보, 기술적 지표(MA5, MA20, RSI), 호가 불균형 비율, 경고 상태를 포함하는 정돈된 데이터 셋트와 요약 설명",
        agent=market_data_specialist
    )

    from datetime import datetime
    current_date = datetime.now().strftime("%Y년 %m월 %d일")

    generate_strategy_task = Task(
        description=(
            f"시세 데이터 분석가가 수집한 결과 데이터를 토대로 {name_a}({symbol_a})와 {name_b}({symbol_b}) 두 종목을 비교 분석하여 StrategyReport 스키마에 맞춤형 데이터를 작성해 한국어로 채워 넣으세요.\n"
            f"보고서 상단에 **작성일:** {current_date}를 반드시 기재해야 하며, 다른 년도나 날짜(예: 2024년)를 사용하면 절대 안 됩니다.\n"
            f"{name_a}의 종목코드는 반드시 '{symbol_a}'로, {name_b}의 종목코드는 반드시 '{symbol_b}'로 표기하십시오.\n\n"
            "**수치 데이터 바인딩 규칙 (필수)**:\n"
            "- 보고서에 들어가는 모든 현재가, MA5, MA20, RSI, 호가 불균형 비율, 호가 심리 및 투자 경고 상태는 시세 분석가가 도구(GetTechnicalIndicators, GetMarketOrderbook, GetStockWarningStatus)를 실행하여 반환한 실제 값과 100% 일치해야 합니다.\n"
            "- 임의로 가상의 수치를 지어내거나 환각(Hallucination)을 일으켜 값을 작성해서는 절대 안 됩니다. 도구 결과값의 수치를 그대로 바인딩하십시오.\n\n"
            "수식 계산은 에이전트가 추정하지 말고 도구의 결과값을 전적으로 준수해야 합니다."
        ),
        expected_output="StrategyReport 구조화된 Pydantic 모델 인스턴스 데이터",
        agent=investment_strategist,
        context=[collect_data_task],
        output_pydantic=StrategyReport
    )

    # 4. 크루 설정 및 실행
    crew = Crew(
        agents=[market_data_specialist, investment_strategist],
        tasks=[collect_data_task, generate_strategy_task],
        process=Process.sequential,
        verbose=True
    )
    
    # 5. 실행 결과 킥오프
    result = crew.kickoff()
    
    # Pydantic 결과 리턴 (구조화된 출력이 확보되지 않은 경우 예외 발생)
    if hasattr(result, "pydantic") and result.pydantic:
        if hasattr(result.pydantic, "model_dump_json"):
            return result.pydantic.model_dump_json()
        return result.pydantic.json()
    elif hasattr(result, "json_dict") and result.json_dict:
        return json.dumps(result.json_dict, ensure_ascii=False)
    
    # 결과 문자열이 JSON 형식인지 검증
    try:
        raw_str = str(result)
        parsed = json.loads(raw_str)
        if isinstance(parsed, dict):
            return raw_str
        elif isinstance(parsed, list):
            raise TypeError(f"CrewAI 결과가 dict가 아닌 list 형식입니다: {parsed}")
    except json.JSONDecodeError:
        pass
        
    raise ValueError(f"CrewAI가 구조화된 데이터(StrategyReport)를 생성하지 못했습니다. 결과: {result}")

if __name__ == "__main__":
    # 로컬 실행 테스트용
    print("AI 에이전트 분석 테스트 시작...")
    report = run_crew_analysis()
    print("\n================== 생성된 보고서 ==================\n")
    print(report)
