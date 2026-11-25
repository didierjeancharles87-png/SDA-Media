"""
Robust PDF parser v4: extract songs with correct verse parsing
"""
import re
import json

with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# More flexible song header pattern
song_header_pattern = re.compile(
    r'(?:^|\n)\s*(\d+)\.\s+(.+?)(?:\s+[Cc][Ll][Ee\u00e9\u00c9\u00c8\u00e8]\s+\S+(?:\s+\S+)?)?\s*$',
    re.MULTILINE
)

headers = []
for m in song_header_pattern.finditer(text):
    num = int(m.group(1))
    title = m.group(2).strip()
    headers.append((m.start(), m.end(), num, title))

print(f'Found {len(headers)} song headers')

all_songs = {}
for i in range(len(headers)):
    pos, end, num, title = headers[i]
    if i + 1 < len(headers):
        next_pos = headers[i + 1][0]
    else:
        next_pos = len(text)
    
    # Content starts after the header line
    content_text = text[end:next_pos]
    
    verses = {}
    current_vnum = None
    current_lines = []
    
    for line in content_text.split('\n'):
        ls = line.strip()
        if not ls:
            # Preserve empty lines as verse separators
            continue
        if ls in ['A. Jamina', 'A . Jamina']:
            continue
        if ls.startswith('===PAGE'):
            continue
        
        # Verse number (just a number on its own)
        vm = re.match(r'^(\d+)$', ls)
        if vm:
            if current_vnum is not None and current_lines:
                key = str(current_vnum)
                if key in verses:
                    verses[key] = verses[key] + current_lines
                else:
                    verses[key] = current_lines
            current_vnum = vm.group(1)
            current_lines = []
            continue
        
        # Skip if line looks like another song header
        if re.match(r'^\d+\.\s+', ls):
            continue
        
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

print(f'Extracted {len(all_songs)} songs from PDF')

# Save
with open('pdf_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(all_songs, f, indent=2, ensure_ascii=False)

nums = sorted([int(k) for k in all_songs.keys()])
print(f'Range: {nums[0]} - {nums[-1]}')
print(f'Count: {len(nums)}')

all_expected = set(range(1, 757))
found = set(nums)
missing = sorted(all_expected - found)
print(f'Missing ({len(missing)}): {missing}')
