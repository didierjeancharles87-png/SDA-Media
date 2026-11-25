"""
Improved PDF song parser - handles Clé with accent and other edge cases.
"""
import re
import json

with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by page markers
pages = text.split('===PAGE ')

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

for page in pages[1:]:
    page_text = page.split('\n', 1)[1] if '\n' in page else ''
    lines = page_text.split('\n')
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        if line_stripped.startswith('--- PAGE'):
            continue
        
        # Check for "A. Jamina" section headers
        if line_stripped in ['A. Jamina', 'A . Jamina']:
            continue
        
        # Check for song header: "NUM. TITLE Clé/Clé/cle KEY" or "NUM. TITLE"
        # Handles Clé, Clé, cle with or without accent on the 'e'
        song_match = re.match(
            r'^(\d+)\.\s+(.+?)(?:\s+[Cc][Ll][Ee\u00e9\u00c9]\s+|$)',
            line_stripped
        )
        if not song_match:
            # Also try: text before number, like "Deraiko ny Anaranao:,: \n41. ISAORANAY"
            song_match = re.search(
                r'(\d+)\.\s+(.+?)(?:\s+[Cc][Ll][Ee\u00e9\u00c9]\s+|$)',
                line_stripped
            )
        
        if song_match:
            save_current()
            current_num = int(song_match.group(1))
            current_title = song_match.group(2).strip()
            current_verses = {}
            current_vnum = None
            current_lines = []
            continue
        
        # Check for voice part indicators starting a verse (no number)
        # Songs without numbered verses might have Feo 1,2,3 or similar
        feo_match = re.match(r'^(?:Feo\s+[\d,]+|Feo\s+)', line_stripped)
        
        # Check for verse number (a line that is just a number or starts with a number)
        verse_match = re.match(r'^(\d+)$', line_stripped)
        if verse_match:
            if current_vnum is not None and current_lines:
                key = str(current_vnum)
                if key in current_verses:
                    current_verses[key] = current_verses[key] + current_lines
                else:
                    current_verses[key] = current_lines
            current_vnum = verse_match.group(1)
            current_lines = []
            continue
        
        # Regular lyric line
        if current_num is not None:
            current_lines.append(line_stripped)

# Save last song
save_current()

print(f'Total songs extracted from PDF: {len(all_songs)}')

# Save parsed songs
serializable = {}
for num, song in all_songs.items():
    serializable[num] = {
        'titre': song['titre'],
        'verses': {k: '\n'.join(v) for k, v in song['verses'].items()}
    }

with open('pdf_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(serializable, f, indent=2, ensure_ascii=False)

print('Saved to pdf_parsed.json')

nums = sorted([int(k) for k in all_songs.keys()])
print(f'Range: {nums[0]} - {nums[-1]}')
print(f'Count: {len(nums)}')

# Find gaps
all_expected = set(range(1, 757))
found = set(nums)
missing = sorted(all_expected - found)
print(f'Missing ({len(missing)}): {missing}')
