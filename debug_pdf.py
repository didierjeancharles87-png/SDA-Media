"""
Debug version of PDF parser
"""
import re
import json

with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

song_header_pattern = re.compile(
    r'(?:^|\n)\s*(\d+)\.\s+(.+?)(?:\s+[Cc][Ll][Ee\u00e9\u00c9\u00c8\u00e8]\s+\S+(?:\s+\S+)?)?\s*$',
    re.MULTILINE
)

# Find all song headers first
headers = []
for m in song_header_pattern.finditer(text):
    num = int(m.group(1))
    title = m.group(2).strip()
    headers.append((m.start(), num, title))

print(f'Found {len(headers)} song headers')
print(f'First 5: {[(h[1], h[2][:30]) for h in headers[:5]]}')
print(f'Last 5: {[(h[1], h[2][:30]) for h in headers[-5:]]}')

# Check for duplicates
from collections import Counter
nums = [h[1] for h in headers]
dupes = {k: v for k, v in Counter(nums).items() if v > 1}
print(f'Duplicate numbers: {dupes}')
if 480 in dupes:
    print('Found 480 duplicates')
    for h in headers:
        if h[1] == 480:
            print(f'  480 at pos {h[0]}: title="{h[2][:50]}"')

# Test parsing song 1
print('\n\n=== Testing Song 1 ===')
pos, num, title = headers[0]
end_pos = headers[1][0]
song_text = text[pos:end_pos]
print(f'Song text length: {len(song_text)}')
print(f'First 300 chars:')
print(repr(song_text[:300]))
print(f'Last 200 chars:')
print(repr(song_text[-200:]))

# Test verse extraction
lines = song_text.split('\n')
print(f'\nLines in song text: {len(lines)}')
for i, line in enumerate(lines[:10]):
    print(f'  {i}: {repr(line[:80])}')
