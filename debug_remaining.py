"""
Check remaining 8 missing songs
"""
import re

with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

for num in [110, 272, 342, 361, 434, 481, 518, 732]:
    # Search raw text
    pattern = re.compile(r'(?:^|\n)\s*' + str(num) + r'\.\s', re.MULTILINE)
    for m in pattern.finditer(text):
        start = max(0, m.start())
        end = min(len(text), m.start() + 500)
        snippet = text[start:end]
        print(f'Song {num}:')
        print(repr(snippet[:300]))
        print()
