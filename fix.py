with open('app_new.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = "       <div style='font-size:20px; font-weight:800; color:#6366f1;'>FinSight</div>\n        <div style='font-size:11px; color:#475569; margin-top:4px; text-transform:uppercase; letter-spacing:0.08em;'>Financial Intelligence Platform</div>"

new = "       <div style='font-size:20px; font-weight:800; color:#6366f1;'>FinSight</div>\n        <div style='font-size:12px; font-weight:600; color:#4f7aff; margin-top:2px;'>by Nikhil Singh</div>\n        <div style='font-size:10px; color:#475569; margin-top:4px; text-transform:uppercase; letter-spacing:0.08em;'>Financial Intelligence Platform</div>"

content = content.replace(old, new)

with open('app_new.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')