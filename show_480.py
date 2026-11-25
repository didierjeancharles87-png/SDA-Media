import json

with open('fihirana_advantista.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('var FIHIRANA_DATA =')
start = content.find('{', start)
depth = 0; end = start
for i in range(start, len(content)):
    if content[i] == '{': depth += 1
    elif content[i] == '}': depth -= 1
    if depth == 0: end = i + 1; break
while end < len(content) and content[end] != ';': end += 1
json_str = content[start:end].rstrip(';')
html_data = json.loads(json_str)

for s in html_data['hira']:
    if s['numero'] == 480:
        print('Song 480:')
        print('  titre:', s['titre'])
        for p in s['paroles']:
            print('  couplet:', p['couplet'])
            print('  texte:', p['texte'][:200])
            print()
        break

# Find in original HTML
idx = content.find('"numero": 480')
if idx < 0:
    idx = content.find('"numero": 480')
print('Found at pos:', idx)
print()
# Show surrounding for editing
snippet = content[idx-200:idx+800]
print(snippet)
