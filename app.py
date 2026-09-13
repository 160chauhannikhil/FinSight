import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import anthropic
import pandas as pd
import numpy as np
import os
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CrisisIQ — Financial Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Full Redesign
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* Animated gradient background */
    .stApp {
        background: linear-gradient(135deg, #060818 0%, #0a0f2e 25%, #0d1a1a 50%, #0a0f2e 75%, #060818 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: #e2e8f0;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080d20 0%, #0a1628 100%) !important;
        border-right: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 4px 0 24px rgba(0,0,0,0.4);
    }

    /* Glass morphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15), inset 0 1px 0 rgba(255,255,255,0.05);
        transform: translateY(-2px);
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.08) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
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

    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.2);
    }

    .kpi-label {
        font-size: 10px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }

    .kpi-value-green {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .kpi-value-amber {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(135deg, #f59e0b, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .kpi-value-red {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(135deg, #ef4444, #dc2626);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Live badge */
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 600;
        color: #10b981;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        50% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    }

    /* Section header */
    .section-header {
        font-size: 24px;
        font-weight: 800;
        color: #f1f5f9;
        margin: 28px 0 8px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .section-subheader {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 20px;
    }

    /* Agent cards */
    .agent-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(139,92,246,0.04) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        position: relative;
        overflow: hidden;
    }

    .agent-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
    }

    .agent-name {
        font-size: 12px;
        font-weight: 700;
        color: #6366f1;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 10px;
    }

    .agent-text {
        font-size: 13px;
        color: #cbd5e1;
        line-height: 1.7;
    }

    /* Success/Warning boxes */
    .success-box {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 10px;
        padding: 14px 18px;
        color: #10b981;
        font-size: 13px;
        font-weight: 500;
    }

    .warning-box {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 10px;
        padding: 14px 18px;
        color: #ef4444;
        font-size: 13px;
        font-weight: 500;
    }

    .info-box {
        background: rgba(6, 182, 212, 0.08);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 10px;
        padding: 14px 18px;
        color: #06b6d4;
        font-size: 13px;
        font-weight: 500;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 700;
        font-size: 13px;
        transition: all 0.3s ease;
        letter-spacing: 0.03em;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        padding: 4px;
        border: 1px solid rgba(255,255,255,0.06);
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #64748b;
        border-radius: 8px;
        font-weight: 500;
        font-size: 13px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.2));
        color: #a5b4fc;
        border: 1px solid rgba(99,102,241,0.4);
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 16px;
    }

    [data-testid="metric-container"] label {
        color: #64748b !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    [data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }

    /* Selectbox */
    .stSelectbox label {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    /* Slider */
    .stSlider label {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }

    /* Dataframe */
    .stDataFrame {
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.06); }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #060818; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(#6366f1, #8b5cf6); border-radius: 3px; }

    /* Radio buttons */
    .stRadio label { color: #94a3b8 !important; font-size: 13px !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: #94a3b8 !important; }

    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label { color: #94a3b8; }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
        border-radius: 4px;
    }

    /* Spinner */
    .stSpinner > div { border-top-color: #6366f1 !important; }

    /* Caption */
    .stCaption { color: #475569 !important; }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 10px !important;
        color: #94a3b8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD NIFTY 500
# ─────────────────────────────────────────────
@st.cache_data
def load_nifty500():
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nifty500.csv")
    df = pd.read_csv(csv_path)
    companies = {}
    for _, row in df.iterrows():
        name = str(row["Company Name"]).strip()
        symbol = str(row["Symbol"]).strip()
        industry = str(row["Industry"]).strip()
        companies[name] = {
            "ticker": f"{symbol}.NS",
            "industry": industry,
            "description": f"{industry} company listed on NSE"
        }
    return companies

COMPANIES = load_nifty500()

# ─────────────────────────────────────────────
# LIVE DATA FETCH
# ─────────────────────────────────────────────
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
                    val = df.loc[key].iloc[0]
                    return safe(val)
            return None

        return {
            "revenue": get_row(fin, "Total Revenue"),
            "gross_profit": get_row(fin, "Gross Profit"),
            "ebitda": get_row(fin, "EBITDA"),
            "ebit": get_row(fin, "EBIT", "Operating Income"),
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
            "roce": round((info.get("returnOnAssets", 0) or 0) * 100, 2),
        }
    except Exception as e:
        return None

# ─────────────────────────────────────────────
# FINANCIAL ENGINE
# ─────────────────────────────────────────────
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
    net_margin = (stressed_net / stressed_revenue * 100) if stressed_revenue else 0
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
        "revenue": stressed_revenue,
        "gross_profit": stressed_gross,
        "ebitda": stressed_ebitda,
        "net_income": stressed_net,
        "total_debt": stressed_debt,
        "cash": stressed_cash,
        "ebitda_margin": ebitda_margin,
        "net_margin": net_margin,
        "debt_to_equity": debt_to_equity,
        "current_ratio": current_ratio,
        "interest_coverage": interest_coverage,
        "resilience": resilience,
        "total_assets": total_assets,
    }

# ─────────────────────────────────────────────
# CHART THEME
# ─────────────────────────────────────────────
CHART_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#94a3b8", family="Inter, sans-serif", size=12),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.08)", tickfont=dict(color="#64748b")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.08)", tickfont=dict(color="#64748b")),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8")),
)

COLORS = {
    "blue": "#6366f1",
    "purple": "#8b5cf6",
    "cyan": "#06b6d4",
    "green": "#10b981",
    "amber": "#f59e0b",
    "red": "#ef4444",
    "pink": "#ec4899",
}

def pl_chart(data, title="P&L Overview"):
    labels = ["Revenue", "Gross Profit", "EBITDA", "Net Income"]
    values = [data.get("revenue") or 0, data.get("gross_profit") or 0,
              data.get("ebitda") or 0, data.get("net_income") or 0]
    colors = [COLORS["blue"], COLORS["cyan"], COLORS["green"], COLORS["purple"]]

    fig = go.Figure()
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        fig.add_trace(go.Bar(
            x=[label], y=[value],
            marker=dict(
                color=color,
                opacity=0.85,
                line=dict(color=color, width=1),
            ),
            text=[f"₹{value:,.0f} Cr"],
            textposition="outside",
            textfont=dict(color="#e2e8f0", size=11, family="Inter"),
            name=label,
            showlegend=False,
        ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color="#e2e8f0", family="Inter"), x=0),
        barmode="group",
        height=320,
        **CHART_THEME
    )
    return fig

def resilience_gauge(score):
    if score >= 70:
        color = COLORS["green"]
        gradient = [[0, "#10b981"], [1, "#06b6d4"]]
    elif score >= 40:
        color = COLORS["amber"]
        gradient = [[0, "#f59e0b"], [1, "#ef4444"]]
    else:
        color = COLORS["red"]
        gradient = [[0, "#ef4444"], [1, "#dc2626"]]

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        number=dict(font=dict(size=40, color=color, family="Inter"), suffix="/100"),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#475569", tickfont=dict(color="#475569")),
            bar=dict(color=color, thickness=0.25),
            bgcolor="rgba(255,255,255,0.02)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            steps=[
                dict(range=[0, 40], color="rgba(239,68,68,0.1)"),
                dict(range=[40, 70], color="rgba(245,158,11,0.1)"),
                dict(range=[70, 100], color="rgba(16,185,129,0.1)"),
            ],
        ),
        domain=dict(x=[0, 1], y=[0, 1])
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0", family="Inter"),
        height=240,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig

def comparison_chart(baseline, stressed, metrics, labels):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Baseline",
        x=labels,
        y=[baseline.get(m, 0) for m in metrics],
        marker=dict(color=COLORS["blue"], opacity=0.8, line=dict(color=COLORS["blue"], width=1)),
        text=[f"₹{baseline.get(m,0):,.0f}" for m in metrics],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=10),
    ))
    fig.add_trace(go.Bar(
        name="Stressed",
        x=labels,
        y=[stressed.get(m, 0) for m in metrics],
        marker=dict(color=COLORS["red"], opacity=0.8, line=dict(color=COLORS["red"], width=1)),
        text=[f"₹{stressed.get(m,0):,.0f}" for m in metrics],
        textposition="outside",
        textfont=dict(color="#94a3b8", size=10),
    ))
    fig.update_layout(
        barmode="group",
        title=dict(text="Baseline vs Stressed Scenario", font=dict(size=14, color="#e2e8f0")),
        height=350,
        **CHART_THEME
    )
    return fig

def radar_chart(metrics_dict, title="Financial Profile"):
    categories = list(metrics_dict.keys())
    values = list(metrics_dict.values())
    values += values[:1]
    categories += categories[:1]

    fig = go.Figure(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor="rgba(99,102,241,0.15)",
        line=dict(color=COLORS["blue"], width=2),
        marker=dict(color=COLORS["blue"], size=6),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.02)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#475569")),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickfont=dict(color="#94a3b8")),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", family="Inter"),
        title=dict(text=title, font=dict(size=14, color="#e2e8f0")),
        height=300,
        margin=dict(l=40, r=40, t=50, b=40),
        showlegend=False,
    )
    return fig

# ─────────────────────────────────────────────
# AI SERVICE
# ─────────────────────────────────────────────
def call_claude(prompt, system="You are a senior financial analyst. Be concise, insightful, and use bullet points."):
    try:
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=800,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"⚠️ AI unavailable: {str(e)}"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 16px;'>
        <div style='font-size:36px; margin-bottom:8px;'>⚡</div>
        <div style='font-size:20px; font-weight:800; background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;'>CrisisIQ</div>
        <div style='font-size:11px; color:#475569; margin-top:4px; font-weight:500; letter-spacing:0.08em; text-transform:uppercase;'>Financial Intelligence Platform</div>
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
        popular = ["Infosys Ltd", "Reliance Industries Ltd", "HDFC Bank Ltd", "Tata Consultancy Services Ltd", "Wipro Ltd"]
        available_popular = [p for p in popular if p in COMPANIES]
        selected_company = st.selectbox("Popular Companies", available_popular if available_popular else list(COMPANIES.keys())[:10])

    company_info = COMPANIES.get(selected_company, {"ticker": "", "industry": "N/A", "description": "N/A"})

    st.markdown(f"""
    <div style='background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.2); border-radius:10px; padding:14px; margin:10px 0;'>
        <div style='font-size:10px; color:#6366f1; font-weight:700; text-transform:uppercase; letter-spacing:0.1em;'>Industry</div>
        <div style='font-size:14px; color:#e2e8f0; font-weight:600; margin-top:4px;'>{company_info['industry']}</div>
        <div style='font-size:11px; color:#64748b; margin-top:6px;'>{company_info['ticker']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio("", [
        "📊 Dashboard",
        "⚡ Crisis Simulator",
        "🧪 Resilience Lab",
        "🤖 AI Boardroom",
        "🔄 Counterfactual",
        "🏢 Company Compare",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown("""
    <div style='font-size:10px; color:#334155; text-align:center; line-height:1.6;'>
        Powered by Yahoo Finance + Claude AI<br>
        Not financial advice
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FETCH LIVE DATA
# ─────────────────────────────────────────────
ticker = company_info["ticker"]
with st.spinner(f"⚡ Loading live data for {selected_company}..."):
    live = fetch_live_data(ticker) if ticker else None

# ─────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────
if page == "📊 Dashboard":
    col_title, col_badge = st.columns([3, 1])
    with col_title:
        st.markdown(f"<div class='section-header'>📊 {selected_company}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='section-subheader'>{company_info['industry']} • {company_info['ticker']} • {company_info['description']}</div>", unsafe_allow_html=True)
    with col_badge:
        st.markdown("<br>", unsafe_allow_html=True)
        if live:
            st.markdown("<div class='live-badge'>🟢 LIVE DATA</div>", unsafe_allow_html=True)

    if live:
        c1, c2, c3, c4 = st.columns(4)
        kpis = [
            (c1, "Revenue", live.get('revenue'), "kpi-value", "₹", " Cr"),
            (c2, "EBITDA", live.get('ebitda'), "kpi-value-green", "₹", " Cr"),
            (c3, "Market Cap", live.get('market_cap'), "kpi-value-amber", "₹", " Cr"),
            (c4, "P/E Ratio", live.get('pe_ratio'), "kpi-value-red", "", "x"),
        ]
        for col, label, value, cls, prefix, suffix in kpis:
            with col:
                if value:
                    formatted = f"{prefix}{value:,.1f}{suffix}"
                else:
                    formatted = "N/A"
                st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>{label}</div>
                    <div class='{cls}'>{formatted}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_pl, col_radar, col_gauge = st.columns([2, 1.5, 1])
        with col_pl:
            st.plotly_chart(pl_chart(live), use_container_width=True)

        with col_radar:
            baseline = apply_shocks(live, {})
            radar_data = {
                "Profitability": min(100, max(0, (live.get('net_income', 0) or 0) / (live.get('revenue', 1) or 1) * 300)),
                "Liquidity": min(100, baseline["current_ratio"] * 30),
                "Leverage": min(100, max(0, 100 - baseline["debt_to_equity"] * 20)),
                "Cash Flow": min(100, (live.get('cash', 0) or 0) / (live.get('revenue', 1) or 1) * 200),
                "Efficiency": min(100, (live.get('ebitda', 0) or 0) / (live.get('revenue', 1) or 1) * 300),
            }
            st.plotly_chart(radar_chart(radar_data, "Financial Profile"), use_container_width=True)

        with col_gauge:
            st.markdown("<div style='text-align:center; font-size:11px; color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;'>Resilience Score</div>", unsafe_allow_html=True)
            st.plotly_chart(resilience_gauge(baseline["resilience"]), use_container_width=True)
            label = "Resilient ✅" if baseline["resilience"] >= 70 else "Moderate ⚠️" if baseline["resilience"] >= 40 else "Vulnerable 🔴"
            color = "#10b981" if baseline["resilience"] >= 70 else "#f59e0b" if baseline["resilience"] >= 40 else "#ef4444"
            st.markdown(f"<div style='text-align:center; font-size:15px; font-weight:700; color:{color};'>{label}</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("<div class='section-header' style='font-size:18px;'>📈 Key Metrics</div>", unsafe_allow_html=True)

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        extra_metrics = [
            (m1, "Net Margin", f"{live['net_income']/live['revenue']*100:.1f}%" if live.get('net_income') and live.get('revenue') else "N/A", COLORS["blue"]),
            (m2, "ROE", f"{live.get('roe', 0):.1f}%", COLORS["purple"]),
            (m3, "P/B Ratio", f"{live.get('pb_ratio', 'N/A')}x", COLORS["cyan"]),
            (m4, "52W High", f"₹{live['52w_high']:,.0f}" if live.get('52w_high') else "N/A", COLORS["green"]),
            (m5, "52W Low", f"₹{live['52w_low']:,.0f}" if live.get('52w_low') else "N/A", COLORS["amber"]),
            (m6, "Div Yield", f"{live.get('dividend_yield', 0):.1f}%", COLORS["pink"]),
        ]
        for col, label, val, color in extra_metrics:
            with col:
                st.markdown(f"""
                <div class='kpi-card' style='text-align:center; padding:16px;'>
                    <div class='kpi-label'>{label}</div>
                    <div style='font-size:18px; font-weight:700; color:{color}; margin-top:6px;'>{val}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<div class='warning-box'>⚠️ Could not fetch live data for this company. Try searching for another company.</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: CRISIS SIMULATOR
# ─────────────────────────────────────────────
   
   elif page == "⚡ Crisis Simulator":
    st.markdown("<div class='section-header'>⚡ Crisis Simulator</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>Apply financial shocks and see real-time impact on company health</div>", unsafe_allow_html=True)

    col_sliders, col_results = st.columns([1, 2])

    with col_sliders:
        st.markdown("**🎚️ Shock Parameters**")
        rev_shock = st.slider("Revenue Shock (%)", -60, 20, 0, 1, key="rev")
        cost_shock = st.slider("Cost Increase (%)", 0, 50, 0, 1, key="cost")
        interest_shock = st.slider("Interest Rate Shock (%)", 0, 100, 0, 5, key="interest")
        debt_shock = st.slider("Debt Increase (%)", 0, 100, 0, 5, key="debt")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**📋 Industry Templates**")
        template = st.selectbox("Apply Template", ["None", "IT Slowdown", "Banking NPA Crisis", "Commodity Crash", "Pandemic Shock", "Rate Hike Cycle"])
        if template == "IT Slowdown": rev_shock, cost_shock = -20, 10
        elif template == "Banking NPA Crisis": rev_shock, cost_shock, debt_shock = -15, 20, 30
        elif template == "Commodity Crash": rev_shock, cost_shock = -35, 25
        elif template == "Pandemic Shock": rev_shock, cost_shock, interest_shock = -40, 30, 20
        elif template == "Rate Hike Cycle": interest_shock, debt_shock = 50, 20

    shocks = {"revenue": rev_shock, "cost": cost_shock, "interest": interest_shock, "debt": debt_shock}

    if live:
        baseline = apply_shocks(live, {})
        stressed = apply_shocks(live, shocks)

        with col_results:
            s1, s2, s3, s4 = st.columns(4)
            delta_rev = stressed["revenue"] - baseline["revenue"]
            delta_ebitda = stressed["ebitda"] - baseline["ebitda"]
            delta_res = stressed["resilience"] - baseline["resilience"]
            delta_cash = stressed["cash"] - baseline["cash"]

            with s1: st.metric("Revenue", f"₹{stressed['revenue']:,.0f}Cr", f"{delta_rev:+.0f}Cr")
            with s2: st.metric("EBITDA", f"₹{stressed['ebitda']:,.0f}Cr", f"{delta_ebitda:+.0f}Cr")
            with s3: st.metric("Resilience", f"{stressed['resilience']:.0f}/100", f"{delta_res:+.0f}pts")
            with s4: st.metric("Cash", f"₹{stressed['cash']:,.0f}Cr", f"{delta_cash:+.0f}Cr")

            st.plotly_chart(
                comparison_chart(baseline, stressed,
                    ["revenue", "gross_profit", "ebitda", "net_income"],
                    ["Revenue", "Gross Profit", "EBITDA", "Net Income"]),
                use_container_width=True
            )

            severity = "🔴 Critical" if delta_res < -30 else "🟠 High" if delta_res < -15 else "🟡 Moderate" if delta_res < -5 else "🟢 Low"
            color = "#ef4444" if delta_res < -30 else "#f59e0b" if delta_res < -15 else "#fbbf24" if delta_res < -5 else "#10b981"
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Crisis Severity Assessment</div>
                <div style='font-size:22px; font-weight:800; color:{color}; margin:8px 0;'>{severity}</div>
                <div style='font-size:12px; color:#64748b;'>Resilience changed by {delta_res:+.1f} points under this scenario</div>
            </div>""", unsafe_allow_html=True)

elif page == "🧪 Resilience Lab":
# ─────────────────────────────────────────────
# PAGE: RESILIENCE LAB
# ─────────────────────────────────────────────
elif page == "🧪 Resilience Lab":
    st.markdown("<div class='section-header'>🧪 Resilience Lab</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>Test management interventions and find the best recovery strategy</div>", unsafe_allow_html=True)

    if live:
        baseline = apply_shocks(live, {})
        interventions = {
            "Cost Cutting (10%)": {"cost": -10},
            "Working Capital Optimization": {"revenue": 5},
            "Debt Restructuring": {"debt": -20, "interest": -15},
            "Revenue Diversification": {"revenue": 15},
            "Asset Monetization": {"debt": -30},
            "Emergency Equity Raise": {"debt": -40},
        }

        results = []
        for name, shock in interventions.items():
            result = apply_shocks(live, shock)
            improvement = result["resilience"] - baseline["resilience"]
            results.append({
                "Intervention": name,
                "Resilience": round(result["resilience"], 1),
                "Improvement": round(improvement, 1),
                "EBITDA (₹Cr)": round(result["ebitda"], 0),
                "Net Income (₹Cr)": round(result["net_income"], 0),
            })

        df = pd.DataFrame(results).sort_values("Resilience", ascending=False)

        col_table, col_chart = st.columns([1, 1])
        with col_table:
            st.markdown("**📋 Intervention Results**")
            st.dataframe(
                df.style.background_gradient(subset=["Resilience"], cmap="RdYlGn")
                        .background_gradient(subset=["Improvement"], cmap="RdYlGn"),
                use_container_width=True,
                hide_index=True
            )

        with col_chart:
            fig = go.Figure(go.Bar(
                y=df["Intervention"],
                x=df["Resilience"],
                orientation="h",
                marker=dict(
                    color=df["Resilience"].tolist(),
                    colorscale=[[0, COLORS["red"]], [0.5, COLORS["amber"]], [1, COLORS["green"]]],
                    cmin=0, cmax=100,
                    line=dict(width=0),
                ),
                text=[f"{v:.1f}" for v in df["Resilience"]],
                textposition="outside",
                textfont=dict(color="#e2e8f0", size=11),
            ))
            fig.update_layout(title="Resilience Score by Intervention", height=350, **CHART_THEME)
            st.plotly_chart(fig, use_container_width=True)

        best = df.iloc[0]
        st.markdown(f"""<div class='success-box'>
            🏆 <strong>Best Strategy:</strong> {best['Intervention']} → Score: {best['Resilience']}/100 (Improvement: +{best['Improvement']:.1f} pts)
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: AI BOARDROOM
# ─────────────────────────────────────────────
elif page == "🤖 AI Boardroom":
    st.markdown("<div class='section-header'>🤖 AI Boardroom</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>6 AI agents analyze, debate, and recommend the best strategy</div>", unsafe_allow_html=True)

    if live:
        baseline = apply_shocks(live, {})
        context = f"""
        Company: {selected_company} | Industry: {company_info['industry']}
        Revenue: ₹{live.get('revenue', 'N/A'):,} Cr | EBITDA: ₹{live.get('ebitda', 'N/A')} Cr
        Net Income: ₹{live.get('net_income', 'N/A')} Cr | Total Debt: ₹{live.get('total_debt', 'N/A')} Cr
        Cash: ₹{live.get('cash', 'N/A')} Cr | Market Cap: ₹{live.get('market_cap', 'N/A')} Cr
        P/E: {live.get('pe_ratio', 'N/A')}x | ROE: {live.get('roe', 'N/A')}% | Resilience: {baseline['resilience']:.0f}/100
        """

        agents = [
            ("💼 CFO Agent", "You are the CFO. Analyze financial health, cash flow risks, and capital structure in 4 bullet points.", COLORS["blue"]),
            ("⚠️ Risk Agent", "You are the CRO. Identify the top 4 financial risks and threats this company faces.", COLORS["red"]),
            ("🎯 Strategy Agent", "You are the CSO. Recommend 4 strategic responses to strengthen this company.", COLORS["purple"]),
            ("🏦 Treasury Agent", "You are the Treasurer. Focus on liquidity, debt management, and cash optimization in 4 points.", COLORS["cyan"]),
            ("🔴 Challenger Agent", "You are the Devil's Advocate. Find 4 critical flaws or blind spots in the current strategy.", COLORS["amber"]),
            ("👑 CEO Decision", "You are the CEO. Synthesize all perspectives and give a final 4-point action plan.", COLORS["green"]),
        ]

        if st.button("🚀 Start Boardroom Session", type="primary"):
            for agent_name, system, color in agents:
                with st.expander(agent_name, expanded=True):
                    with st.spinner(f"Analyzing..."):
                        response = call_claude(
                            f"Analyze this company and give your expert perspective:\n{context}",
                            system
                        )
                    st.markdown(f"""
                    <div class='agent-card'>
                        <div class='agent-name' style='color:{color};'>{agent_name}</div>
                        <div class='agent-text'>{response}</div>
                    </div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown("**⚖️ Human Decision**")
        col_dec, col_btn = st.columns([2, 1])
        with col_dec:
            decision = st.radio("Your Decision", [
                "✅ Approve AI Recommendation",
                "❌ Reject and Override",
                "🔄 Request More Analysis"
            ])
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Submit Decision"):
                st.markdown(f"<div class='success-box'>✅ Decision recorded: {decision}</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: COUNTERFACTUAL
# ─────────────────────────────────────────────
elif page == "🔄 Counterfactual":
    st.markdown("<div class='section-header'>🔄 Counterfactual Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>Compare alternative strategies side by side</div>", unsafe_allow_html=True)

    if live:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("**Strategy A — Conservative**")
            s1_rev = st.slider("Revenue Shock A (%)", -50, 20, -10, key="s1r")
            s1_cost = st.slider("Cost Change A (%)", -20, 50, 5, key="s1c")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("**Strategy B — Aggressive**")
            s2_rev = st.slider("Revenue Shock B (%)", -50, 20, 5, key="s2r")
            s2_cost = st.slider("Cost Change B (%)", -20, 50, 15, key="s2c")
            st.markdown("</div>", unsafe_allow_html=True)

        strat_a = apply_shocks(live, {"revenue": s1_rev, "cost": s1_cost})
        strat_b = apply_shocks(live, {"revenue": s2_rev, "cost": s2_cost})

        ca, cb = st.columns(2)
        with ca:
            color_a = "#10b981" if strat_a["resilience"] >= 70 else "#f59e0b" if strat_a["resilience"] >= 40 else "#ef4444"
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>Strategy A — Resilience</div>
                <div style='font-size:32px; font-weight:800; color:{color_a};'>{strat_a["resilience"]:.0f}/100</div>
                <div style='font-size:12px; color:#64748b; margin-top:6px;'>EBITDA: ₹{strat_a["ebitda"]:,.0f} Cr</div>
            </div>""", unsafe_allow_html=True)
        with cb:
            color_b = "#10b981" if strat_b["resilience"] >= 70 else "#f59e0b" if strat_b["resilience"] >= 40 else "#ef4444"
            st.markdown(f"""<div class='kpi-card'>
                <div class='kpi-label'>Strategy B — Resilience</div>
                <div style='font-size:32px; font-weight:800; color:{color_b};'>{strat_b["resilience"]:.0f}/100</div>
                <div style='font-size:12px; color:#64748b; margin-top:6px;'>EBITDA: ₹{strat_b["ebitda"]:,.0f} Cr</div>
            </div>""", unsafe_allow_html=True)

        fig = go.Figure()
        metrics = ["revenue", "ebitda", "net_income", "cash"]
        labels = ["Revenue", "EBITDA", "Net Income", "Cash"]
        fig.add_trace(go.Bar(name="Strategy A", x=labels, y=[strat_a.get(m,0) for m in metrics],
            marker=dict(color=COLORS["blue"], opacity=0.85), text=[f"₹{strat_a.get(m,0):,.0f}" for m in metrics], textposition="outside"))
        fig.add_trace(go.Bar(name="Strategy B", x=labels, y=[strat_b.get(m,0) for m in metrics],
            marker=dict(color=COLORS["green"], opacity=0.85), text=[f"₹{strat_b.get(m,0):,.0f}" for m in metrics], textposition="outside"))
        fig.update_layout(barmode="group", title="Strategy A vs Strategy B", height=350, **CHART_THEME)
        st.plotly_chart(fig, use_container_width=True)

        if st.button("🤖 Get AI Analysis"):
            with st.spinner("AI analyzing strategies..."):
                prompt = f"""Compare these two strategies for {selected_company}:
                Strategy A: Revenue {s1_rev}%, Cost {s1_cost}% → Resilience: {strat_a['resilience']:.0f}/100, EBITDA: ₹{strat_a['ebitda']:,.0f} Cr
                Strategy B: Revenue {s2_rev}%, Cost {s2_cost}% → Resilience: {strat_b['resilience']:.0f}/100, EBITDA: ₹{strat_b['ebitda']:,.0f} Cr
                Which is better and why? Give 4 key insights."""
                analysis = call_claude(prompt)
            st.markdown(f"""<div class='agent-card'>
                <div class='agent-name'>AI Strategic Analysis</div>
                <div class='agent-text'>{analysis}</div>
            </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE: COMPANY COMPARE
# ─────────────────────────────────────────────
elif page == "🏢 Company Compare":
    st.markdown("<div class='section-header'>🏢 Company Comparison</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-subheader'>Benchmark multiple Nifty 500 companies under the same crisis scenario</div>", unsafe_allow_html=True)

    selected_companies = st.multiselect(
        "Select Companies (max 6)",
        list(COMPANIES.keys()),
        default=list(COMPANIES.keys())[:4],
        max_selections=6
    )

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        comp_rev = st.slider("Shared Revenue Shock (%)", -50, 0, -20)
    with col_s2:
        comp_cost = st.slider("Shared Cost Increase (%)", 0, 50, 10)

    if st.button("📊 Run Comparison") and selected_companies:
        results = []
        progress = st.progress(0)
        status = st.empty()

        for i, company in enumerate(selected_companies):
            status.markdown(f"<div class='info-box'>⚡ Fetching data for {company}...</div>", unsafe_allow_html=True)
            ticker = COMPANIES[company]["ticker"]
            data = fetch_live_data(ticker)
            if data:
                stressed = apply_shocks(data, {"revenue": comp_rev, "cost": comp_cost})
                results.append({
                    "Company": company,
                    "Industry": COMPANIES[company]["industry"],
                    "Resilience": round(stressed["resilience"], 1),
                    "Revenue (₹Cr)": round(stressed["revenue"], 0),
                    "EBITDA (₹Cr)": round(stressed["ebitda"], 0),
                    "Net Income (₹Cr)": round(stressed["net_income"], 0),
                })
            progress.progress((i + 1) / len(selected_companies))

        status.empty()

        if results:
            df = pd.DataFrame(results).sort_values("Resilience", ascending=False)

            st.dataframe(
                df.style.background_gradient(subset=["Resilience"], cmap="RdYlGn"),
                use_container_width=True,
                hide_index=True
            )

            fig = go.Figure(go.Bar(
                x=df["Company"],
                y=df["Resilience"],
                marker=dict(
                    color=df["Resilience"].tolist(),
                    colorscale=[[0, COLORS["red"]], [0.4, COLORS["amber"]], [1, COLORS["green"]]],
                    cmin=0, cmax=100,
                    showscale=True,
                    colorbar=dict(title="Score", tickfont=dict(color="#94a3b8")),
                ),
                text=[f"{v:.0f}" for v in df["Resilience"]],
                textposition="outside",
                textfont=dict(color="#e2e8f0", size=12),
            ))
            fig.update_layout(
                title=f"Resilience Ranking — {comp_rev}% Revenue Shock, +{comp_cost}% Cost",
                height=400,
                **CHART_THEME
            )
            st.plotly_chart(fig, use_container_width=True)

            winner = df.iloc[0]
            loser = df.iloc[-1]
            st.markdown(f"""<div class='success-box'>
                🏆 <strong>Most Resilient:</strong> {winner['Company']} — Score {winner['Resilience']}/100
            </div>""", unsafe_allow_html=True)
            st.markdown(f"""<div class='warning-box'>
                ⚠️ <strong>Most Vulnerable:</strong> {loser['Company']} — Score {loser['Resilience']}/100
            </div>""", unsafe_allow_html=True)