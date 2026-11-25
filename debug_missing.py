"""
Debug specific missing songs from PDF parse
"""
import re
import json

with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

song_header_pattern = re.compile(
    r'(?:^|\n)\s*(\d+)\.\s+(.+?)(?:\s+[Cc][Ll][Ee\u00e9\u00c9\u00c8\u00e8]\s+\S+(?:\s+\S+)?)?\s*$',
    re.MULTILINE
)

headers = []
for m in song_header_pattern.finditer(text):
    num = int(m.group(1))
    title = m.group(2).strip()
    headers.append((m.start(), m.end(), num, title))

# Check missing songs - find the headers
missing = [8, 9, 11, 15, 41, 42, 45, 84]
for num in missing:
    for h in headers:
        if h[2] == num:
            pos, end, n, title = h
            # Find next header
            next_idx = headers.index(h) + 1
            if next_idx < len(headers):
                next_pos = headers[next_idx][0]
            else:
                next_pos = len(text)
            content = text[end:next_pos]
            
            # Show raw content
            print(f'Song {num}: {title}')
            print(f'  Content length: {len(content)}')
            
            # Check for verse numbers in content
            verse_nums = re.findall(r'^(\d+)$', content, re.MULTILINE)
            print(f'  Verse numbers found: {verse_nums}')
            
            # Show first 300 chars
            print(f'  Raw content: {repr(content[:300])}')
            print()
            break
    else:
        print(f'Song {num}: HEADER NOT FOUND')
        # Search in raw text
        pattern = re.compile(r'(?:^|\n)\s*' + str(num) + r'\.\s', re.MULTILINE)
        matches = pattern.findall(text)
        print(f'  Raw search matches: {len(matches)}')
        # Show context
        for m in pattern.finditer(text):
            print(f'  Context: {repr(text[m.start():m.start()+200])}')
        print()
