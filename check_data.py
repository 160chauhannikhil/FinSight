import yfinance as yf
import pandas as pd
import numpy as np

tickers = {
    "Infosys": "INFY.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Reliance": "RELIANCE.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Wipro": "WIPRO.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Maruti": "MARUTI.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Zomato": "ZOMATO.NS",
}

fields = ["Total Revenue", "Gross Profit", "EBITDA", "EBIT", "Net Income"]
bs_fields = ["Total Assets", "Total Debt", "Cash And Cash Equivalents"]

results = []
for name, ticker in tickers.items():
    print(f"Checking {name}...")
    t = yf.Ticker(ticker)
    fin = t.financials
    bs = t.balance_sheet
    row = {"Company": name}
    for f in fields:
        row[f] = "✅" if fin is not None and not fin.empty and f in fin.index else "❌"
    for f in bs_fields:
        row[f] = "✅" if bs is not None and not bs.empty and f in bs.index else "❌"
    results.append(row)

df = pd.DataFrame(results)
print(df.to_string(index=False))