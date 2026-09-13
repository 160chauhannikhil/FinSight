import requests

ALPHA_VANTAGE_KEY = "1XC74SBV27YOO89K"

def fetch_alpha_vantage(ticker):
    try:
        symbol = ticker.replace(".NS", "") + ".BSE"
        inc_url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
        inc_data = requests.get(inc_url, timeout=10).json()
        bal_url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
        bal_data = requests.get(bal_url, timeout=10).json()
        ov_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
        ov_data = requests.get(ov_url, timeout=10).json()
        if not ov_data.get("Symbol"):
            return None
        def safe_float(val, divisor=1e7):
            try:
                return round(float(val) / divisor, 2)
            except:
                return None
        inc = inc_data.get("annualReports", [{}])[0] if inc_data.get("annualReports") else {}
        bal = bal_data.get("annualReports", [{}])[0] if bal_data.get("annualReports") else {}
        return {
            "revenue": safe_float(inc.get("totalRevenue")),
            "gross_profit": safe_float(inc.get("grossProfit")),
            "ebitda": safe_float(inc.get("ebitda")),
            "ebit": safe_float(inc.get("ebit")),
            "net_income": safe_float(inc.get("netIncome")),
            "total_assets": safe_float(bal.get("totalAssets")),
            "total_debt": safe_float(bal.get("totalLiabilities")),
            "cash": safe_float(bal.get("cashAndCashEquivalentsAtCarryingValue")),
            "capex": 0,
            "market_cap": safe_float(ov_data.get("MarketCapitalization"), 1e7),
            "pe_ratio": round(float(ov_data.get("PERatio", 0)), 2) if ov_data.get("PERatio") not in [None, "None"] else None,
            "pb_ratio": round(float(ov_data.get("PriceToBookRatio", 0)), 2) if ov_data.get("PriceToBookRatio") not in [None, "None"] else None,
            "dividend_yield": round(float(ov_data.get("DividendYield", 0)) * 100, 2) if ov_data.get("DividendYield") not in [None, "None"] else 0,
            "52w_high": float(ov_data.get("52WeekHigh", 0)) if ov_data.get("52WeekHigh") not in [None, "None"] else None,
            "52w_low": float(ov_data.get("52WeekLow", 0)) if ov_data.get("52WeekLow") not in [None, "None"] else None,
            "current_price": float(ov_data.get("50DayMovingAverage", 0)) if ov_data.get("50DayMovingAverage") not in [None, "None"] else None,
            "sector": ov_data.get("Sector", "N/A"),
            "roe": round(float(ov_data.get("ReturnOnEquityTTM", 0)) * 100, 2) if ov_data.get("ReturnOnEquityTTM") not in [None, "None"] else None,
            "net_interest_income": None,
            "operating_profit": safe_float(inc.get("operatingIncome")),
            "nim": None,
        }
    except Exception as e:
        return None
