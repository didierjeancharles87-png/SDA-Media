"""
Final PDF parser v5: handles all verse formats
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

print(f'Found {len(headers)} headers')

all_songs = {}

for i in range(len(headers)):
    pos, end, num, title = headers[i]
    next_pos = headers[i + 1][0] if i + 1 < len(headers) else len(text)
    content = text[end:next_pos]
    
    verses = {}
    current_vnum = None
    current_lines = []
    
    def save_verse():
        nonlocal current_vnum, current_lines
        if current_vnum is not None and current_lines:
            key = str(current_vnum)
            if key in verses:
                verses[key] = verses[key] + current_lines
            else:
                verses[key] = current_lines
            current_lines = []
    
    for line in content.split('\n'):
        ls = line.strip()
        if not ls:
            continue
        if ls in ['A. Jamina', 'A . Jamina']:
            continue
        if ls.startswith('===PAGE'):
            continue
        # Skip if looks like another song header
        if re.match(r'^\d+\.\s+', ls):
            continue
        
        # Check for verse number patterns:
        # Pattern 1: Line is just a number "1", "2", etc.
        # Pattern 2: Line starts with number+space then lyrics "1     Avia..."
        # Pattern 3: Line starts with number then ":" or similar
        
        # Pattern 1: standalone number
        vm1 = re.match(r'^(\d+)$', ls)
        # Pattern 2: number + whitespace + text
        vm2 = re.match(r'^(\d+)\s{2,}(.+)', ls)
        
        if vm1:
            save_verse()
            current_vnum = vm1.group(1)
            current_lines = []
        elif vm2:
            save_verse()
            current_vnum = vm2.group(1)
            # The text after the number is part of the verse
            current_lines = [vm2.group(2).strip()]
        else:
            current_lines.append(ls)
    
    save_verse()
    
    if verses:
        all_songs[num] = {
            'titre': title,
            'verses': {k: '\n'.join(v) for k, v in verses.items()}
        }
    
    # For songs without numbered verses, put all lyrics in verse "1"
    if not verses and content.strip():
        # Clean content
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

# Handle duplicate numbers (like 480 appearing twice)
# For duplicates, merge the verses
dup_counts = {}
for h in headers:
    n = h[2]
    dup_counts[n] = dup_counts.get(n, 0) + 1

dups = {k: v for k, v in dup_counts.items() if v > 1}
print(f'Duplicate numbers: {dups}')

# The second 480 (Raha mafy izao ny mahory) should actually be 481
# Let's check if both 480 entries have data
if 480 in all_songs:
    print('Song 480 verses:', list(all_songs[480]['verses'].keys()))

print(f'Total songs: {len(all_songs)}')

# Save
with open('pdf_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(all_songs, f, indent=2, ensure_ascii=False)

nums = sorted([int(k) for k in all_songs.keys()])
all_expected = set(range(1, 757))
found = set(nums)
missing = sorted(all_expected - found)
print(f'Missing ({len(missing)}): {missing}')
