with open('app_new.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''def get_company_data(company_name, ticker):
    live = fetch_live_data(ticker)
    if live and live.get("revenue"):
        return live, "live"
    fallback = FALLBACK_DATA.get(company_name)
    if fallback:
        return fallback, "fallback"
    return live, "live"'''

new = '''def get_company_data(company_name, ticker):
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
    return None, "none"'''

content = content.replace(old, new)

with open('app_new.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed')