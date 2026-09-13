import os

files = ['app_new.py', 'export_pdf.py', 'README.md']

for filename in files:
    if not os.path.exists(filename):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('CrisisIQ', 'FinSight')
    content = content.replace('crisisiq', 'finsight')
    content = content.replace('AI Crisis Simulator', 'FinSight')
    content = content.replace('AI-Powered Financial Crisis Simulator', 'FinSight')
    content = content.replace('Financial Intelligence Platform', 'Financial Intelligence Platform')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filename}')

print('All done!')