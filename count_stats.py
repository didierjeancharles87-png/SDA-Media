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

ot_books = len(data['testamenta_taloha'])
nv_books = len(data['testamenta_vaovao'])
total_books = ot_books + nv_books

ot_ch = sum(b['chapter_count'] for b in data['testamenta_taloha'])
nv_ch = sum(b['chapter_count'] for b in data['testamenta_vaovao'])
total_ch = ot_ch + nv_ch

ot_v = sum(sum(len(vv) for vv in b['chapters'].values()) for b in data['testamenta_taloha'])
nv_v = sum(sum(len(vv) for vv in b['chapters'].values()) for b in data['testamenta_vaovao'])
total_v = ot_v + nv_v

print(f'Testamenta Taloha (AT): {ot_books} livres, {ot_ch} chapitres, {ot_v} versets')
print(f'Testamenta Vaovao (NT): {nv_books} livres, {nv_ch} chapitres, {nv_v} versets')
print(f'Total: {total_books} livres, {total_ch} chapitres, {total_v} versets')
