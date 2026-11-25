"""
Resolve duplicate song numbers by matching titles with HTML
"""
import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

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

html_map = {}
for s in html_data['hira']:
    html_map[s['numero']] = s['titre'].lower()

# Duplicate pairs
dups = {
    27: [('AVIA,RY VAZAN-TANY  O!', 'AVIA,RY VAZAN-TANY O'), ('NANDAO NY LANITRA IANAO', 'NANDAO NY LANITRA IANAO')],
    100: [('HE TAZAKO ILAY MPAMONJY', 'HE TAZAKO ILAY MPAMONJY'), ('HE REKO FA MANAKOAKO', 'HE REKO FA MANAKOAKO')],
    218: [('MIDERA ANAO ZAHAY', 'MIDERA ANAO ZAHAY'), ('NY LANITRA FIANDRIANANAO', 'NY LANITRA FIANDRIANANAO')],
    260: [('IANAO RY JESO O!', 'IANAO RY JESO O'), ('RAISO AHO, TOMPO O', 'RAISO AHO TOMPO')],
    334: [('FOTOANA TOY INONA', 'FOTOANA TOY INONA'), ('HO AKAIKINAO KOKOA', 'HO AKAIKINAO KOKOA')],
    343: [('NY MPAMONJY NO MITADY', 'NY MPAMONJY NO MITADY'), ('MANATONA RY MPANOTA', 'MANATONA RY MPANOTA')],
    480: [('O! RY NAMAKO AVIA', 'O! RY NAMAKO AVIA'), ('RAHA MAFY IZAO NY MAHORY', 'RAHA MAFY IZAO NY MAHORY')],
    723: [('AOKA HIRAY SAINA ISIKA', 'AOKA HIRAY SAINA ISIKA'), ('MAMAKY NY ONJA', 'MAMAKY NY ONJA')],
}

for num in sorted(dups.keys()):
    t0_short, t0_full = dups[num][0]
    t1_short, t1_full = dups[num][1]
    
    html_title = html_map.get(num, '')
    print('Song ' + str(num) + ':')
    print('  HTML title: ' + html_map.get(num, 'NOT IN HTML'))
    print('  PDF [0]: ' + t0_short)
    print('  PDF [1]: ' + t1_short)
    
    # Check which PDF title matches HTML
    t0_match = t0_full.lower() in html_title or html_title in t0_full.lower()
    t1_match = t1_full.lower() in html_title or html_title in t1_full.lower()
    
    if t0_match and not t1_match:
        print('  -> [0] MATCHES HTML (keep as song ' + str(num) + ')')
        print('  -> [1] is extra song, needs different number')
    elif t1_match and not t0_match:
        print('  -> [1] MATCHES HTML (keep as song ' + str(num) + ')')
        print('  -> [0] is extra song, needs different number')
    elif t0_match and t1_match:
        print('  -> BOTH match!')
    else:
        print('  -> NEITHER matches')
    
    # Find occurrences in PDF text
    with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    pattern = re.compile(r'(?:^|\n)[ \t]*' + str(num) + r'\.[ \t]+', re.MULTILINE)
    for m in pattern.finditer(text):
        start_pos = m.start()
        # Get next 200 chars
        snippet = text[start_pos:start_pos+200]
        # Check which title it has
        for k, (short, full) in enumerate([dups[num][0], dups[num][1]]):
            if short[:30] in snippet:
                print('  Occ at pos ' + str(start_pos) + ': [' + str(k) + '] ' + full)
    print()
