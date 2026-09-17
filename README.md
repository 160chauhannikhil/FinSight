# ⚡ FinSight — AI-Powered Financial Intelligence Platform
### *by Nikhil Singh*

> **"Democratizing professional financial intelligence — what cost ₹50 lakhs and 2 weeks now takes 30 seconds and costs nothing."**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Yahoo Finance](https://img.shields.io/badge/Data-Yahoo%20Finance-purple?style=flat-square)](https://finance.yahoo.com)
[![Claude AI](https://img.shields.io/badge/AI-Claude%20Sonnet-orange?style=flat-square)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 🎯 Problem Statement

When a financial crisis hits a company — revenue crash, interest rate hike, market downturn — management has **no fast, intelligent tool** to understand the true impact and decide what to do next.

| Without FinSight | With FinSight |
|---|---|
| 3-5 days in Excel | 30 seconds |
| ₹50-100L consultant fees | Free |
| Outdated static data | Live NSE market data |
| 1 perspective | 6 AI expert agents |
| Manual benchmarking | Instant vs 500 companies |
| No stress testing | Real-time scenario simulation |

---

## 🚀 Live Demo

| Platform | URL | Status |
|---|---|---|
| **Streamlit Cloud** | [finsight-gjcwxba4rp6y2b49hgkghf.streamlit.app](https://finsight-gjcwxba4rp6y2b49hgkghf.streamlit.app) | 🟢 Live |
| **GitHub** | [github.com/160chauhannikhil/FinSight](https://github.com/160chauhannikhil/FinSight) | 🟢 Public |

---

## 📊 What FinSight Does

FinSight is a **real-time AI-powered financial stress testing platform** built for corporate management teams, equity analysts, MBA students, and financial consultants. It combines live market data, machine learning, and multi-agent AI to deliver professional-grade financial analysis in seconds.

### 8 Powerful Modules

---

### 1. 📊 Executive Dashboard
Real-time financial snapshot of any Nifty 500 company.

**Features:**
- Live KPI cards: Revenue, EBITDA, Market Cap, P/E Ratio
- Interactive P&L bar chart (Revenue → Gross Profit → EBITDA → Net Income)
- Financial Profile radar chart across 5 dimensions (Profitability, Liquidity, Leverage, Cash Flow, Efficiency)
- Financial Resilience Gauge (0-100 score)
- Stock price history chart with 20-day and 50-day moving averages
- Trading volume chart with color-coded up/down days
- 6 additional metrics: Net Margin, ROE, P/B Ratio, 52-Week High/Low, Dividend Yield
- **Live Data** badge (green) or **Verified Data** badge (amber) to indicate data source

---

### 2. ⚡ Crisis Simulator
Apply financial stress scenarios and instantly see impact on company health.

**4 Stress Parameters:**
| Parameter | Range | What It Simulates |
|---|---|---|
| Revenue Stress | -60% to +20% | Demand crash, recession, competition |
| Cost Pressure | 0% to +50% | Inflation, supply chain, wage hikes |
| Interest Rate Stress | 0% to +100% | RBI rate hikes, refinancing risk |
| Debt Leverage Stress | 0% to +100% | Additional borrowing, credit crunch |

**6 Industry Crisis Templates:**
- IT Slowdown (2023 pattern)
- Banking NPA Crisis (Yes Bank pattern)
- Commodity Crash (Steel/Metal sector)
- Pandemic Shock (COVID-19 model)
- Rate Hike Cycle (RBI 2022-23)

**Output:** Stressed Revenue, EBITDA, Resilience Score, Cash — with crisis severity assessment (Critical/High/Moderate/Low)

---

### 3. 🧪 Resilience Lab
Test management interventions and find the optimal recovery strategy.

**6 Management Interventions Tested:**
| Intervention | What It Does |
|---|---|
| Cost Cutting (10%) | Reduces operational expenses |
| Working Capital Optimization | Improves receivables and inventory cycles |
| Debt Restructuring | Refinances debt at lower rates |
| Revenue Diversification | Enters new markets/product lines |
| Asset Monetization | Sells non-core assets to reduce debt |
| Emergency Equity Raise | Rights issue to strengthen balance sheet |

**Output:** Ranked comparison table with resilience scores, improvement points, EBITDA and Net Income for each intervention. Best strategy automatically identified.

---

### 4. 🤖 AI Boardroom
6 specialized AI agents analyze the company from different C-suite perspectives and debate the best strategy.

**6 AI Agents:**
| Agent | Role | Focus |
|---|---|---|
| 💼 CFO Agent | Chief Financial Officer | Cash flow, capital structure, liquidity |
| ⚠️ Risk Agent | Chief Risk Officer | Downside risks, credit risk, market risk |
| 🎯 Strategy Agent | Chief Strategy Officer | Growth opportunities, competitive positioning |
| 🏦 Treasury Agent | Treasurer | Debt management, hedging, cash optimization |
| 🔴 Challenger Agent | Devil's Advocate | Flaws in strategy, blind spots, assumptions |
| 👑 CEO Decision | Chief Executive Officer | Final synthesis and action plan |

**Human Decision:** After AI analysis, user approves/rejects/requests more analysis — embodying "AI analyzes, Human decides" framework.

**AI Model:** Claude claude-sonnet-4-6 (Anthropic) | Pre-written expert fallback when API unavailable

---

### 5. 🔄 Counterfactual Analysis
Compare two alternative management strategies side by side.

**Use Case:** "Should we cut costs aggressively (Strategy A) or invest in growth despite higher costs (Strategy B)?"

- Independent sliders for each strategy
- Side-by-side resilience scores and EBITDA comparison
- Grouped bar chart: Revenue, EBITDA, Net Income, Cash
- AI-powered analysis explaining which strategy is better and why

---

### 6. 🏢 Company Comparison
Benchmark up to 6 Nifty 500 companies under the same crisis scenario simultaneously.

- Multi-select from all 500 Nifty companies
- Shared stress scenario applied to all
- Resilience ranking with color-coded bar chart
- Most resilient and most vulnerable companies highlighted
- Progress tracking as each company's data is fetched

---

### 7. 🔮 Stock Price Prediction
ML-powered stock price forecast with news sentiment and technical analysis.

**Machine Learning Model:**
- Algorithm: Random Forest Regressor (100 decision trees)
- Training data: 2 years of daily OHLCV data
- Forecast periods: 1 Month, 3 Months, 6 Months
- Confidence interval shown (best case / worst case range)

**8 Technical Indicators (via `ta` library):**
| Indicator | Signal |
|---|---|
| RSI (14-day) | >70 Overbought, <30 Oversold |
| MACD (12/26/9) | Bullish/Bearish crossover |
| Bollinger Bands (20-day) | Price position relative to bands |
| EMA 20 & 50 | Short and medium-term trend |
| ATR (14-day) | Volatility measure |
| OBV | Volume confirms price trend |

**7 Candlestick Patterns Detected:**
Doji, Hammer, Shooting Star, Bullish Engulfing, Bearish Engulfing, Three White Soldiers, Three Black Crows

**News Sentiment Analysis:**
- Source: Google News RSS (free, no API key)
- Analyzes top 10 recent headlines
- Positive/negative keyword scoring
- Adjusts prediction by up to ±5%

**Overall Signal:** Combines all 6 signals (RSI, MACD, Bollinger, Trend, News, Candlestick) → Bullish/Bearish/Neutral

---

### 8. 📐 Benchmarks & Advanced Ratios
Compare company vs industry averages and calculate 15+ financial ratios.

**Industry Benchmarks (10 sectors):**
IT Services, Banking, Financial Services, FMCG, Automotive, Pharma, Manufacturing, Energy, Food Tech, Conglomerate

**Benchmark metrics:** EBITDA Margin, ROE, P/E Ratio, Debt/Equity — company vs industry average with visual bar comparison

**15+ Financial Ratios Calculated:**

| Ratio | Formula | Benchmark |
|---|---|---|
| Altman Z-Score | 1.2X1+1.4X2+3.3X3+0.6X4+1.0X5 | >2.99 Safe |
| Graham Number | √(22.5 × EPS × BVPS) | Buy below this |
| EV/EBITDA | (MCap+Debt-Cash)/EBITDA | <15x cheap |
| ROCE | EBIT/Capital Employed × 100 | >12% good |
| Interest Coverage | EBIT/Interest Expense | >3x safe |
| Working Capital Ratio | Current Assets/Current Liabilities | >1.5x |
| Earnings Yield | EPS/Price × 100 | >5% good |
| Asset Turnover | Revenue/Total Assets | >0.5x |
| Debt to Assets | Total Debt/Total Assets | <0.4x |
| Equity Multiplier | Total Assets/Equity | Lower safer |
| Net Margin | Net Income/Revenue × 100 | >10% |
| ROE | Net Income/Equity × 100 | >15% |
| P/E Ratio | Price/EPS | 15-25x fair |
| P/B Ratio | Price/Book Value | <3x |
| Dividend Yield | Annual Dividend/Price × 100 | Varies |

**Company vs Industry Radar Chart:** Visual comparison across 5 dimensions vs industry average

---

### 9. 📄 PDF Report Export
Generate a professional boardroom-ready PDF report in one click.

**Report Contents:**
- Executive Summary with KPI cards
- Full financial metrics table
- Advanced financial ratios with interpretation
- Industry benchmark comparison
- FinSight branding with date/time stamp

---

## 🏗️ Architecture & Tech Stack

```
┌─────────────────────────────────────────────────────────┐
│                    FinSight Platform                     │
├─────────────────┬───────────────────┬───────────────────┤
│   Data Layer    │   Analysis Layer  │   AI Layer        │
│                 │                   │                   │
│ Yahoo Finance   │ Financial Engine  │ Claude AI API     │
│ (Live NSE data) │ (25+ ratios)      │ (6 agents)        │
│                 │                   │                   │
│ Nifty500 CSV    │ ML Prediction     │ News Sentiment    │
│ (500 companies) │ (Random Forest)   │ (Google News)     │
│                 │                   │                   │
│ Fallback Data   │ Technical Analysis│ Pre-written       │
│ (15 companies)  │ (RSI,MACD,BB,ATR) │ Expert Fallback   │
├─────────────────┴───────────────────┴───────────────────┤
│              Streamlit Web Interface                     │
│         (8 modules, dark theme, Plotly charts)           │
└─────────────────────────────────────────────────────────┘
```

| Layer | Technology | Purpose |
|---|---|---|
| **UI Framework** | Streamlit | Web interface, all pages and charts |
| **Charts** | Plotly | Interactive bar, line, radar, gauge charts |
| **Live Data** | yfinance (Yahoo Finance) | Real financial data for 500 NSE companies |
| **ML Model** | Scikit-learn (Random Forest) | Stock price prediction |
| **Technical Analysis** | ta library | RSI, MACD, Bollinger Bands, EMA, ATR, OBV |
| **News Sentiment** | BeautifulSoup + Google News | Free news scraping and sentiment scoring |
| **AI Agents** | Anthropic Claude claude-sonnet-4-6 | 6-agent boardroom analysis |
| **PDF Export** | ReportLab | Professional PDF report generation |
| **Data Storage** | CSV + Python dict | Nifty 500 list + verified fallback data |
| **Deployment** | Streamlit Cloud / Render.com | Free public hosting |
| **Version Control** | GitHub | Code storage and CI/CD |

---

## 📈 Data Coverage

| Source | Coverage | Update Frequency |
|---|---|---|
| Yahoo Finance (live) | All 500 Nifty companies | Every 5 minutes (cached) |
| Verified Fallback Data | 15 major companies | FY2024 annual figures |
| Alpha Vantage API | Additional companies | On request |
| Google News RSS | All companies | Real-time |

**15 Companies with Verified FY2024 Data:**
Infosys, TCS, Reliance Industries, HDFC Bank, ICICI Bank, Axis Bank, SBI, Wipro, Maruti Suzuki, Sun Pharma, HUL, Asian Paints, Bajaj Finance, ONGC, Zomato

---

## 🚀 How to Run

### Option 1 — Run Locally (All 500 Companies, Full Features)

```bash
# Clone the repository
git clone https://github.com/160chauhannikhil/FinSight.git
cd FinSight

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_new.py

# Open browser
# http://localhost:8501
```

### Option 2 — Share Publicly with ngrok

```bash
# Start the app first
streamlit run app_new.py

# In a new terminal, start ngrok
ngrok http 8501

# Share the https://xyz.ngrok-free.app URL with anyone
```

### Option 3 — Access Online (15 Companies)

Visit: **https://finsight-gjcwxba4rp6y2b49hgkghf.streamlit.app**

No installation required.

---

## ⚙️ Environment Variables (Optional)

| Variable | Purpose | Required |
|---|---|---|
| `ANTHROPIC_API_KEY` | Enable AI Boardroom agents | Optional |
| `ALPHA_VANTAGE_KEY` | Additional data source | Optional |

```bash
# Set API key for AI Boardroom
export ANTHROPIC_API_KEY="your-key-here"  # Linux/Mac
set ANTHROPIC_API_KEY="your-key-here"     # Windows
```

---

## 📁 Project Structure

```
FinSight/
├── app_new.py          # Main application (8 modules, UI, logic)
├── predict.py          # ML prediction engine (Random Forest + technical analysis)
├── fallback_data.py    # Verified FY2024 data for 15 major companies
├── alpha_vantage.py    # Alpha Vantage API integration
├── export_pdf.py       # PDF report generator (ReportLab)
├── nifty500.csv        # Complete Nifty 500 company list (NSE)
├── requirements.txt    # Python dependencies
├── runtime.txt         # Python version specification
└── README.md           # This file
```

---

## 🎓 Academic & Professional Context

**Project Type:** MBA Capstone / Independent Research Project

**Author:** Nikhil Singh | MBA in Operations & Marketing

**Relevance to Industry:**
- **Financial Advisory (Big 4):** Stress testing framework mirrors Deloitte/PwC financial due diligence
- **Risk Management:** Altman Z-Score and resilience scoring used in credit risk assessment
- **Equity Research:** Live data + technical analysis + ML prediction for investment decisions
- **Corporate Finance:** Crisis simulation for CFO-level scenario planning
- **Consulting:** Industry benchmarking for M&A target analysis

**Real-World Crisis Applications:**
- COVID-19 (2020): Revenue drop modeling
- RBI Rate Hikes (2022-23): Interest rate stress testing
- Yes Bank Crisis (2020): Early warning via Z-Score
- Adani Group (2023): Leverage risk analysis
- IT Slowdown (2023): Sector comparison

---

## 📊 Key Metrics

| Metric | Value |
|---|---|
| Companies Covered | 500 (entire Nifty 500) |
| Financial Ratios Calculated | 15+ |
| AI Agents | 6 specialized agents |
| Stress Parameters | 4 (Revenue, Cost, Interest, Debt) |
| Industry Templates | 6 crisis scenarios |
| Management Interventions | 6 options tested |
| Technical Indicators | 8 (RSI, MACD, BB, EMA20, EMA50, EMA200, ATR, OBV) |
| Candlestick Patterns | 7 detected automatically |
| Lines of Code | ~1,500+ |
| Modules | 8 pages |

---

## ⚠️ Disclaimer

FinSight is built for **educational and analytical purposes only**. It is not financial advice. All analysis, predictions, and recommendations are generated by algorithms and AI models based on historical data and should not be used as the sole basis for investment or business decisions.

- Past performance does not guarantee future results
- Stock price predictions are probabilistic estimates with uncertainty
- AI agent analysis is supplementary, not definitive
- Always consult qualified financial advisors for major decisions

---

## 📄 License

MIT License — Free to use, modify, and distribute with attribution.

---

## 🙏 Acknowledgments

- **Yahoo Finance** — Live financial data via yfinance
- **NSE India** — Nifty 500 company list
- **Anthropic** — Claude AI for agent intelligence
- **Streamlit** — Web application framework
- **Plotly** — Interactive visualization library
- **Scikit-learn** — Machine learning toolkit

---

<div align="center">

**Built with ⚡ by Nikhil Singh**

*FinSight — Where AI meets Financial Intelligence*

[GitHub](https://github.com/160chauhannikhil/FinSight) • [Live Demo](https://finsight-gjcwxba4rp6y2b49hgkghf.streamlit.app)

</div>
