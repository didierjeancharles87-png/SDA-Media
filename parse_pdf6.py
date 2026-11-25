"""
Final PDF parser v6: handles all verse formats
"""
import re
import json

with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

song_header_pattern = re.compile(
    r'(?:^|\n)[ \t]*(\d+)\.[ \t]+(.+?)(?:[ \t]+[Cc][Ll][Ee\u00e9\u00c9\u00c8\u00e8][ \t]+\S+(?:[ \t]+\S+)?)?[ \t]*$',
    re.MULTILINE
)

headers = []
for m in song_header_pattern.finditer(text):
    num = int(m.group(1))
    title = m.group(2).strip()
    headers.append((m.start(), m.end(), num, title))

print(f'Found {len(headers)} headers')

all_songs = {}

# Filter: keep only first occurrence of each song number
seen = set()
unique_headers = []
for pos, end, num, title in headers:
    if num not in seen:
        seen.add(num)
        unique_headers.append((pos, end, num, title))
    else:
        print(f'  Drop duplicate: song {num} at pos {pos}')
headers = unique_headers
print(f'Unique headers: {len(headers)}')

for i in range(len(headers)):
    pos, end, num, title = headers[i]
    next_pos = headers[i + 1][0] if i + 1 < len(headers) else len(text)
    content = text[end:next_pos]
    
    verses = {}
    current_vnum = None
    current_lines = []
    
    for line in content.split('\n'):
        ls = line.strip()
        if not ls:
            continue
        if ls in ['A. Jamina', 'A . Jamina']:
            continue
        if ls.startswith('===PAGE'):
            continue
        if re.match(r'^\d+\.\s+', ls):
            continue
        
        # Pattern 1: standalone number
        vm1 = re.match(r'^(\d+)$', ls)
        # Pattern 2: number + 2+ spaces + text
        vm2 = re.match(r'^(\d+)\s{2,}(.+)', ls)
        
        if vm1:
            if current_vnum is not None and current_lines:
                key = str(current_vnum)
                if key in verses:
                    verses[key] = verses[key] + current_lines
                else:
                    verses[key] = current_lines
            current_vnum = vm1.group(1)
            current_lines = []
        elif vm2:
            if current_vnum is not None and current_lines:
                key = str(current_vnum)
                if key in verses:
                    verses[key] = verses[key] + current_lines
                else:
                    verses[key] = current_lines
            current_vnum = vm2.group(1)
            current_lines = [vm2.group(2).strip()]
        else:
            current_lines.append(ls)
    
    # Save last verse
    if current_vnum is not None and current_lines:
        key = str(current_vnum)
        if key in verses:
            verses[key] = verses[key] + current_lines
        else:
            verses[key] = current_lines
    
    if verses:
        all_songs[num] = {
            'titre': title,
            'verses': {k: '\n'.join(v) for k, v in verses.items()}
        }
    
    # For songs without numbered verses, put all lyrics in verse "1"
    if num not in all_songs and content.strip():
        clean_lines = []
        for line in content.split('\n'):
            ls = line.strip()
            if ls and not re.match(r'^\d+\.\s+', ls) and ls not in ['A. Jamina', 'A . Jamina'] and not ls.startswith('===PAGE'):
                clean_lines.append(ls)
        if clean_lines:
            all_songs[num] = {
                'titre': title,
                'verses': {'1': '\n'.join(clean_lines)}
            }

print(f'Total songs: {len(all_songs)}')

with open('pdf_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(all_songs, f, indent=2, ensure_ascii=False)

nums = sorted([int(k) for k in all_songs.keys()])
all_expected = set(range(1, 757))
found = set(nums)
missing = sorted(all_expected - found)
print(f'Missing ({len(missing)}): {missing}')
