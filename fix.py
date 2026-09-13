with open('app_new.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the warning message to show debug info
old = '''    else:
        st.markdown("<div class='warning-box'>⚠️ Could not fetch live data. Try another company.</div>", unsafe_allow_html=True)'''

new = '''    else:
        st.markdown(f"<div class='warning-box'>⚠️ Could not fetch live data for '{selected_company}'. Try: Infosys Ltd, TCS, Reliance Industries Ltd</div>", unsafe_allow_html=True)'''

content = content.replace(old, new, 1)

# Fix get_company_data to always try fallback
old2 = '''def get_company_data(company_name, ticker):
    live = fetch_live_data(ticker)
    if live and live.get("revenue"):
        return live, "live"
    fallback = FALLBACK_DATA.get(company_name)
    if fallback:
        return fallback, "fallback"
    alpha = fetch_alpha_vantage(ticker)
    if alpha and alpha.get("revenue"):
        return alpha, "live"'''

new2 = '''def get_company_data(company_name, ticker):
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
    return None, "none"'''

content = content.replace(old2, new2)

with open('app_new.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed')