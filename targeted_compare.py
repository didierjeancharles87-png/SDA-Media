"""
Targeted comparison: find HTML songs missing verses that PDF has.
"""
import json, re

with open('fihirana_advantista.html', 'r', encoding='utf-8') as f:
    content = f.read()
start = content.find('var FIHIRANA_DATA =')
start = content.find('{', start)
depth = 0
end = start
for i in range(start, len(content)):
    if content[i] == '{': depth += 1
    elif content[i] == '}': depth -= 1
    if depth == 0: end = i + 1; break
while end < len(content) and content[end] != ';': end += 1
json_str = content[start:end].rstrip(';')
html_data = json.loads(json_str)

with open('pdf_parsed.json', 'r', encoding='utf-8') as f:
    pdf = json.load(f)

html_map = {}
for s in html_data['hira']:
    verses = {}
    for p in s['paroles']:
        verses[p['couplet']] = p['texte']
    html_map[s['numero']] = {'titre': s['titre'], 'verses': verses, 'obj': s}

common = sorted(set(html_map.keys()) & set(int(k) for k in pdf.keys()))

# ── Case 1: Find songs where HTML has FEWER verses than PDF ──
print("=== SONGS WHERE HTML MISSING VERSES PDF HAS ===")
for num in common:
    ns = str(num)
    h = html_map[num]
    p = pdf[ns]
    h_verses = set(h['verses'].keys())
    p_verses = set(p['verses'].keys())
    
    # Filter out 'extra' from comparison
    h_stripped = {v for v in h_verses if v != 'extra'}
    
    # PDF verses not in HTML (excluding extra)
    missing = p_verses - h_stripped
    if missing:
        print(num, ':', h['titre'], '- missing PDF verses:', sorted(missing, key=int))
        for v in sorted(missing, key=int):
            print('  PDF verse', v, ':', p['verses'][v][:120])

print("\n=== SONGS WHERE PDF HAS LONGER VERSES THAN HTML ===")
count = 0
for num in common:
    if count >= 20: break
    ns = str(num)
    h = html_map[num]
    p = pdf[ns]
    for v in sorted(set(h['verses'].keys()) & set(p['verses'].keys())):
        if v == 'extra': continue
        htxt = h['verses'][v]
        ptxt = p['verses'][v]
        # If PDF is significantly longer, likely HTML is truncated
        if len(ptxt) > len(htxt) * 1.3 and len(htxt) > 20:
            print(num, ':', h['titre'], '- verse', v)
            print('  HTML len:', len(htxt), 'PDF len:', len(ptxt))
            print('  HTML:', htxt[:150])
            print('  PDF: ', ptxt[:150])
            count += 1
            print()
