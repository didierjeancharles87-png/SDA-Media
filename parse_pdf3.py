"""
Improved PDF song parser v3 - handles more edge cases.
"""
import re
import json

with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace problematic Unicode chars for comparison
# Keep original for output

all_songs = {}
current_num = None
current_title = None
current_verses = {}
current_vnum = None
current_lines = []

def save_current():
    global current_num, current_title, current_verses, current_vnum, current_lines
    if current_num is not None and current_title:
        if current_vnum is not None and current_lines:
            key = str(current_vnum)
            if key in current_verses:
                current_verses[key] = current_verses[key] + current_lines
            else:
                current_verses[key] = current_lines
        if current_verses:
            all_songs[current_num] = {
                'titre': current_title,
                'verses': dict(current_verses)
            }

# More flexible song header pattern
# Matches: "NUM. TITLE" optionally followed by "Clé/cle/Cle KEY" or at end of line
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

# Now parse verses for each song by finding text between headers
all_songs = {}
for i, (pos, num, title) in enumerate(headers):
    # Determine the end position (next header or end of text)
    if i + 1 < len(headers):
        end_pos = headers[i + 1][0]
    else:
        end_pos = len(text)
    
    # Get the text for this song
    song_text = text[pos:end_pos]
    
    # Extract verses
    verses = {}
    current_vnum = None
    current_lines = []
    
    lines = song_text.split('\n')
    # Skip the first line (the header itself)
    for line in lines[1:]:
        ls = line.strip()
        if not ls:
            continue
        
        # Skip "A. Jamina" headers
        if ls in ['A. Jamina', 'A . Jamina']:
            continue
        
        # Verse number
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
        
        # Check if this is another song header (shouldn't be but just in case)
        if re.match(r'^\d+\.\s+', ls):
            break
        
        # Regular line
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

print(f'Total songs extracted from PDF: {len(all_songs)}')

# Save to JSON
serializable = {}
for num, song in all_songs.items():
    serializable[num] = {
        'titre': song['titre'],
        'verses': song['verses']
    }

with open('pdf_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(serializable, f, indent=2, ensure_ascii=False)

print('Saved to pdf_parsed.json')

nums = sorted(all_songs.keys())
print(f'Range: {nums[0]} - {nums[-1]}')
print(f'Count: {len(nums)}')

all_expected = set(range(1, 757))
found = set(nums)
missing = sorted(all_expected - found)
print(f'Missing ({len(missing)}): {missing}')
