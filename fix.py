with open('app_new.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'search_query = st.text_input("🔍 Search Company", placeholder="Type company name...")\n\n    all_companies'

new = '    search_query = st.text_input("🔍 Search Company", placeholder="Type company name...")\n    all_companies'

content = content.replace(old, new)

with open('app_new.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')