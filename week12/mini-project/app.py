import os
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 프로젝트 루트 및 mini-project 폴더를 Python path에 추가
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parents[2]))

import config
# pyrefly: ignore [missing-import]
from toss_client import TossClient
# pyrefly: ignore [missing-import]
from agent import run_crew_analysis

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="반도체 대표 2사 AI 투자 전략 분석실",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Toss Client 초기화
toss_client = TossClient()

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.markdown("### 🛠️ Control Panel")

# 1. API 접속 모드 확인
if toss_client.is_mock:
    st.sidebar.warning("⚠️ 시뮬레이션 모드 작동 중\n(API 키가 없거나 올바르지 않아 모의 시세 데이터가 출력됩니다.)")
else:
    st.sidebar.success("🔑 실시간 토스증권 API 연결 성공")

# 환경 변수 체크
st.sidebar.markdown("#### API 상태 체크")
env_check = {
    "TOSS_API_KEY": config.TOSS_API_KEY is not None,
    "TOSS_SECRET_KEY": config.TOSS_SECRET_KEY is not None,
    "OPENAI_API_KEY": config.OPENAI_API_KEY is not None,
    "GOOGLE_AI_API_KEY": config.GOOGLE_AI_API_KEY is not None,
}

for name, loaded in env_check.items():
    status_icon = "✅" if loaded else "❌"
    st.sidebar.text(f"{status_icon} {name}")

# --- MAIN PAGE HEADER ---
st.html('<div class="main-header">반도체 대표 10사 AI 투자 전략 분석실</div>')
st.html('<div class="sub-header">토스증권 실시간/시뮬레이션 시세 정보와 CrewAI 에이전트 협업 기반의 기술적/수급 비교 분석</div>')

# 10대 반도체 종목 매핑 (이름, 코드, 설명)
SEMICON_STOCKS = {
    "삼성전자 (005930)": ("005930", "삼성전자", "DRAM, NAND Flash, 모바일 AP"),
    "SK하이닉스 (000660)": ("000660", "SK하이닉스", "DRAM, NAND Flash, CIS"),
    "삼성전기 (009150)": ("009150", "삼성전기", "반도체 패키지 기판 (FC-BGA 등)"),
    "삼성SDI (006400)": ("006400", "삼성SDI", "반도체 공정 소재 (EMC, CMP 슬러리 등)"),
    "한미반도체 (042700)": ("042700", "한미반도체", "반도체 패키징 및 후공정 검사 장비 (HBM 필수 장비)"),
    "주성엔지니어링 (036930)": ("036930", "주성엔지니어링", "반도체 증착 장비 (ALD 등)"),
    "이수페타시스 (007660)": ("007660", "이수페타시스", "초고다층 PCB (AI 가속기용 기판)"),
    "원익IPS (240810)": ("240810", "원익IPS", "반도체 증착 및 열처리 장비"),
    "대덕전자 (353200)": ("353200", "대덕전자", "반도체용 패키지 기판 (PCB)"),
    "DB하이텍 (000990)": ("000990", "DB하이텍", "시스템 반도체 및 파운드리")
}

# --- STOCK SELECTION ---
st.markdown("### 🔍 분석 종목 선택")
stock_options = list(SEMICON_STOCKS.keys())

col_sel1, col_sel2 = st.columns(2)
with col_sel1:
    selected_key_a = st.selectbox("첫 번째 분석 종목", stock_options, index=0)
    symbol_a, name_a, desc_a = SEMICON_STOCKS[selected_key_a]
    st.caption(f"**설명**: {desc_a}")

with col_sel2:
    remaining_options = [opt for opt in stock_options if SEMICON_STOCKS[opt][0] != symbol_a]
    selected_key_b = st.selectbox("두 번째 분석 종목", remaining_options, index=0)
    symbol_b, name_b, desc_b = SEMICON_STOCKS[selected_key_b]
    st.caption(f"**설명**: {desc_b}")

# --- HELPER FUNCTIONS ---
def parse_warning_list(warn_list: list) -> tuple[str, bool]:
    """경고 목록을 분석하여 표시 수준과 단기과열 여부를 반환합니다."""
    if not isinstance(warn_list, list) or not warn_list:
        return "NONE", False
        
    has_warning = any(w.get("warningType") in ["INVESTMENT_WARNING", "INVESTMENT_RISK"] for w in warn_list)
    has_overheat = any(w.get("warningType") == "OVERHEATED" for w in warn_list)
    has_vi = any(w.get("warningType") in ["VI_STATIC", "VI_DYNAMIC", "VI_STATIC_AND_DYNAMIC"] for w in warn_list)
    has_liq = any(w.get("warningType") == "LIQUIDATION_TRADING" for w in warn_list)
    
    if has_liq:
        return "정리매매", has_overheat
    elif has_warning:
        return "투자경고/위험", has_overheat
    elif has_vi:
        return "VI 발동", has_overheat
    elif has_overheat:
        return "단기과열", has_overheat
    return "NONE", False

def draw_candlestick_chart(symbol, title):
    """지정된 종목의 50일 일봉 캔들 차트를 그립니다."""
    res = toss_client.get_candles(symbol, "1d", 50)
    candles = res.get("candles", [])
    if not candles:
        st.info(f"{title} 캔들 데이터가 없습니다.")
        return None
        
    df = pd.DataFrame(candles)
    df = df.iloc[::-1].reset_index(drop=True)
    df["close"] = df["closePrice"].astype(float)
    df["open"] = df["openPrice"].astype(float)
    df["high"] = df["highPrice"].astype(float)
    df["low"] = df["lowPrice"].astype(float)
    df["date"] = df["timestamp"].apply(lambda x: x.split("T")[0] if "T" in x else x)
    
    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='#ef4444',
        decreasing_line_color='#1d4ed8'
    )])
    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
        height=380
    )
    return fig

# --- TABS FOR STOCK ANALYSIS ---
st.markdown("### 📊 개별 종목 분석")
tab1, tab2 = st.tabs([f"📊 {name_a} ({symbol_a})", f"📊 {name_b} ({symbol_b})"])

with tab1:
    col_t1_1, col_t1_2 = st.columns([1, 2])
    with col_t1_1:
        st.html('<div class="metric-card">')
        st.html(f'<div class="metric-title">{name_a} 현재가</div>')
        try:
            p_a = toss_client.get_prices([symbol_a])[0]
            price_val = int(p_a["lastPrice"])
            st.html(f'<div class="metric-value">{price_val:,} KRW</div>')
        except Exception:
            st.html('<div class="metric-value">조회 실패</div>')
            
        warn_a_list = toss_client.get_warnings(symbol_a)
        warn_level_a, short_overheat_a = parse_warning_list(warn_a_list)
        if warn_level_a == "NONE" and not short_overheat_a:
            st.html('<div class="warning-card warning-normal">정상 거래 가능 (주의 없음)</div>')
        else:
            overheat_str_a = " / 단기과열" if short_overheat_a and warn_level_a != "단기과열" else ""
            st.html(f'<div class="warning-card warning-caution">유의: {warn_level_a}{overheat_str_a}</div>')
        st.html('</div>')
        
    with col_t1_2:
        fig_a = draw_candlestick_chart(symbol_a, f"{name_a} 최근 50일 일봉")
        if fig_a:
            st.plotly_chart(fig_a, use_container_width=True)

with tab2:
    col_t2_1, col_t2_2 = st.columns([1, 2])
    with col_t2_1:
        st.html('<div class="metric-card">')
        st.html(f'<div class="metric-title">{name_b} 현재가</div>')
        try:
            p_b = toss_client.get_prices([symbol_b])[0]
            price_val_b = int(p_b["lastPrice"])
            st.html(f'<div class="metric-value">{price_val_b:,} KRW</div>')
        except Exception:
            st.html('<div class="metric-value">조회 실패</div>')
            
        warn_b_list = toss_client.get_warnings(symbol_b)
        warn_level_b, short_overheat_b = parse_warning_list(warn_b_list)
        if warn_level_b == "NONE" and not short_overheat_b:
            st.html('<div class="warning-card warning-normal">정상 거래 가능 (주의 없음)</div>')
        else:
            overheat_str_b = " / 단기과열" if short_overheat_b and warn_level_b != "단기과열" else ""
            st.html(f'<div class="warning-card warning-caution">유의: {warn_level_b}{overheat_str_b}</div>')
        st.html('</div>')
        
    with col_t2_2:
        fig_b = draw_candlestick_chart(symbol_b, f"{name_b} 최근 50일 일봉")
        if fig_b:
            st.plotly_chart(fig_b, use_container_width=True)

st.markdown("---")

# 4. CrewAI 에이전트 실행 및 보고서 섹션
st.markdown("---")
st.markdown("### 🤖 AI 에이전트 협업 분석 결과")

# Sidebar에 분석 실행 버튼 제공
run_button = st.sidebar.button("🚀 AI 비교 분석 시작", use_container_width=True)

if run_button:
    with st.spinner(f"🕵️ 시세 데이터 분석가와 투자 전략 분석가가 협업하여 {name_a}와 {name_b}의 리포트를 작성하는 중입니다... (약 20~40초 소요)"):
        try:
            report_content = run_crew_analysis(symbol_a, name_a, symbol_b, name_b)
            
            # 생성된 리포트 세션 캐시에 저장 (로컬 파일 쓰기는 보안/정합성을 위해 제거됨)
            st.session_state["last_report"] = report_content
            st.success("✅ AI 분석 리포트 생성이 완료되었습니다!")
        except Exception as e:
            st.error(f"❌ 분석 도중 오류가 발생했습니다: {e}")

# 리포트 렌더링 섹션
if "last_report" in st.session_state:
    raw_content = st.session_state["last_report"]
    # JSON 형식으로 파싱하여 구조적 레이아웃으로 출력
    import json
    report_data = json.loads(raw_content)
    if not isinstance(report_data, dict):
        raise TypeError(f"AI 분석 결과가 올바른 딕셔너리 구조가 아닙니다. 실제 타입: {type(report_data)}, 데이터: {report_data}")
    
    st.subheader(f"📄 {report_data.get('title', '반도체/IT 대표 종목 투자 전략 보고서')}")
    st.caption(f"📅 분석 기준 및 작성일자: {report_data.get('date', '')}")
    
    # 1. 핵심 시세 요약 대조 카드
    st.markdown("#### 📊 1. 핵심 시세 요약")
    summaries = report_data.get("summary_table", [])
    if len(summaries) >= 2:
        sum_col1, sum_col2 = st.columns(2)
        for i, col in enumerate([sum_col1, sum_col2]):
            stock = summaries[i]
            with col:
                st.html(f"""
                <div class="metric-card" style="margin-bottom: 15px;">
                    <div style="font-weight: 800; font-size: 1.3rem; color: #00C9FF; margin-bottom: 10px;">
                        {stock.get('name')} ({stock.get('symbol')})
                    </div>
                    <table style="width: 100%; border-collapse: collapse; border: none;">
                        <tr style="border-bottom: 1px solid #374151;"><td style="padding: 6px 0; color: #9ca3af; border: none;">현재가</td><td style="text-align: right; font-weight: 700; ; border: none;">{stock.get('price')}</td></tr>
                        <tr style="border-bottom: 1px solid #374151;"><td style="padding: 6px 0; color: #9ca3af; border: none;">MA5 (5일 이동평균)</td><td style="text-align: right; font-weight: 700; ; border: none;">{stock.get('ma5')}</td></tr>
                        <tr style="border-bottom: 1px solid #374151;"><td style="padding: 6px 0; color: #9ca3af; border: none;">MA20 (20일 이동평균)</td><td style="text-align: right; font-weight: 700; ; border: none;">{stock.get('ma20')}</td></tr>
                        <tr style="border-bottom: 1px solid #374151;"><td style="padding: 6px 0; color: #9ca3af; border: none;">RSI (14일)</td><td style="text-align: right; font-weight: 700; ; border: none;">{stock.get('rsi')}</td></tr>
                        <tr style="border-bottom: 1px solid #374151;"><td style="padding: 6px 0; color: #9ca3af; border: none;">호가 불균형 비율</td><td style="text-align: right; font-weight: 700; ; border: none;">{stock.get('orderbook_ratio')}</td></tr>
                        <tr style="border-bottom: 1px solid #374151;"><td style="padding: 6px 0; color: #9ca3af; border: none;">수급 심리 상태</td><td style="text-align: right; font-weight: 700;  border: none;">{stock.get('sentiment')}</td></tr>
                        <tr><td style="padding: 6px 0; color: #9ca3af; border: none;">투자 경고 상태</td><td style="text-align: right; font-weight: 700; color: #ef4444; border: none;">{stock.get('warning_status')}</td></tr>
                    </table>
                </div>
                """)
    
    # 2. 기술적 및 수급 분석 대조
    st.markdown("---")
    st.markdown("#### 📈 2. 기술적 및 수급 분석 결과")
    col_an1, col_an2 = st.columns(2)
    with col_an1:
        st.info("💡 **기술적 지표 분석 (RSI 및 이동평균선 추세)**")
        st.write(report_data.get("technical_analysis", ""))
    with col_an2:
        st.info("💼 **수급 강도 및 투자 심리 분석**")
        st.write(report_data.get("supply_demand_analysis", ""))
        
    # 3. 최선호주 (Top Pick) 및 상대 강도
    st.markdown("---")
    st.markdown("#### 🏆 3. 종합 최선호주 (Top Pick) 및 상대 강도 비교")
    top_pick = report_data.get("top_pick_selection", "선정 중")
    st.html(f"""
    <div style="background: linear-gradient(135deg, rgba(0, 201, 255, 0.08) 0%, rgba(146, 254, 157, 0.08) 100%);
                border: 2px solid #92FE9D; border-radius: 12px; padding: 25px; text-align: center; margin-bottom: 25px;">
        <span style="font-size: 1.1rem; color: #8892b0; font-weight: 600; letter-spacing: 1px;">종합 최선호주 (Top Pick)</span><br>
        <span style="font-size: 2.6rem; color: #92FE9D; font-weight: 800; text-shadow: 0 0 12px rgba(146,254,157,0.4);">{top_pick}</span>
    </div>
    """)
    
    col_tp1, col_tp2 = st.columns(2)
    with col_tp1:
        st.success("🎯 **단기 관점 (1~2주) 최선호 의견**")
        st.write(report_data.get("top_pick_short", ""))
    with col_tp2:
        st.success("🎯 **중기 관점 (1개월) 최선호 의견**")
        st.write(report_data.get("top_pick_mid", ""))
        
    # 4. 종목별 투자 가이드
    st.markdown("---")
    st.markdown("#### 🛠️ 4. 종목별 대응 전략 & 리스크 요인")
    col_str1, col_str2 = st.columns(2)
    with col_str1:
        st.warning(f"⚡ **{name_a} 대응 전략 및 손절 기준**")
        st.write(report_data.get("strategy_a", ""))
    with col_str2:
        st.warning(f"⚡ **{name_b} 대응 전략 및 손절 기준**")
        st.write(report_data.get("strategy_b", ""))
else:
    st.info("👈 왼쪽 Control Panel에서 'AI 비교 분석 시작' 버튼을 누르면 AI 에이전트들이 실시간 가격 및 기술적 분석 보고서를 생성합니다.")
