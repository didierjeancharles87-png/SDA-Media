"""
Find correct numbering for extra songs by checking PDF page ordering.
"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('pdf_all_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Duplicate numbers and their positions (from earlier output)
dups_positions = {
    27: [18189, 173922],
    100: [67479, 73457],
    218: [140309, 333901],
    260: [166066, 166703],
    334: [210643, 275106],
    343: [215249, 216059],
    480: [310002, 310590],
    723: [471201, 478105],
}

# For each duplicate pair, show what song numbers come BEFORE and AFTER each occurrence
for num in sorted(dups_positions.keys()):
    occ = dups_positions[num]
    print('=== Song ' + str(num) + ' duplicates ===')
    
    # Get titles
    pattern = re.compile(r'(?:^|\n)[ \t]*(\d+)\.[ \t]+(.+?)(?:[ \t]*$)', re.MULTILINE)
    
    for idx, pos in enumerate(occ):
        # What's just before this occurrence?
        matches_before = list(pattern.finditer(text[:pos]))
        if matches_before:
            prev = matches_before[-1]
            prev_num = int(prev.group(1))
            prev_title = prev.group(2).strip()[:50]
        else:
            prev_num = 'START'
            prev_title = ''
        
        # What's just after?
        after_text = text[pos+1:pos+2000]
        matches_after = list(pattern.finditer(after_text))
        next_entries = []
        for i, m in enumerate(matches_after[:3]):
            next_num = int(m.group(1))
            next_title = m.group(2).strip()[:50]
            next_entries.append(str(next_num) + ': ' + next_title)
        
        # Get the title of this occurrence
        this_match = pattern.search(text[pos:pos+200])
        if this_match:
            this_title = this_match.group(2).strip()[:50]
        
        print(f'  [{idx}] pos={pos}')
        print(f'    Title: {this_title}')
        print(f'    Previous song: {prev_num}: {prev_title}')
        print(f'    Next songs: {", ".join(next_entries[:2])}')
    
    print()
