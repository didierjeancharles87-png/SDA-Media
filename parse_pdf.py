"""
Extract all songs from PDF text with careful verse parsing.
"""
import re

with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by page markers
pages = text.split('===PAGE ')

# Parse each page, looking for songs
all_songs = {}  # numero -> {titre, verses: {vnum: [lines]}}

current_num = None
current_title = None
current_verses = {}  # {vnum: [lines]}
current_vnum = None
current_lines = []

def save_current():
    global current_num, current_title, current_verses, current_vnum, current_lines
    if current_num is not None and current_title:
        if current_vnum is not None and current_lines:
            # Save current verse
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
        
        # Skip empty lines and page markers
        if not line_stripped:
            continue
        if line_stripped.startswith('--- PAGE'):
            continue
        
        # Check if this is a song header: "NUM. TITLE Clé/cle KEY" or "NUM. TITLE"
        song_match = re.match(r'^(\d+)\.\s+(.+?)(?:\s+[Cc][Ll][Ee]\s+|$)', line_stripped)
        if song_match:
            save_current()
            
            current_num = int(song_match.group(1))
            current_title = song_match.group(2).strip()
            current_verses = {}
            current_vnum = None
            current_lines = []
            continue
        
        # Check for verse number (a line that is just a number)
        verse_match = re.match(r'^(\d+)$', line_stripped)
        if verse_match:
            # Save current verse if any
            if current_vnum is not None and current_lines:
                key = str(current_vnum)
                if key in current_verses:
                    current_verses[key] = current_verses[key] + current_lines
                else:
                    current_verses[key] = current_lines
            
            current_vnum = verse_match.group(1)
            current_lines = []
            continue
        
        # Check for "A. Jamina" or section headers
        if line_stripped in ['A. Jamina', 'A . Jamina']:
            continue
        
        # Check for song-specific markers like "Feo 1,2,3" or part names
        if 'Feo' in line_stripped and any(c.isdigit() for c in line_stripped):
            # This is a voice part indicator, it's still part of the lyrics
            if current_num is not None:
                current_lines.append(line_stripped)
            continue
        
        # Regular lyric line
        if current_num is not None:
            current_lines.append(line_stripped)

# Save last song
save_current()

print(f'Total songs extracted from PDF: {len(all_songs)}')

# Save parsed songs
import json
# Convert to serializable format
serializable = {}
for num, song in all_songs.items():
    serializable[num] = {
        'titre': song['titre'],
        'verses': {k: '\n'.join(v) for k, v in song['verses'].items()}
    }

with open('pdf_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(serializable, f, indent=2, ensure_ascii=False)

print('Saved to pdf_parsed.json')

# Print summary
nums = sorted(all_songs.keys())
print(f'Range: {nums[0]} - {nums[-1]}')
print(f'Sample: {nums[:5]} ... {nums[-5:]}')

# Find duplicate numbers
from collections import Counter
num_counts = Counter(nums)
dupes = {k: v for k, v in num_counts.items() if v > 1}
if dupes:
    print(f'Duplicate numbers: {dupes}')
