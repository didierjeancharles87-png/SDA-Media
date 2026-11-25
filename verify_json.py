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
        end = start
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

        json_str = line[start:end]
        data = json.loads(json_str)

        ot = data['testamenta_taloha']
        nv = data['testamenta_vaovao']

        print(f'OT books: {len(ot)}')
        print(f'NV books: {len(nv)}')
        print()

        for book in ot:
            ch_count = book['chapter_count']
            v_count = sum(len(v) for v in book['chapters'].values())
            print(f'  {book["name"]}: {ch_count} ch, {v_count} v')

        print()
        for book in nv:
            ch_count = book['chapter_count']
            v_count = sum(len(v) for v in book['chapters'].values())
            print(f'  {book["name"]}: {ch_count} ch, {v_count} v')

        break
