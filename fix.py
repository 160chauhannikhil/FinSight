with open('fallback_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add dotted versions of all company names
additions = '''
    "Infosys Ltd.": {
        "revenue": 2016, "gross_profit": 608, "ebitda": 511,
        "ebit": 455, "net_income": 331, "total_assets": 1645,
        "total_debt": 97, "cash": 234, "capex": 31,
        "market_cap": 420300, "pe_ratio": 13.48, "pb_ratio": 3.2,
        "dividend_yield": 2.8, "roe": 32.5, "sector": "Technology",
        "current_price": 1850, "52w_high": 1990, "52w_low": 1350,
    },
    "Tata Consultancy Services Ltd.": {
        "revenue": 2408, "gross_profit": 850, "ebitda": 720,
        "ebit": 650, "net_income": 460, "total_assets": 2100,
        "total_debt": 45, "cash": 520, "capex": 42,
        "market_cap": 1380000, "pe_ratio": 28.5, "pb_ratio": 12.1,
        "dividend_yield": 1.8, "roe": 48.2, "sector": "Technology",
        "current_price": 3800, "52w_high": 4200, "52w_low": 3200,
    },
    "Reliance Industries Ltd.": {
        "revenue": 9000, "gross_profit": 2100, "ebitda": 1800,
        "ebit": 1500, "net_income": 750, "total_assets": 18000,
        "total_debt": 3200, "cash": 2100, "capex": 1200,
        "market_cap": 1750000, "pe_ratio": 22.4, "pb_ratio": 2.8,
        "dividend_yield": 0.4, "roe": 9.8, "sector": "Energy",
        "current_price": 2580, "52w_high": 2900, "52w_low": 2100,
    },
    "Wipro Ltd.": {
        "revenue": 900, "gross_profit": 280, "ebitda": 190,
        "ebit": 165, "net_income": 120, "total_assets": 980,
        "total_debt": 42, "cash": 180, "capex": 18,
        "market_cap": 245000, "pe_ratio": 19.2, "pb_ratio": 3.1,
        "dividend_yield": 0.2, "roe": 16.8, "sector": "Technology",
        "current_price": 445, "52w_high": 560, "52w_low": 380,
    },
    "Maruti Suzuki India Ltd.": {
        "revenue": 1420, "gross_profit": 320, "ebitda": 210,
        "ebit": 180, "net_income": 125, "total_assets": 1100,
        "total_debt": 15, "cash": 320, "capex": 45,
        "market_cap": 380000, "pe_ratio": 26.8, "pb_ratio": 4.2,
        "dividend_yield": 0.9, "roe": 18.2, "sector": "Automotive",
        "current_price": 11500, "52w_high": 13000, "52w_low": 9800,
    },
    "Sun Pharmaceutical Industries Ltd.": {
        "revenue": 480, "gross_profit": 280, "ebitda": 145,
        "ebit": 120, "net_income": 98, "total_assets": 780,
        "total_debt": 28, "cash": 145, "capex": 22,
        "market_cap": 320000, "pe_ratio": 34.2, "pb_ratio": 5.8,
        "dividend_yield": 0.8, "roe": 14.2, "sector": "Pharma",
        "current_price": 1320, "52w_high": 1480, "52w_low": 1050,
    },
    "Hindustan Unilever Ltd.": {
        "revenue": 620, "gross_profit": 320, "ebitda": 165,
        "ebit": 148, "net_income": 105, "total_assets": 420,
        "total_debt": 8, "cash": 85, "capex": 12,
        "market_cap": 520000, "pe_ratio": 52.4, "pb_ratio": 48.2,
        "dividend_yield": 1.8, "roe": 198.5, "sector": "FMCG",
        "current_price": 2210, "52w_high": 2800, "52w_low": 2100,
    },
    "Asian Paints Ltd.": {
        "revenue": 365, "gross_profit": 168, "ebitda": 92,
        "ebit": 80, "net_income": 58, "total_assets": 420,
        "total_debt": 12, "cash": 48, "capex": 18,
        "market_cap": 220000, "pe_ratio": 48.2, "pb_ratio": 18.4,
        "dividend_yield": 1.2, "roe": 28.4, "sector": "Paints",
        "current_price": 2280, "52w_high": 3200, "52w_low": 2100,
    },
    "Bajaj Finance Ltd.": {
        "revenue": 5200, "gross_profit": 3800, "ebitda": 3800,
        "ebit": 3500, "net_income": 1400, "total_assets": 38000,
        "total_debt": 28000, "cash": 2800, "capex": 120,
        "market_cap": 420000, "pe_ratio": 28.4, "pb_ratio": 5.2,
        "dividend_yield": 0.4, "roe": 21.8, "sector": "Financial Services",
        "net_interest_income": 3800, "operating_profit": 3500,
        "current_price": 6800, "52w_high": 8000, "52w_low": 6000,
    },
    "Oil & Natural Gas Corporation Ltd.": {
        "revenue": 6800, "gross_profit": 2100, "ebitda": 1850,
        "ebit": 1600, "net_income": 480, "total_assets": 8200,
        "total_debt": 980, "cash": 420, "capex": 620,
        "market_cap": 280000, "pe_ratio": 8.2, "pb_ratio": 1.1,
        "dividend_yield": 4.8, "roe": 14.2, "sector": "Energy",
        "current_price": 220, "52w_high": 285, "52w_low": 195,
    },
    "HDFC Bank Ltd.": {
        "revenue": 98710, "gross_profit": 47240, "ebitda": 47240,
        "ebit": 44800, "net_income": 60810, "total_assets": 3561047,
        "total_debt": 210000, "cash": 185000, "capex": 3200,
        "market_cap": 1050000, "pe_ratio": 17.2, "pb_ratio": 2.1,
        "dividend_yield": 1.2, "roe": 16.5, "sector": "Financial Services",
        "net_interest_income": 89657, "operating_profit": 44800,
        "current_price": 1650, "52w_high": 1880, "52w_low": 1400,
    },
    "ICICI Bank Ltd.": {
        "revenue": 78620, "gross_profit": 38940, "ebitda": 38940,
        "ebit": 36500, "net_income": 44210, "total_assets": 2389000,
        "total_debt": 156000, "cash": 142000, "capex": 2800,
        "market_cap": 780000, "pe_ratio": 17.6, "pb_ratio": 3.1,
        "dividend_yield": 0.8, "roe": 18.2, "sector": "Financial Services",
        "net_interest_income": 63651, "operating_profit": 36500,
        "current_price": 1120, "52w_high": 1280, "52w_low": 950,
    },
    "Zomato Ltd.": {
        "revenue": 4206, "gross_profit": 1839, "ebitda": 293,
        "ebit": 194, "net_income": 351, "total_assets": 16436,
        "total_debt": 24, "cash": 8953, "capex": 180,
        "market_cap": 180000, "pe_ratio": 195.0, "pb_ratio": 8.2,
        "dividend_yield": 0.0, "roe": 4.2, "sector": "Consumer Cyclical",
        "current_price": 220, "52w_high": 280, "52w_low": 180,
    },
    "State Bank of India.": {
        "revenue": 395693, "gross_profit": 152000, "ebitda": 152000,
        "ebit": 142000, "net_income": 61077, "total_assets": 6184000,
        "total_debt": 420000, "cash": 380000, "capex": 4200,
        "market_cap": 690000, "pe_ratio": 11.3, "pb_ratio": 1.4,
        "dividend_yield": 1.8, "roe": 20.3, "sector": "Financial Services",
        "net_interest_income": 153765, "operating_profit": 142000,
        "current_price": 780, "52w_high": 912, "52w_low": 680,
    },
'''

# Insert before closing }
content = content.replace('\n}\n\nINDUSTRY_BENCHMARKS', additions + '\n}\n\nINDUSTRY_BENCHMARKS')

with open('fallback_data.py', 'w', encoding='utf-8') as f:
    f.write(content)

import ast
with open('fallback_data.py', 'r', encoding='utf-8') as f:
    c = f.read()
try:
    ast.parse(c)
    print('Valid!')
except SyntaxError as e:
    print(f'Error at line {e.lineno}: {e.msg}')