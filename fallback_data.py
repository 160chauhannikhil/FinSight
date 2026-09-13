FALLBACK_DATA = {
    "Zomato Ltd": {
        "revenue": 4206, "gross_profit": 1839, "ebitda": 293,
        "ebit": 194, "net_income": 351, "total_assets": 16436,
        "total_debt": 24, "cash": 8953, "capex": 180,
        "market_cap": 180000, "pe_ratio": 195.0, "pb_ratio": 8.2,
        "dividend_yield": 0.0, "roe": 4.2, "sector": "Consumer Cyclical",
    },
    "HDFC Bank Ltd": {
        "revenue": 98710, "gross_profit": 47240, "ebitda": 47240,
        "ebit": 44800, "net_income": 60810, "total_assets": 3561047,
        "total_debt": 210000, "cash": 185000, "capex": 3200,
        "market_cap": 1050000, "pe_ratio": 17.2, "pb_ratio": 2.1,
        "dividend_yield": 1.2, "roe": 16.5, "sector": "Financial Services",
        "net_interest_income": 89657, "operating_profit": 44800,
    },
    "ICICI Bank Ltd": {
        "revenue": 78620, "gross_profit": 38940, "ebitda": 38940,
        "ebit": 36500, "net_income": 44210, "total_assets": 2389000,
        "total_debt": 156000, "cash": 142000, "capex": 2800,
        "market_cap": 780000, "pe_ratio": 17.6, "pb_ratio": 3.1,
        "dividend_yield": 0.8, "roe": 18.2, "sector": "Financial Services",
        "net_interest_income": 63651, "operating_profit": 36500,
    },
    "Axis Bank Ltd": {
        "revenue": 88067, "gross_profit": 35650, "ebitda": 35650,
        "ebit": 33200, "net_income": 26480, "total_assets": 1432000,
        "total_debt": 98000, "cash": 118000, "capex": 1800,
        "market_cap": 387933, "pe_ratio": 14.03, "pb_ratio": 1.8,
        "dividend_yield": 0.1, "roe": 17.3, "sector": "Financial Services",
        "net_interest_income": 47614, "operating_profit": 33200,
    },
    "State Bank of India": {
        "revenue": 395693, "gross_profit": 152000, "ebitda": 152000,
        "ebit": 142000, "net_income": 61077, "total_assets": 6184000,
        "total_debt": 420000, "cash": 380000, "capex": 4200,
        "market_cap": 690000, "pe_ratio": 11.3, "pb_ratio": 1.4,
        "dividend_yield": 1.8, "roe": 20.3, "sector": "Financial Services",
        "net_interest_income": 153765, "operating_profit": 142000,
    },
    "Paytm": {
        "revenue": 9978, "gross_profit": 5468, "ebitda": -624,
        "ebit": -890, "net_income": -1422, "total_assets": 14832,
        "total_debt": 180, "cash": 8626, "capex": 420,
        "market_cap": 32000, "pe_ratio": None, "pb_ratio": 2.1,
        "dividend_yield": 0.0, "roe": -12.4, "sector": "Technology",
    },
    "Nykaa": {
        "revenue": 6386, "gross_profit": 1756, "ebitda": 213,
        "ebit": 124, "net_income": 40, "total_assets": 4218,
        "total_debt": 96, "cash": 892, "capex": 180,
        "market_cap": 38000, "pe_ratio": 890.0, "pb_ratio": 12.4,
        "dividend_yield": 0.0, "roe": 1.8, "sector": "Consumer Cyclical",
    },
}

INDUSTRY_BENCHMARKS = {
    "IT Services": {
        "avg_ebitda_margin": 24.5, "avg_pe": 28.0, "avg_roe": 28.0,
        "avg_debt_equity": 0.05, "avg_current_ratio": 2.8,
        "top_companies": ["Infosys", "TCS", "Wipro", "HCL Tech"],
    },
    "Banking": {
        "avg_ebitda_margin": 45.0, "avg_pe": 15.0, "avg_roe": 16.0,
        "avg_debt_equity": 8.5, "avg_current_ratio": 1.1,
        "top_companies": ["HDFC Bank", "ICICI Bank", "Axis Bank", "SBI"],
    },
    "Financial Services": {
        "avg_ebitda_margin": 45.0, "avg_pe": 15.0, "avg_roe": 16.0,
        "avg_debt_equity": 8.5, "avg_current_ratio": 1.1,
        "top_companies": ["HDFC Bank", "ICICI Bank", "Axis Bank", "SBI"],
    },
    "FMCG": {
        "avg_ebitda_margin": 22.0, "avg_pe": 55.0, "avg_roe": 72.0,
        "avg_debt_equity": 0.02, "avg_current_ratio": 1.5,
        "top_companies": ["HUL", "ITC", "Nestle", "Dabur"],
    },
    "Automotive": {
        "avg_ebitda_margin": 12.0, "avg_pe": 28.0, "avg_roe": 18.0,
        "avg_debt_equity": 0.15, "avg_current_ratio": 1.2,
        "top_companies": ["Maruti", "Tata Motors", "M&M", "Hero Moto"],
    },
    "Pharma": {
        "avg_ebitda_margin": 20.0, "avg_pe": 32.0, "avg_roe": 16.0,
        "avg_debt_equity": 0.12, "avg_current_ratio": 2.1,
        "top_companies": ["Sun Pharma", "Dr Reddy", "Cipla", "Divi's"],
    },
    "Manufacturing": {
        "avg_ebitda_margin": 14.0, "avg_pe": 18.0, "avg_roe": 12.0,
        "avg_debt_equity": 0.45, "avg_current_ratio": 1.3,
        "top_companies": ["Tata Steel", "JSW Steel", "Hindalco", "Vedanta"],
    },
    "Energy": {
        "avg_ebitda_margin": 18.0, "avg_pe": 12.0, "avg_roe": 14.0,
        "avg_debt_equity": 0.55, "avg_current_ratio": 1.1,
        "top_companies": ["ONGC", "BPCL", "IOC", "Reliance"],
    },
    "Food Tech": {
        "avg_ebitda_margin": 5.0, "avg_pe": 180.0, "avg_roe": 3.0,
        "avg_debt_equity": 0.02, "avg_current_ratio": 3.2,
        "top_companies": ["Zomato", "Swiggy"],
    },
    "Conglomerate": {
        "avg_ebitda_margin": 16.0, "avg_pe": 22.0, "avg_roe": 10.0,
        "avg_debt_equity": 0.35, "avg_current_ratio": 1.4,
        "top_companies": ["Reliance", "Tata Group", "Adani Group"],
    },
}