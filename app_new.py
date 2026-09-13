import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import anthropic
import pandas as pd
import numpy as np
import os
from fallback_data import FALLBACK_DATA, INDUSTRY_BENCHMARKS
from alpha_vantage import fetch_alpha_vantage
from predict import predict_stock_price
from export_pdf import generate_pdf_report

st.set_page_config(
    page_title="FinSight",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp {
    background: linear-gradient(135deg, #060818 0%, #0a0f2e 25%, #0d1a1a 50%, #0a0f2e 75%, #060818 100%);
    color: #e2e8f0;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d20 0%, #0a1628 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.3);
}
.kpi-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 6px 0;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
}
.kpi-label {
    font-size: 10px;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
}
.kpi-value { font-size: 26px; font-weight: 800; color: #6366f1; }
.kpi-value-green { font-size: 26px; font-weight: 800; color: #10b981; }
.kpi-value-amber { font-size: 26px; font-weight: 800; color: #f59e0b; }
.kpi-value-red { font-size: 26px; font-weight: 800; color: #ef4444; }
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.4);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    color: #10b981;
}
.section-header {
    font-size: 24px;
    font-weight: 800;
    color: #f1f5f9;
    margin: 28px 0 8px 0;
}
.section-subheader { font-size: 13px; color: #64748b; margin-bottom: 20px; }
.agent-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(139,92,246,0.04) 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-left: 3px solid #6366f1;
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}
.agent-name { font-size: 12px; font-weight: 700; color: #6366f1; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px; }
.agent-text { font-size: 13px; color: #cbd5e1; line-height: 1.7; }
.success-box { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.3); border-radius: 10px; padding: 14px 18px; color: #10b981; font-size: 13px; }
.warning-box { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.3); border-radius: 10px; padding: 14px 18px; color: #ef4444; font-size: 13px; }
.info-box { background: rgba(6,182,212,0.08); border: 1px solid rgba(6,182,212,0.3); border-radius: 10px; padding: 14px 18px; color: #06b6d4; font-size: 13px; }
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white; border: none; border-radius: 10px;
    padding: 10px 24px; font-weight: 700; font-size: 13px;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3);
}
[data-testid="metric-container"] { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 16px; }
hr { border-color: rgba(255,255,255,0.06); }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #060818; }
::-webkit-scrollbar-thumb { background: #6366f1; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#94a3b8", family="Inter, sans-serif", size=12),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.08)", tickfont=dict(color="#64748b")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.08)", tickfont=dict(color="#64748b")),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
)

COLORS = {"blue": "#6366f1", "purple": "#8b5cf6", "cyan": "#06b6d4", "green": "#10b981", "amber": "#f59e0b", "red": "#ef4444", "pink": "#ec4899"}

@st.cache_data
def load_nifty500():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nifty500.csv")
    df = pd.read_csv(csv_path)
    companies = {}
    for _, row in df.iterrows():
        name = str(row["Company Name"]).strip()
        symbol = str(row["Symbol"]).strip()
        industry = str(row["Industry"]).strip()
        companies[name] = {"ticker": f"{symbol}.NS", "industry": industry, "description": f"{industry} company listed on NSE"}
    return companies

COMPANIES = load_nifty500()

@st.cache_data(ttl=300)
def fetch_live_data(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.info
        fin = t.financials
        bs = t.balance_sheet
        cf = t.cashflow
        def safe(val):
            try:
                v = float(val)
                return round(v / 1e7, 2) if not np.isnan(v) else None
            except:
                return None 


        def get_row(df, *keys):
            for key in keys:
                if df is not None and not df.empty and key in df.index:
                    return safe(df.loc[key].iloc[0])
            return None
        return {
            "revenue": get_row(fin, "Total Revenue"),
            "gross_profit": get_row(fin, "Gross Profit") or get_row(fin, "Net Interest Income"),
            "ebitda": get_row(fin, "EBITDA") or (
                (get_row(fin, "EBIT", "Operating Income") or 0) +
                (get_row(fin, "Reconciled Depreciation", "Depreciation And Amortization") or 0)
            ) or get_row(fin, "Net Interest Income") or None,
            "ebit": get_row(fin, "EBIT", "Operating Income") or get_row(fin, "Net Interest Income"),
            "net_income": get_row(fin, "Net Income"),
            "total_assets": get_row(bs, "Total Assets"),
            "total_debt": get_row(bs, "Total Debt", "Long Term Debt"),
            "cash": get_row(bs, "Cash And Cash Equivalents", "Cash"),
            "capex": abs(get_row(cf, "Capital Expenditure") or 0),
            "market_cap": safe(info.get("marketCap")),
            "pe_ratio": round(info.get("trailingPE", 0), 2) if info.get("trailingPE") else None,
            "pb_ratio": round(info.get("priceToBook", 0), 2) if info.get("priceToBook") else None,
            "dividend_yield": round((info.get("dividendYield", 0) or 0) * 100, 2),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "sector": info.get("sector", "N/A"),
            "roe": round((info.get("returnOnEquity", 0) or 0) * 100, 2),
            "net_interest_income": get_row(fin, "Net Interest Income"),
            "operating_profit": get_row(fin, "Operating Income", "EBIT"),
            "nim": round(info.get("netInterestMargin", 0) * 100, 2) if info.get("netInterestMargin") else None,
            
        }
    except:
        return None

def get_company_data(company_name, ticker):
    # Try fallback first on cloud (Yahoo Finance blocked)
    fallback = FALLBACK_DATA.get(company_name)
    if fallback:
        return fallback, "fallback"
    # Try live data
    live = fetch_live_data(ticker)
    if live and live.get("revenue"):
        return live, "live"
    # Try alpha vantage
    alpha = fetch_alpha_vantage(ticker)
    if alpha and alpha.get("revenue"):
        return alpha, "live"
    return None, "none"
    # Try with different headers for cloud deployment
    try:
        import yfinance as yf
        import pandas as pd
        t = yf.Ticker(ticker)
        t._session = None
        info = t.fast_info
        if hasattr(info, 'last_price') and info.last_price:
            basic = {
                "revenue": None,
                "gross_profit": None,
                "ebitda": None,
                "ebit": None,
                "net_income": None,
                "total_assets": None,
                "total_debt": None,
                "cash": None,
                "capex": 0,
                "market_cap": round(float(info.market_cap) / 1e7, 2) if hasattr(info, 'market_cap') and info.market_cap else None,
                "pe_ratio": round(float(info.pe_ratio), 2) if hasattr(info, 'pe_ratio') and info.pe_ratio else None,
                "pb_ratio": None,
                "dividend_yield": 0,
                "52w_high": float(info.fifty_two_week_high) if hasattr(info, 'fifty_two_week_high') else None,
                "52w_low": float(info.fifty_two_week_low) if hasattr(info, 'fifty_two_week_low') else None,
                "current_price": float(info.last_price) if hasattr(info, 'last_price') else None,
                "sector": "N/A",
                "roe": None,
                "net_interest_income": None,
                "operating_profit": None,
                "nim": None,
            }
            return basic, "partial"
    except:
        pass
    return None, "none"


def get_company_data(company_name, ticker):
    live = fetch_live_data(ticker)
    if live and live.get("revenue"):
        return live, "live"
    fallback = FALLBACK_DATA.get(company_name)
    if fallback:
        return fallback, "fallback"
    # Try with different headers for cloud deployment
    try:
        import yfinance as yf
        import pandas as pd
        t = yf.Ticker(ticker)
        t._session = None
        info = t.fast_info
        if hasattr(info, 'last_price') and info.last_price:
            basic = {
                "revenue": None,
                "gross_profit": None,
                "ebitda": None,
                "ebit": None,
                "net_income": None,
                "total_assets": None,
                "total_debt": None,
                "cash": None,
                "capex": 0,
                "market_cap": round(float(info.market_cap) / 1e7, 2) if hasattr(info, 'market_cap') and info.market_cap else None,
                "pe_ratio": round(float(info.pe_ratio), 2) if hasattr(info, 'pe_ratio') and info.pe_ratio else None,
                "pb_ratio": None,
                "dividend_yield": 0,
                "52w_high": float(info.fifty_two_week_high) if hasattr(info, 'fifty_two_week_high') else None,
                "52w_low": float(info.fifty_two_week_low) if hasattr(info, 'fifty_two_week_low') else None,
                "current_price": float(info.last_price) if hasattr(info, 'last_price') else None,
                "sector": "N/A",
                "roe": None,
                "net_interest_income": None,
                "operating_profit": None,
                "nim": None,
            }
            return basic, "partial"
    except:
        pass
    return None, "none"


def get_company_data(company_name, ticker):
    live = fetch_live_data(ticker)
    if live and live.get("revenue"):
        return live, "live"
    fallback = FALLBACK_DATA.get(company_name)
    if fallback:
        return fallback, "fallback"
    # Try with different headers for cloud deployment
    try:
        import yfinance as yf
        import pandas as pd
        t = yf.Ticker(ticker)
        t._session = None
        info = t.fast_info
        if hasattr(info, 'last_price') and info.last_price:
            basic = {
                "revenue": None,
                "gross_profit": None,
                "ebitda": None,
                "ebit": None,
                "net_income": None,
                "total_assets": None,
                "total_debt": None,
                "cash": None,
                "capex": 0,
                "market_cap": round(float(info.market_cap) / 1e7, 2) if hasattr(info, 'market_cap') and info.market_cap else None,
                "pe_ratio": round(float(info.pe_ratio), 2) if hasattr(info, 'pe_ratio') and info.pe_ratio else None,
                "pb_ratio": None,
                "dividend_yield": 0,
                "52w_high": float(info.fifty_two_week_high) if hasattr(info, 'fifty_two_week_high') else None,
                "52w_low": float(info.fifty_two_week_low) if hasattr(info, 'fifty_two_week_low') else None,
                "current_price": float(info.last_price) if hasattr(info, 'last_price') else None,
                "sector": "N/A",
                "roe": None,
                "net_interest_income": None,
                "operating_profit": None,
                "nim": None,
            }
            return basic, "partial"
    except:
        pass
    return None, "none"


def get_company_data(company_name, ticker):
    live = fetch_live_data(ticker)
    if live and live.get("revenue"):
        return live, "live"
    fallback = FALLBACK_DATA.get(company_name)
    if fallback:
        return fallback, "fallback"
    # Try with different headers for cloud deployment
    try:
        import yfinance as yf
        import pandas as pd
        t = yf.Ticker(ticker)
        t._session = None
        info = t.fast_info
        if hasattr(info, 'last_price') and info.last_price:
            basic = {
                "revenue": None,
                "gross_profit": None,
                "ebitda": None,
                "ebit": None,
                "net_income": None,
                "total_assets": None,
                "total_debt": None,
                "cash": None,
                "capex": 0,
                "market_cap": round(float(info.market_cap) / 1e7, 2) if hasattr(info, 'market_cap') and info.market_cap else None,
                "pe_ratio": round(float(info.pe_ratio), 2) if hasattr(info, 'pe_ratio') and info.pe_ratio else None,
                "pb_ratio": None,
                "dividend_yield": 0,
                "52w_high": float(info.fifty_two_week_high) if hasattr(info, 'fifty_two_week_high') else None,
                "52w_low": float(info.fifty_two_week_low) if hasattr(info, 'fifty_two_week_low') else None,
                "current_price": float(info.last_price) if hasattr(info, 'last_price') else None,
                "sector": "N/A",
                "roe": None,
                "net_interest_income": None,
                "operating_profit": None,
                "nim": None,
            }
            return basic, "partial"
    except:
        pass
    return None, "none"


def apply_stresss(data, stresss):
    revenue = data.get("revenue") or 1000
    gross_profit = data.get("gross_profit") or revenue * 0.3
    ebitda = data.get("ebitda") or revenue * 0.2
    net_income = data.get("net_income") or revenue * 0.1
    total_debt = data.get("total_debt") or 200
    cash = data.get("cash") or 100
    total_assets = data.get("total_assets") or revenue * 1.5
    rev_stress = 1 + stresss.get("revenue", 0) / 100
    cost_stress = 1 + stresss.get("cost", 0) / 100
    interest_stress = 1 + stresss.get("interest", 0) / 100
    stressed_revenue = revenue * rev_stress
    stressed_gross = gross_profit * rev_stress / cost_stress
    stressed_ebitda = ebitda * rev_stress / cost_stress
    stressed_net = net_income * rev_stress / cost_stress / interest_stress
    stressed_debt = total_debt * (1 + stresss.get("debt", 0) / 100)
    stressed_cash = cash * (1 - abs(stresss.get("revenue", 0)) / 200)
    ebitda_margin = (stressed_ebitda / stressed_revenue * 100) if stressed_revenue else 0
    debt_to_equity = stressed_debt / max((total_assets - stressed_debt), 1)
    current_ratio = stressed_cash / max(stressed_debt * 0.3, 1)
    interest_coverage = stressed_ebitda / max(stressed_debt * 0.08 * interest_stress, 1)
    resilience = min(100, max(0,
        (min(ebitda_margin, 30) / 30 * 25) +
        (min(current_ratio, 3) / 3 * 25) +
        (max(0, (3 - debt_to_equity)) / 3 * 25) +
        (min(interest_coverage, 10) / 10 * 25)
    ))
    return {
        "revenue": stressed_revenue, "gross_profit": stressed_gross,
        "ebitda": stressed_ebitda, "net_income": stressed_net,
        "total_debt": stressed_debt, "cash": stressed_cash,
        "ebitda_margin": ebitda_margin, "debt_to_equity": debt_to_equity,
        "current_ratio": current_ratio, "interest_coverage": interest_coverage,
        "resilience": resilience, "total_assets": total_assets,
    }

def pl_chart(data, title="P&L Overview"):
    labels = ["Revenue", "Gross Profit", "EBITDA", "Net Income"]
    values = [data.get("revenue") or 0, data.get("gross_profit") or 0, data.get("ebitda") or 0, data.get("net_income") or 0]
    colors = [COLORS["blue"], COLORS["cyan"], COLORS["green"], COLORS["purple"]]
    fig = go.Figure()
    for label, value, color in zip(labels, values, colors):
        fig.add_trace(go.Bar(x=[label], y=[value], marker=dict(color=color, opacity=0.85),
            text=[f"₹{value:,.0f}Cr"], textposition="outside",
            textfont=dict(color="#e2e8f0", size=11), name=label, showlegend=False))
    fig.update_layout(title=dict(text=title, font=dict(size=15, color="#e2e8f0")), height=320, **CHART_THEME)
    return fig

def resilience_gauge(score):
    color = COLORS["green"] if score >= 70 else COLORS["amber"] if score >= 40 else COLORS["red"]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number=dict(font=dict(size=40, color=color), suffix="/100"),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#475569"),
            bar=dict(color=color, thickness=0.25),
            bgcolor="rgba(255,255,255,0.02)",
            bordercolor="rgba(255,255,255,0.08)",
            steps=[
                dict(range=[0, 40], color="rgba(239,68,68,0.1)"),
                dict(range=[40, 70], color="rgba(245,158,11,0.1)"),
                dict(range=[70, 100], color="rgba(16,185,129,0.1)"),
            ],
        ),
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"), height=240, margin=dict(l=20,r=20,t=20,b=20))
    return fig

def comparison_chart(baseline, stressed, metrics, labels):
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Baseline", x=labels, y=[baseline.get(m, 0) for m in metrics],
        marker=dict(color=COLORS["blue"], opacity=0.8),
        text=[f"₹{baseline.get(m,0):,.0f}" for m in metrics], textposition="outside",
        textfont=dict(color="#94a3b8", size=10)))
    fig.add_trace(go.Bar(name="Stressed", x=labels, y=[stressed.get(m, 0) for m in metrics],
        marker=dict(color=COLORS["red"], opacity=0.8),
        text=[f"₹{stressed.get(m,0):,.0f}" for m in metrics], textposition="outside",
        textfont=dict(color="#94a3b8", size=10)))
    fig.update_layout(barmode="group", title="Baseline vs Stressed", height=350, **CHART_THEME)
    return fig

def radar_chart(metrics_dict, title="Financial Profile"):
    categories = list(metrics_dict.keys())
    values = list(metrics_dict.values())
    values += values[:1]
    categories += categories[:1]
    fig = go.Figure(go.Scatterpolar(
        r=values, theta=categories, fill='toself',
        fillcolor="rgba(99,102,241,0.15)",
        line=dict(color=COLORS["blue"], width=2),
        marker=dict(color=COLORS["blue"], size=6),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.02)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.06)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94a3b8")),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        title=dict(text=title, font=dict(size=14, color="#e2e8f0")),
        height=300, margin=dict(l=40,r=40,t=50,b=40), showlegend=False,
    )
    return fig
@st.cache_data(ttl=300)
def fetch_price_history(ticker, period="1y"):
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        return hist
    except:
        return None

def price_history_chart(hist, company_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode="lines",
        name="Price",
        line=dict(color=COLORS["blue"], width=2),
        fill="tozeroy",
        fillcolor="rgba(99,102,241,0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist["Close"].rolling(20).mean(),
        mode="lines",
        name="20D MA",
        line=dict(color=COLORS["amber"], width=1.5, dash="dash"),
    ))
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist["Close"].rolling(50).mean(),
        mode="lines",
        name="50D MA",
        line=dict(color=COLORS["pink"], width=1.5, dash="dot"),
    ))
    fig.update_layout(
        title=dict(text=f"{company_name} — Price History", font=dict(size=15, color="#e2e8f0")),
        height=350,
        hovermode="x unified",
        **CHART_THEME
    )
    return fig

def volume_chart(hist, company_name):
    colors = [COLORS["green"] if hist["Close"].iloc[i] >= hist["Open"].iloc[i] else COLORS["red"] for i in range(len(hist))]
    fig = go.Figure(go.Bar(
        x=hist.index,
        y=hist["Volume"],
        marker_color=colors,
        opacity=0.7,
        name="Volume",
    ))
    fig.update_layout(
        title=dict(text="Trading Volume", font=dict(size=14, color="#e2e8f0")),
        height=200,
        **CHART_THEME
    )
    return fig
def call_claude(prompt, system="You are a senior financial analyst. Be concise and use bullet points."):
    try:
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model="claude-sonnet-4-6", max_tokens=800,
            system=system, messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"AI unavailable: {str(e)}"


def apply_shocks(data, shocks):
    revenue = data.get("revenue") or 1000
    gross_profit = data.get("gross_profit") or revenue * 0.3
    ebitda = data.get("ebitda") or revenue * 0.2
    net_income = data.get("net_income") or revenue * 0.1
    total_debt = data.get("total_debt") or 200
    cash = data.get("cash") or 100
    total_assets = data.get("total_assets") or revenue * 1.5
    rev_shock = 1 + shocks.get("revenue", 0) / 100
    cost_shock = 1 + shocks.get("cost", 0) / 100
    interest_shock = 1 + shocks.get("interest", 0) / 100
    stressed_revenue = revenue * rev_shock
    stressed_gross = gross_profit * rev_shock / cost_shock
    stressed_ebitda = ebitda * rev_shock / cost_shock
    stressed_net = net_income * rev_shock / cost_shock / interest_shock
    stressed_debt = total_debt * (1 + shocks.get("debt", 0) / 100)
    stressed_cash = cash * (1 - abs(shocks.get("revenue", 0)) / 200)
    ebitda_margin = (stressed_ebitda / stressed_revenue * 100) if stressed_revenue else 0
    debt_to_equity = stressed_debt / max((total_assets - stressed_debt), 1)
    current_ratio = stressed_cash / max(stressed_debt * 0.3, 1)
    interest_coverage = stressed_ebitda / max(stressed_debt * 0.08 * interest_shock, 1)
    resilience = min(100, max(0,
        (min(ebitda_margin, 30) / 30 * 25) +
        (min(current_ratio, 3) / 3 * 25) +
        (max(0, (3 - debt_to_equity)) / 3 * 25) +
        (min(interest_coverage, 10) / 10 * 25)
    ))
    return {
        "revenue": stressed_revenue, "gross_profit": stressed_gross,
        "ebitda": stressed_ebitda, "net_income": stressed_net,
        "total_debt": stressed_debt, "cash": stressed_cash,
        "ebitda_margin": ebitda_margin, "debt_to_equity": debt_to_equity,
        "current_ratio": current_ratio, "interest_coverage": interest_coverage,
        "resilience": resilience, "total_assets": total_assets,
    }

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 16px;'>
        <div style='font-size:36px;'>⚡</div>
        <div style='font-size:20px; font-weight:800; color:#6366f1;'>FinSight</div>
        <div style='font-size:11px; color:#475569; margin-top:4px; text-transform:uppercase; letter-spacing:0.08em;'>Financial Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    search_query = st.text_input("🔍 Search Company", placeholder="Type company name...")
    if search_query:
        matches = [name for name in COMPANIES.keys() if search_query.lower() in name.lower()][:20]
        if matches:
            selected_company = st.selectbox("Results", matches)
        else:
            st.warning("No companies found")
            selected_company = list(COMPANIES.keys())[0]
    else:
        top10 = list(COMPANIES.keys())[:10]
        selected_company = st.selectbox("Select Company", top10)
    company_info = COMPANIES.get(selected_company, {"ticker": "", "industry": "N/A", "description": "N/A"})
    st.markdown(f"""
    <div style='background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2); border-radius:10px; padding:14px; margin:10px 0;'>
        <div style='font-size:10px; color:#6366f1; font-weight:700; text-transform:uppercase;'>Industry</div>
        <div style='font-size:14px; color:#e2e8f0; font-weight:600; margin-top:4px;'>{company_info['industry']}</div>
        <div style='font-size:11px; color:#64748b; margin-top:6px;'>{company_info['ticker']}</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    page = st.radio("", ["📊 Dashboard", "⚡ Crisis Simulator", "🧪 Resilience Lab", "🤖 AI Boardroom", "🔄 Counterfactual", "🏢 Company Compare", "🔮 Price Prediction", "📐 Benchmarks & Ratios"], label_visibility="collapsed")
    st.divider()
    st.markdown("<div style='font-size:10px; color:#334155; text-align:center;'>Powered by Yahoo Finance + Claude AI<br>Not financial advice</div>", unsafe_allow_html=True)

# FETCH DATA
ticker = company_info["ticker"]
with st.spinner(f"Loading live data..."):
    if ticker:
        live, data_source = get_company_data(selected_company, ticker)
    else:
        live, data_source = None, "none"

# DASHBOARD
if page == "📊 Dashboard":
    col_title, col_badge = st.columns([3, 1])
    with col_title:
        st.markdown(f"<div class='section-header'>📊 {selected_company}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-subheader'>{company_info['industry']} • {company_info['ticker']}</div>", unsafe_allow_html=True)
    with col_badge:
        st.markdown("<br>", unsafe_allow_html=True)
        if live:
            if data_source == "live":
                st.markdown("<div class='live-badge'>🟢 LIVE DATA</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='live-badge' style='border-color:#f59e0b; color:#f59e0b;'>🟡 VERIFIED DATA</div>", unsafe_allow_html=True)
    if live:
        c1, c2, c3, c4 = st.columns(4)
        def fmt_cr(val):
            if not val:
                return "N/A"
            if val >= 100000:
                return f"₹{val/100000:.2f}L Cr"
            elif val >= 1000:
                return f"₹{val/1000:.1f}K Cr"
            else:
                return f"₹{val:.0f} Cr"

        is_bank = any(x in company_info['industry'].lower() for x in ['bank', 'financial', 'nbfc'])

        with c1:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Revenue</div><div class='kpi-value'>{fmt_cr(live.get('revenue'))}</div></div>", unsafe_allow_html=True)
        with c2:
            ebitda_label = "Operating Profit" if is_bank else "EBITDA"
            ebitda_val = live.get('operating_profit') if is_bank else live.get('ebitda')
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>{ebitda_label}</div><div class='kpi-value-green'>{fmt_cr(ebitda_val)}</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Market Cap</div><div class='kpi-value-amber'>{fmt_cr(live.get('market_cap'))}</div></div>", unsafe_allow_html=True)
        with c4:
            val = f"{live['pe_ratio']}x" if live.get('pe_ratio') else "N/A"
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>P/E Ratio</div><div class='kpi-value-red'>{val}</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col_pl, col_radar, col_gauge = st.columns([2, 1.5, 1])
        with col_pl:
            st.plotly_chart(pl_chart(live), use_container_width=True)
        with col_radar:
            baseline = apply_stresss(live, {})
            radar_data = {
                "Profitability": min(100, max(0, (live.get('net_income', 0) or 0) / (live.get('revenue', 1) or 1) * 300)),
                "Liquidity": min(100, baseline["current_ratio"] * 30),
                "Leverage": min(100, max(0, 100 - baseline["debt_to_equity"] * 20)),
                "Cash Flow": min(100, (live.get('cash', 0) or 0) / (live.get('revenue', 1) or 1) * 200),
                "Efficiency": min(100, (live.get('ebitda', 0) or 0) / (live.get('revenue', 1) or 1) * 300),
            }
            st.plotly_chart(radar_chart(radar_data), use_container_width=True)
        with col_gauge:
            st.markdown("<div style='text-align:center; font-size:11px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.08em;'>Resilience</div>", unsafe_allow_html=True)
            st.plotly_chart(resilience_gauge(baseline["resilience"]), use_container_width=True)
            label = "Resilient ✅" if baseline["resilience"] >= 70 else "Moderate ⚠️" if baseline["resilience"] >= 40 else "Vulnerable 🔴"
            color = "#10b981" if baseline["resilience"] >= 70 else "#f59e0b" if baseline["resilience"] >= 40 else "#ef4444"
            st.markdown(f"<div style='text-align:center; font-size:15px; font-weight:700; color:{color};'>{label}</div>", unsafe_allow_html=True)
        st.divider()
        st.markdown("<div class='section-header' style='font-size:18px;'>📈 Stock Price History</div>", unsafe_allow_html=True)
        period_col, _ = st.columns([1, 3])
        with period_col:
            period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
        hist = fetch_price_history(ticker, period)
        if hist is not None and not hist.empty:
            st.plotly_chart(price_history_chart(hist, selected_company), use_container_width=True)
            st.plotly_chart(volume_chart(hist, selected_company), use_container_width=True)
        else:
            st.markdown("<div class='warning-box'>⚠️ Price history unavailable</div>", unsafe_allow_html=True)
        st.divider()
        col_export, _ = st.columns([1, 3])
        with col_export:
            if st.button("📄 Export PDF Report"):
                with st.spinner("Generating PDF..."):
                    industry = company_info.get("industry", "IT Services")
                    benchmark = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS.get("IT Services"))
                    baseline = apply_shocks(live, {})
                    pdf_buffer = generate_pdf_report(
                        selected_company, industry, ticker, live, baseline, benchmark
                    )
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_buffer,
                        file_name=f"FinSight_{selected_company.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        st.divider()
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        extra = [
            (m1, "Net Margin", f"{live['net_income']/live['revenue']*100:.1f}%" if live.get('net_income') and live.get('revenue') else "N/A", COLORS["blue"]),
            (m2, "ROE", f"{live.get('roe', 0):.1f}%", COLORS["purple"]),
            (m3, "P/B Ratio", f"{live.get('pb_ratio', 'N/A')}x", COLORS["cyan"]),
            (m4, "52W High", f"₹{live['52w_high']:,.0f}" if live.get('52w_high') else "N/A", COLORS["green"]),
            (m5, "52W Low", f"₹{live['52w_low']:,.0f}" if live.get('52w_low') else "N/A", COLORS["amber"]),
            (m6, "Div Yield", f"{live.get('dividend_yield', 0):.1f}%", COLORS["pink"]),
        ]
        for col, label, val, color in extra:
            with col:
                st.markdown(f"<div class='kpi-card' style='text-align:center; padding:16px;'><div class='kpi-label'>{label}</div><div style='font-size:18px; font-weight:700; color:{color}; margin-top:6px;'>{val}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='warning-box'>⚠️ Could not fetch live data for '{selected_company}'. Try: Infosys Ltd, TCS, Reliance Industries Ltd</div>", unsafe_allow_html=True)

# CRISIS SIMULATOR
elif page == "⚡ Crisis Simulator":
    st.markdown("<div class='section-header'>⚡ Crisis Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>Apply financial stresss and see real-time impact</div>", unsafe_allow_html=True)

    col_sliders, col_results = st.columns([1, 2])

    with col_sliders:
        st.markdown("**🎚️ Stress Parameters**")
        rev_stress = st.slider("Revenue Stress (%)", -60, 20, 0, 1, key="rev")
        cost_stress = st.slider("Cost Pressure (%)", 0, 50, 0, 1, key="cost")
        interest_stress = st.slider("Interest Rate Stress (%)", 0, 100, 0, 5, key="interest")
        debt_stress = st.slider("Debt Leverage Stress (%)", 0, 100, 0, 5, key="debt")
        st.markdown("**📋 Industry Templates**")
        template = st.selectbox("Apply Template", ["None", "IT Slowdown", "Banking NPA Crisis", "Commodity Crash", "Pandemic Stress", "Rate Hike Cycle"])

    if template == "IT Slowdown":
        rev_stress, cost_stress = -20, 10
    elif template == "Banking NPA Crisis":
        rev_stress, cost_stress, debt_stress = -15, 20, 30
    elif template == "Commodity Crash":
        rev_stress, cost_stress = -35, 25
    elif template == "Pandemic Stress":
        rev_stress, cost_stress, interest_stress = -40, 30, 20
    elif template == "Rate Hike Cycle":
        interest_stress, debt_stress = 50, 20

    stresss = {"revenue": rev_stress, "cost": cost_stress, "interest": interest_stress, "debt": debt_stress}

    if live:
        baseline = apply_stresss(live, {})
        stressed = apply_stresss(live, stresss)
        delta_rev = stressed["revenue"] - baseline["revenue"]
        delta_ebitda = stressed["ebitda"] - baseline["ebitda"]
        delta_res = stressed["resilience"] - baseline["resilience"]
        delta_cash = stressed["cash"] - baseline["cash"]

        with col_results:
            s1, s2, s3, s4 = st.columns(4)
            def fmt(val):
                if val >= 100000:
                    return f"₹{val/100000:.1f}L Cr"
                elif val >= 1000:
                    return f"₹{val/1000:.1f}K Cr"
                else:
                    return f"₹{val:.0f} Cr"

            with s1:
                st.metric("Revenue", fmt(stressed['revenue']), f"{delta_rev:+.0f} Cr")
            with s2:
                st.metric("EBITDA", fmt(stressed['ebitda']), f"{delta_ebitda:+.0f} Cr")
            with s3:
                st.metric("Resilience", f"{stressed['resilience']:.0f}/100", f"{delta_res:+.0f} pts")
            with s4:
                st.metric("Cash", fmt(stressed['cash']), f"{delta_cash:+.0f} Cr")

            st.plotly_chart(comparison_chart(baseline, stressed,
                ["revenue", "gross_profit", "ebitda", "net_income"],
                ["Revenue", "Gross Profit", "EBITDA", "Net Income"]), use_container_width=True)

            severity = "🔴 Critical" if delta_res < -30 else "🟠 High" if delta_res < -15 else "🟡 Moderate" if delta_res < -5 else "🟢 Low"
            color = "#ef4444" if delta_res < -30 else "#f59e0b" if delta_res < -15 else "#fbbf24" if delta_res < -5 else "#10b981"
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Crisis Severity</div><div style='font-size:22px; font-weight:800; color:{color};'>{severity}</div><div style='font-size:12px; color:#64748b;'>Resilience changed by {delta_res:+.1f} points</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='warning-box'>⚠️ No live data available.</div>", unsafe_allow_html=True)

# RESILIENCE LAB
elif page == "🧪 Resilience Lab":
    st.markdown("<div class='section-header'>🧪 Resilience Lab</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>Test management interventions and find the best recovery strategy</div>", unsafe_allow_html=True)

    if live:
        baseline = apply_stresss(live, {})
        interventions = {
            "Cost Cutting (10%)": {"cost": -10},
            "Working Capital Optimization": {"revenue": 5},
            "Debt Restructuring": {"debt": -20, "interest": -15},
            "Revenue Diversification": {"revenue": 15},
            "Asset Monetization": {"debt": -30},
            "Emergency Equity Raise": {"debt": -40},
        }
        results = []
        for name, stress in interventions.items():
            result = apply_stresss(live, stress)
            results.append({
                "Intervention": name,
                "Resilience": round(result["resilience"], 1),
                "Improvement": round(result["resilience"] - baseline["resilience"], 1),
                "EBITDA (₹Cr)": round(result["ebitda"], 0),
                "Net Income (₹Cr)": round(result["net_income"], 0),
            })
        df = pd.DataFrame(results).sort_values("Resilience", ascending=False)
        col_table, col_chart = st.columns([1, 1])
        with col_table:
            st.markdown("**📋 Intervention Results**")
            st.dataframe(df, use_container_width=True, hide_index=True)
        with col_chart:
            fig = go.Figure(go.Bar(
                y=df["Intervention"], x=df["Resilience"], orientation="h",
                marker=dict(color=df["Resilience"].tolist(), colorscale=[[0, COLORS["red"]], [0.5, COLORS["amber"]], [1, COLORS["green"]]], cmin=0, cmax=100),
                text=[f"{v:.1f}" for v in df["Resilience"]], textposition="outside",
                textfont=dict(color="#e2e8f0", size=11),
            ))
            fig.update_layout(title="Resilience by Intervention", height=350, **CHART_THEME)
            st.plotly_chart(fig, use_container_width=True)
        best = df.iloc[0]
        st.markdown(f"<div class='success-box'>🏆 <strong>Best Strategy:</strong> {best['Intervention']} → Score: {best['Resilience']}/100 (+{best['Improvement']} pts)</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='warning-box'>⚠️ No live data available.</div>", unsafe_allow_html=True)

# AI BOARDROOM
elif page == "🤖 AI Boardroom":
    st.markdown("<div class='section-header'>🤖 AI Boardroom</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>6 AI agents analyze, debate, and recommend the best strategy</div>", unsafe_allow_html=True)

    if live:
        baseline = apply_stresss(live, {})
        context = f"Company: {selected_company} | Industry: {company_info['industry']} | Revenue: ₹{live.get('revenue','N/A')} Cr | EBITDA: ₹{live.get('ebitda','N/A')} Cr | Net Income: ₹{live.get('net_income','N/A')} Cr | Debt: ₹{live.get('total_debt','N/A')} Cr | Cash: ₹{live.get('cash','N/A')} Cr | Market Cap: ₹{live.get('market_cap','N/A')} Cr | P/E: {live.get('pe_ratio','N/A')}x | Resilience: {baseline['resilience']:.0f}/100"

        agents = [
            ("💼 CFO Agent", "You are the CFO. Analyze financial health and capital structure in 4 bullet points.", COLORS["blue"]),
            ("⚠️ Risk Agent", "You are the CRO. Identify top 4 financial risks.", COLORS["red"]),
            ("🎯 Strategy Agent", "You are the CSO. Recommend 4 strategic responses.", COLORS["purple"]),
            ("🏦 Treasury Agent", "You are the Treasurer. Focus on liquidity and debt in 4 points.", COLORS["cyan"]),
            ("🔴 Challenger Agent", "You are Devil's Advocate. Find 4 critical flaws.", COLORS["amber"]),
            ("👑 CEO Decision", "You are the CEO. Give final 4-point action plan.", COLORS["green"]),
        ]

        if st.button("🚀 Start Boardroom Session", type="primary"):
            for agent_name, system, color in agents:
                with st.expander(agent_name, expanded=True):
                    with st.spinner("Analyzing..."):
                        response = call_claude(f"Analyze:\n{context}", system)
                    st.markdown(f"<div class='agent-card'><div class='agent-name' style='color:{color};'>{agent_name}</div><div class='agent-text'>{response}</div></div>", unsafe_allow_html=True)

        st.divider()
        decision = st.radio("Your Decision", ["✅ Approve AI Recommendation", "❌ Reject and Override", "🔄 Request More Analysis"])
        if st.button("Submit Decision"):
            st.markdown(f"<div class='success-box'>✅ Decision recorded: {decision}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='warning-box'>⚠️ No live data available.</div>", unsafe_allow_html=True)

# COUNTERFACTUAL
elif page == "🔄 Counterfactual":
    st.markdown("<div class='section-header'>🔄 Counterfactual Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>Compare alternative strategies side by side</div>", unsafe_allow_html=True)

    if live:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Strategy A**")
            s1_rev = st.slider("Revenue Stress A (%)", -50, 20, -10, key="s1r")
            s1_cost = st.slider("Cost Change A (%)", -20, 50, 5, key="s1c")
        with col2:
            st.markdown("**Strategy B**")
            s2_rev = st.slider("Revenue Stress B (%)", -50, 20, 5, key="s2r")
            s2_cost = st.slider("Cost Change B (%)", -20, 50, 15, key="s2c")

        strat_a = apply_stresss(live, {"revenue": s1_rev, "cost": s1_cost})
        strat_b = apply_stresss(live, {"revenue": s2_rev, "cost": s2_cost})

        ca, cb = st.columns(2)
        with ca:
            color_a = "#10b981" if strat_a["resilience"] >= 70 else "#f59e0b" if strat_a["resilience"] >= 40 else "#ef4444"
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Strategy A Resilience</div><div style='font-size:32px; font-weight:800; color:{color_a};'>{strat_a['resilience']:.0f}/100</div><div style='font-size:12px; color:#64748b;'>EBITDA: ₹{strat_a['ebitda']:,.0f}Cr</div></div>", unsafe_allow_html=True)
        with cb:
            color_b = "#10b981" if strat_b["resilience"] >= 70 else "#f59e0b" if strat_b["resilience"] >= 40 else "#ef4444"
            st.markdown(f"<div class='kpi-card'><div class='kpi-label'>Strategy B Resilience</div><div style='font-size:32px; font-weight:800; color:{color_b};'>{strat_b['resilience']:.0f}/100</div><div style='font-size:12px; color:#64748b;'>EBITDA: ₹{strat_b['ebitda']:,.0f}Cr</div></div>", unsafe_allow_html=True)

        fig = go.Figure()
        metrics = ["revenue", "ebitda", "net_income", "cash"]
        labels = ["Revenue", "EBITDA", "Net Income", "Cash"]
        fig.add_trace(go.Bar(name="Strategy A", x=labels, y=[strat_a.get(m,0) for m in metrics], marker=dict(color=COLORS["blue"], opacity=0.85), text=[f"₹{strat_a.get(m,0):,.0f}" for m in metrics], textposition="outside"))
        fig.add_trace(go.Bar(name="Strategy B", x=labels, y=[strat_b.get(m,0) for m in metrics], marker=dict(color=COLORS["green"], opacity=0.85), text=[f"₹{strat_b.get(m,0):,.0f}" for m in metrics], textposition="outside"))
        fig.update_layout(barmode="group", title="Strategy A vs Strategy B", height=350, **CHART_THEME)
        st.plotly_chart(fig, use_container_width=True)

        if st.button("🤖 Get AI Analysis"):
            with st.spinner("Analyzing..."):
                prompt = f"Compare strategies for {selected_company}: A (Revenue {s1_rev}%, Cost {s1_cost}%) → Resilience {strat_a['resilience']:.0f}/100 vs B (Revenue {s2_rev}%, Cost {s2_cost}%) → Resilience {strat_b['resilience']:.0f}/100. Which is better and why? 4 key insights."
                analysis = call_claude(prompt)
            st.markdown(f"<div class='agent-card'><div class='agent-name'>AI Analysis</div><div class='agent-text'>{analysis}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='warning-box'>⚠️ No live data available.</div>", unsafe_allow_html=True)

# COMPANY COMPARE
elif page == "🏢 Company Compare":
    st.markdown("<div class='section-header'>🏢 Company Comparison</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>Benchmark Nifty 500 companies under the same crisis scenario</div>", unsafe_allow_html=True)

    selected_companies = st.multiselect("Select Companies (max 6)", list(COMPANIES.keys()), default=list(COMPANIES.keys())[:4], max_selections=6)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        comp_rev = st.slider("Shared Revenue Stress (%)", -50, 0, -20)
    with col_s2:
        comp_cost = st.slider("Shared Cost Pressure (%)", 0, 50, 10)

    if st.button("📊 Run Comparison") and selected_companies:
        results = []
        progress = st.progress(0)
        status = st.empty()
        for i, company in enumerate(selected_companies):
            status.markdown(f"<div class='info-box'>⚡ Fetching {company}...</div>", unsafe_allow_html=True)
            data = fetch_live_data(COMPANIES[company]["ticker"])
            if data:
                stressed = apply_stresss(data, {"revenue": comp_rev, "cost": comp_cost})
                results.append({
                    "Company": company,
                    "Industry": COMPANIES[company]["industry"],
                    "Resilience": round(stressed["resilience"], 1),
                    "Revenue (₹Cr)": round(stressed["revenue"], 0),
                    "EBITDA (₹Cr)": round(stressed["ebitda"], 0),
                })
            progress.progress((i + 1) / len(selected_companies))
        status.empty()
        if results:
            df = pd.DataFrame(results).sort_values("Resilience", ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)
            fig = go.Figure(go.Bar(
                x=df["Company"], y=df["Resilience"],
                marker=dict(color=df["Resilience"].tolist(), colorscale=[[0, COLORS["red"]], [0.4, COLORS["amber"]], [1, COLORS["green"]]], cmin=0, cmax=100, showscale=True),
                text=[f"{v:.0f}" for v in df["Resilience"]], textposition="outside",
                textfont=dict(color="#e2e8f0", size=12),
            ))
            fig.update_layout(title="Resilience Ranking", height=400, **CHART_THEME)
            st.plotly_chart(fig, use_container_width=True)
            winner = df.iloc[0]
            loser = df.iloc[-1]
            st.markdown(f"<div class='success-box'>🏆 Most Resilient: {winner['Company']} — {winner['Resilience']}/100</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='warning-box'>⚠️ Most Vulnerable: {loser['Company']} — {loser['Resilience']}/100</div>", unsafe_allow_html=True)
# PRICE PREDICTION
elif page == "🔮 Price Prediction":
    st.markdown("<div class='section-header'>🔮 Stock Price Prediction</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>ML-powered 30-day price forecast with confidence intervals</div>", unsafe_allow_html=True)

    col_settings, col_info = st.columns([1, 2])
    with col_settings:
        pred_months = st.selectbox("Forecast Period", ["1 Month", "3 Months", "6 Months"], index=0)
        pred_days = {"1 Month": 1, "3 Months": 3, "6 Months": 6}[pred_months]
        run_prediction = st.button("🚀 Run Prediction Model", type="primary")

    if run_prediction:
        with st.spinner("Training ML model — analyzing news, technicals and candlesticks..."):
            result = predict_stock_price(ticker, selected_company, pred_days)

        if result:
            with col_info:
                p1, p2, p3, p4 = st.columns(4)
                change_color = "#10b981" if result["change_pct"] >= 0 else "#ef4444"
                change_arrow = "▲" if result["change_pct"] >= 0 else "▼"
                with p1:
                    st.markdown(f"""<div class='kpi-card'>
                        <div class='kpi-label'>Current Price</div>
                        <div class='kpi-value'>₹{result['last_price']:,.0f}</div>
                    </div>""", unsafe_allow_html=True)
                with p2:
                    st.markdown(f"""<div class='kpi-card'>
                        <div class='kpi-label'>Predicted ({pred_days}d)</div>
                        <div style='font-size:22px; font-weight:800; color:{change_color};'>₹{result['predicted_price']:,.0f}</div>
                    </div>""", unsafe_allow_html=True)
                with p3:
                    st.markdown(f"""<div class='kpi-card'>
                        <div class='kpi-label'>Expected Change</div>
                        <div style='font-size:22px; font-weight:800; color:{change_color};'>{change_arrow} {abs(result['change_pct'])}%</div>
                    </div>""", unsafe_allow_html=True)
                with p4:
                    st.markdown(f"""<div class='kpi-card'>
                        <div class='kpi-label'>Model Accuracy</div>
                        <div class='kpi-value-green'>{result['model_score']}%</div>
                    </div>""", unsafe_allow_html=True)

            # Main prediction chart
            import plotly.graph_objects as go
            fig = go.Figure()

            # Historical prices
            fig.add_trace(go.Scatter(
                x=result["historical_dates"][-180:],
                y=result["historical_prices"][-180:],
                mode="lines",
                name="Historical Price",
                line=dict(color=COLORS["blue"], width=2),
            ))

            # Confidence interval
            fig.add_trace(go.Scatter(
                x=result["future_dates"] + result["future_dates"][::-1],
                y=result["future_upper"] + result["future_lower"][::-1],
                fill="toself",
                fillcolor="rgba(139,92,246,0.15)",
                line=dict(color="rgba(0,0,0,0)"),
                name="Confidence Range",
            ))

            # Predicted prices
            fig.add_trace(go.Scatter(
                x=result["future_dates"],
                y=result["future_prices"],
                mode="lines+markers",
                name="Predicted Price",
                line=dict(color=COLORS["purple"], width=2, dash="dash"),
                marker=dict(size=6, color=COLORS["purple"]),
            ))

            # Upper bound
            fig.add_trace(go.Scatter(
                x=result["future_dates"],
                y=result["future_upper"],
                mode="lines",
                name="Best Case",
                line=dict(color=COLORS["green"], width=1, dash="dot"),
            ))

            # Lower bound
            fig.add_trace(go.Scatter(
                x=result["future_dates"],
                y=result["future_lower"],
                mode="lines",
                name="Worst Case",
                line=dict(color=COLORS["red"], width=1, dash="dot"),
            ))

            fig.update_layout(
                title=f"{selected_company} — {pred_months} Price Forecast",
                height=450,
                hovermode="x unified",
                **CHART_THEME
            )
            st.plotly_chart(fig, use_container_width=True)

            # Model details
            st.divider()
            d1, d2, d3, d4 = st.columns(4)
            with d1:
                st.markdown(f"""<div class='kpi-card' style='text-align:center;'>
                    <div class='kpi-label'>EMA 20</div>
                    <div style='font-size:18px; font-weight:700; color:{COLORS["cyan"]};'>₹{result.get('ema20', 0):,.0f}</div>
                </div>""", unsafe_allow_html=True)
            with d2:
                st.markdown(f"""<div class='kpi-card' style='text-align:center;'>
                    <div class='kpi-label'>EMA 50</div>
                    <div style='font-size:18px; font-weight:700; color:{COLORS["amber"]};'>₹{result.get('ema50', 0):,.0f}</div>
                </div>""", unsafe_allow_html=True)            
            with d3:
                st.markdown(f"""<div class='kpi-card' style='text-align:center;'>
                    <div class='kpi-label'>Daily Volatility</div>
                    <div style='font-size:18px; font-weight:700; color:{COLORS["pink"]};'>{result['volatility']}%</div>
                </div>""", unsafe_allow_html=True)
            with d4:
                best_case = result['future_upper'][-1]
                worst_case = result['future_lower'][-1]
                st.markdown(f"""<div class='kpi-card' style='text-align:center;'>
                    <div class='kpi-label'>Price Range</div>
                    <div style='font-size:14px; font-weight:700; color:{COLORS["green"]};'>▲ ₹{best_case:,.0f}</div>
                    <div style='font-size:14px; font-weight:700; color:{COLORS["red"]};'>▼ ₹{worst_case:,.0f}</div>
                </div>""", unsafe_allow_html=True)
            # Technical signals
            st.divider()
            st.markdown("<div class='section-header' style='font-size:18px;'>📡 Technical Signals</div>", unsafe_allow_html=True)
            t1, t2, t3, t4, t5 = st.columns(5)
            signals = [
                (t1, "RSI", f"{result['rsi']}", result['rsi_signal'], "#f59e0b"),
                (t2, "MACD", result['macd_signal'], result['macd_signal'], "#6366f1"),
                (t3, "Bollinger", result['bb_signal'], result['bb_signal'], "#06b6d4"),
                (t4, "Trend", result['trend'], result['trend'], "#10b981"),
                (t5, "Overall", result['overall_signal'], result['overall_signal'], "#8b5cf6"),
            ]
            for col, label, val, signal, color in signals:
                sig_color = "#10b981" if "Bull" in signal or "Over" not in signal and "Up" in signal else "#ef4444" if "Bear" in signal or "Down" in signal else "#f59e0b"
                with col:
                    st.markdown(f"""<div class='kpi-card' style='text-align:center;'>
                        <div class='kpi-label'>{label}</div>
                        <div style='font-size:16px; font-weight:700; color:{sig_color};'>{val}</div>
                    </div>""", unsafe_allow_html=True)

            # Candlestick patterns
            if result["patterns"]:
                st.markdown("<div class='section-header' style='font-size:18px;'>🕯️ Candlestick Patterns Detected</div>", unsafe_allow_html=True)
                for pattern, sentiment, description in result["patterns"]:
                    color = "#10b981" if sentiment == "bullish" else "#ef4444" if sentiment == "bearish" else "#f59e0b"
                    st.markdown(f"""<div class='kpi-card'>
                        <div style='font-size:14px; font-weight:700; color:{color};'>{pattern} — {sentiment.upper()}</div>
                        <div style='font-size:12px; color:#64748b; margin-top:4px;'>{description}</div>
                    </div>""", unsafe_allow_html=True)

            # News sentiment
            st.markdown("<div class='section-header' style='font-size:18px;'>📰 News Sentiment</div>", unsafe_allow_html=True)
            news = result["news"]
            news_color = "#10b981" if news["sentiment_label"] == "Bullish" else "#ef4444" if news["sentiment_label"] == "Bearish" else "#f59e0b"
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>Market Sentiment</div>
                <div style='font-size:22px; font-weight:800; color:{news_color};'>{news["sentiment_label"]}</div>
                <div style='font-size:12px; color:#64748b; margin-top:4px;'>Positive signals: {news["positive_signals"]} | Negative signals: {news["negative_signals"]}</div>
            </div>""", unsafe_allow_html=True)
            if news["headlines"]:
                st.markdown("**Recent Headlines:**")
                for headline in news["headlines"]:
                    st.markdown(f"• {headline}")
            st.markdown("""<div class='info-box'>
                ⚠️ <strong>Disclaimer:</strong> This prediction is based on historical price patterns using Linear Regression. 
                It is for educational and analytical purposes only. Not financial advice. 
                Stock markets are inherently unpredictable and actual prices may vary significantly.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div class='warning-box'>⚠️ Could not generate prediction. Insufficient historical data for this company.</div>", unsafe_allow_html=True)
# BENCHMARKS & RATIOS
elif page == "📐 Benchmarks & Ratios":
    st.markdown("<div class='section-header'>📐 Benchmarks & Financial Ratios</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>Compare company metrics against industry averages and advanced financial ratios</div>", unsafe_allow_html=True)

    if live:
        industry = company_info.get("industry", "IT Services")
        benchmark = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS.get("IT Services"))

        # ── INDUSTRY BENCHMARK COMPARISON ──
        st.markdown("<div class='section-header' style='font-size:18px;'>🏭 Industry Benchmark Comparison</div>", unsafe_allow_html=True)

        revenue = live.get("revenue") or 1000
        ebitda = live.get("ebitda") or 0
        net_income = live.get("net_income") or 0
        total_debt = live.get("total_debt") or 0
        total_assets = live.get("total_assets") or revenue * 1.5
        equity = total_assets - total_debt

        company_ebitda_margin = round(ebitda / revenue * 100, 1) if revenue else 0
        company_roe = live.get("roe") or (
            round(net_income / max(equity, 1) * 100, 1) if net_income and equity else 0
        )
        company_pe = live.get("pe_ratio") or 0
        company_de = round(total_debt / max(equity, 1), 2)

        metrics_compare = [
            ("EBITDA Margin", company_ebitda_margin, benchmark["avg_ebitda_margin"], "%"),
            ("ROE", company_roe, benchmark["avg_roe"], "%"),
            ("P/E Ratio", company_pe, benchmark["avg_pe"], "x"),
            ("Debt/Equity", company_de, benchmark["avg_debt_equity"], "x"),
        ]

        for metric_name, company_val, industry_val, unit in metrics_compare:
            col_label, col_bar, col_vals = st.columns([1, 2, 1])
            with col_label:
                st.markdown(f"<div style='font-size:13px; font-weight:600; color:#94a3b8; padding-top:8px;'>{metric_name}</div>", unsafe_allow_html=True)
            with col_bar:
                if metric_name == "Debt/Equity":
                    better = company_val < industry_val
                else:
                    better = company_val > industry_val
                color = "#10b981" if better else "#ef4444"
                max_val = max(company_val, industry_val, 0.1) * 1.3
                company_pct = min(company_val / max_val * 100, 100)
                industry_pct = min(industry_val / max_val * 100, 100)
                st.markdown(f"""
                <div style='margin:6px 0;'>
                    <div style='font-size:10px; color:#64748b; margin-bottom:2px;'>Company</div>
                    <div style='background:rgba(255,255,255,0.05); border-radius:4px; height:10px;'>
                        <div style='width:{company_pct}%; background:{color}; height:10px; border-radius:4px;'></div>
                    </div>
                    <div style='font-size:10px; color:#64748b; margin-top:4px; margin-bottom:2px;'>Industry Avg</div>
                    <div style='background:rgba(255,255,255,0.05); border-radius:4px; height:10px;'>
                        <div style='width:{industry_pct}%; background:#6366f1; height:10px; border-radius:4px;'></div>
                    </div>
                </div>""", unsafe_allow_html=True)
            with col_vals:
                status = "✅" if better else "⚠️"
                st.markdown(f"""<div style='font-size:12px; text-align:right; padding-top:4px;'>
                    <div style='color:#e2e8f0; font-weight:700;'>{company_val}{unit} {status}</div>
                    <div style='color:#64748b;'>Avg: {industry_val}{unit}</div>
                </div>""", unsafe_allow_html=True)

        st.divider()

        # ── ADVANCED FINANCIAL RATIOS ──
        st.markdown("<div class='section-header' style='font-size:18px;'>🔢 Advanced Financial Ratios</div>", unsafe_allow_html=True)

        # Altman Z-Score
        working_capital = live.get("cash", 0) or 0
        retained_earnings = net_income
        ebit_val = live.get("ebit") or ebitda
        market_cap = live.get("market_cap") or 0
        sales = revenue

        if total_assets > 0:
            x1 = working_capital / total_assets
            x2 = retained_earnings / total_assets
            x3 = (ebit_val or 0) / total_assets
            x4 = market_cap / max(total_debt, 1)
            x5 = sales / total_assets
            z_score = round(1.2*x1 + 1.4*x2 + 3.3*x3 + 0.6*x4 + 1.0*x5, 2)
        else:
            z_score = 0

        z_label = "Safe Zone ✅" if z_score > 2.99 else "Grey Zone ⚠️" if z_score > 1.81 else "Distress Zone 🔴"
        z_color = "#10b981" if z_score > 2.99 else "#f59e0b" if z_score > 1.81 else "#ef4444"

        # Graham Number
        eps = net_income / 100 if net_income else 0
        bvps = equity / 100 if equity else 0
        graham = round((22.5 * max(eps, 0) * max(bvps, 0)) ** 0.5, 2) if eps > 0 and bvps > 0 else 0
        current_price = live.get("current_price") or 0
        graham_signal = "Undervalued ✅" if graham > current_price > 0 else "Overvalued ⚠️" if current_price > 0 else "N/A"
        graham_color = "#10b981" if graham > current_price > 0 else "#ef4444"

        # More ratios
        asset_turnover = round(revenue / total_assets, 2) if total_assets else 0
        debt_to_assets = round(total_debt / total_assets, 2) if total_assets else 0
        equity_multiplier = round(total_assets / max(equity, 1), 2)
        cash_ratio = round((live.get("cash") or 0) / max(total_debt * 0.3, 1), 2)
        roce = round((ebit_val or 0) / max(total_assets - total_debt, 1) * 100, 2) if total_assets else 0

        # Display ratios
        r1, r2, r3 = st.columns(3)

        with r1:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>Altman Z-Score</div>
                <div style='font-size:28px; font-weight:800; color:{z_color};'>{z_score}</div>
                <div style='font-size:12px; color:{z_color}; margin-top:4px;'>{z_label}</div>
                <div style='font-size:11px; color:#64748b; margin-top:8px;'>
                    &gt;2.99 Safe | 1.81-2.99 Grey | &lt;1.81 Distress
                </div>
            </div>""", unsafe_allow_html=True)

        with r2:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>Graham Number</div>
                <div style='font-size:28px; font-weight:800; color:{graham_color};'>₹{graham:,.0f}</div>
                <div style='font-size:12px; color:{graham_color}; margin-top:4px;'>{graham_signal}</div>
                <div style='font-size:11px; color:#64748b; margin-top:8px;'>
                    Current Price: ₹{current_price:,.0f}
                </div>
            </div>""", unsafe_allow_html=True)

        with r3:
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>ROCE</div>
                <div style='font-size:28px; font-weight:800; color:#8b5cf6;'>{roce}%</div>
                <div style='font-size:12px; color:#64748b; margin-top:4px;'>Return on Capital Employed</div>
                <div style='font-size:11px; color:#64748b; margin-top:8px;'>
                    Industry Avg ROE: {benchmark['avg_roe']}%
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
  
        # New ratios
        ev = (market_cap + total_debt - (live.get("cash") or 0))
        ev_ebitda = round(ev / max(ebitda, 1), 2) if ebitda and ebitda > 0 else 0
        interest_expense = total_debt * 0.08
        interest_coverage = round((ebit_val or 0) / max(interest_expense, 1), 2)
        working_capital = (live.get("cash") or 0) - (total_debt * 0.3)
        working_capital_ratio = round((live.get("cash") or 0) / max(total_debt * 0.3, 1), 2)
        earnings_yield = round(1 / max(company_pe, 0.1) * 100, 2) if company_pe else 0

        r4, r5, r6, r7 = st.columns(4)

        extra_ratios = [
            (r4, "EV/EBITDA", f"{ev_ebitda}x", "#06b6d4", "Enterprise value multiple — lower is cheaper"),
            (r5, "Interest Coverage", f"{interest_coverage}x", "#10b981" if interest_coverage > 3 else "#ef4444", "Ability to pay interest — >3x is safe"),
            (r6, "Working Capital Ratio", f"{working_capital_ratio}x", "#8b5cf6", "Short-term liquidity health"),
            (r7, "Earnings Yield", f"{earnings_yield}%", "#f59e0b", "Return on investment vs price"),
        ] 

        for col, label, val, color, desc in extra_ratios:
            with col:
                st.markdown(f"""<div class='kpi-card' style='text-align:center;'>
                    <div class='kpi-label'>{label}</div>
                    <div style='font-size:22px; font-weight:800; color:{color};'>{val}</div>
                    <div style='font-size:10px; color:#64748b; margin-top:6px;'>{desc}</div>
                </div>""", unsafe_allow_html=True)

        st.divider()

        # Benchmark radar chart
        st.markdown("<div class='section-header' style='font-size:18px;'>🕸️ Company vs Industry Radar</div>", unsafe_allow_html=True)

        company_scores = {
            "Profitability": min(100, company_ebitda_margin / benchmark["avg_ebitda_margin"] * 50) if benchmark["avg_ebitda_margin"] else 50,
            "Valuation": min(100, max(0, 100 - (company_pe / max(benchmark["avg_pe"], 1) * 50))) if company_pe else 50,
            "Returns": min(100, company_roe / max(benchmark["avg_roe"], 1) * 50) if company_roe else 50,
            "Leverage": min(100, max(0, 100 - (company_de / max(benchmark["avg_debt_equity"], 0.1) * 50))),
            "Z-Score": min(100, z_score / 3 * 100),
        }

        industry_scores = {
            "Profitability": 50,
            "Valuation": 50,
            "Returns": 50,
            "Leverage": 50,
            "Z-Score": 50,
        }

        categories = list(company_scores.keys())
        comp_vals = list(company_scores.values()) + [list(company_scores.values())[0]]
        ind_vals = list(industry_scores.values()) + [list(industry_scores.values())[0]]
        categories_closed = categories + [categories[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=comp_vals, theta=categories_closed,
            fill='toself', fillcolor="rgba(99,102,241,0.2)",
            line=dict(color=COLORS["blue"], width=2),
            name=selected_company,
        ))
        fig.add_trace(go.Scatterpolar(
            r=ind_vals, theta=categories_closed,
            fill='toself', fillcolor="rgba(16,185,129,0.1)",
            line=dict(color=COLORS["green"], width=2, dash="dash"),
            name="Industry Average",
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="rgba(255,255,255,0.02)",
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.06)"),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94a3b8")),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8"),
            height=400,
            showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Top companies in industry
        st.markdown(f"<div class='info-box'>🏆 <strong>Top companies in {industry}:</strong> {', '.join(benchmark['top_companies'])}</div>", unsafe_allow_html=True)

    else:
        st.markdown("<div class='warning-box'>⚠️ No live data available.</div>", unsafe_allow_html=True)