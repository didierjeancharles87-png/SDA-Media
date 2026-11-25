import re
import json

with open('baibolyMG_v2.html', 'r', encoding='utf-8') as f:
    html = f.read()

lines = html.split('\n')
for line in lines:
    if 'window.BIBLE_DATA' in line and '=' in line:
        prefix = 'window.BIBLE_DATA = '
        start = line.index(prefix) + len(prefix)
        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(line)):
            ch = line[i]
            if escape:
                escape = False
            elif ch == '\\' and in_string:
                escape = True
            elif ch == '"':
                in_string = not in_string
            elif not in_string:
                if ch == '{' or ch == '[':
                    depth += 1
                elif ch == '}' or ch == ']':
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break
        data = json.loads(line[start:end])
        break

standard = {
    'Genesisy': (50, 1533), 'Eksodosy': (40, 1213), 'Levitikosy': (27, 859),
    'Nomery': (36, 1288), 'Deoteronomia': (34, 959), 'Josoa': (24, 658),
    'Mpitsara': (21, 618), 'Rota': (4, 85), '1 Samoela': (31, 810),
    '2 Samoela': (24, 695), '1 Mpanjaka': (22, 816), '2 Mpanjaka': (25, 719),
    '1 Tantara': (29, 942), '2 Tantara': (36, 822), 'Ezra': (10, 280),
    'Nehemia': (13, 406), 'Estera': (10, 167), 'Joba': (42, 1070),
    'Salamo': (150, 2527), 'Ohabolana': (31, 915), 'Mpitoriteny': (12, 222),
    'Tonon-kiran\'i Solomona': (8, 117), 'Isaia': (66, 1292),
    'Jeremia': (52, 1364), 'Fitomaniana': (5, 154), 'Ezekiela': (48, 1273),
    'Daniela': (12, 357), 'Hosea': (14, 197), 'Joela': (3, 73),
    'Amosa': (9, 146), 'Obadia': (1, 21), 'Jona': (4, 48),
    'Mika': (7, 105), 'Nahoma': (3, 47), 'Habakoka': (3, 56),
    'Zefania': (3, 53), 'Hagay': (2, 38), 'Zakaria': (14, 211),
    'Malakia': (4, 55)
}

issues = []
for book in data['testamenta_taloha']:
    name = book['name']
    ch = book['chapter_count']
    v = sum(len(vv) for vv in book['chapters'].values())
    if name in standard:
        exp_ch, exp_v = standard[name]
        if ch != exp_ch or v != exp_v:
            diff_ch = ch - exp_ch
            diff_v = v - exp_v
            issues.append(f'  {name}: {ch}ch/{v}v (std {exp_ch}ch/{exp_v}v, diff {diff_ch:+d}ch/{diff_v:+d}v)')

print(f'Books with discrepancies: {len(issues)}')
for i in issues:
    print(i)
if not issues:
    print('All books match standard versification!')

print('\n=== Books we just replaced ===')
replaced = ['Genesisy','Eksodosy','Levitikosy','Nomery','1 Mpanjaka','1 Tantara',
            'Nehemia','Joba','Salamo','Ezekiela','Daniela']
for book in data['testamenta_taloha']:
    if book['name'] in replaced:
        ch = book['chapter_count']
        v = sum(len(vv) for vv in book['chapters'].values())
        status = 'OK' if (book['name'] not in standard or 
                         (ch == standard[book['name']][0] and v == standard[book['name']][1])) else 'DIFF'
        print(f'  {book["name"]}: {ch}ch/{v}v [{status}]')
