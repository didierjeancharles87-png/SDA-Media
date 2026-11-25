#!/usr/bin/env python3
"""Verify the output HTML and fix any missing chapters."""
import os
import urllib.request
import re
import html as html_mod

# Check which chapters might have failed
errors = {
    'NUM': 12,
    'DEU': 23,
    '2CH': 31,
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for code, ch in errors.items():
    path = f'bible_cache/{code}.{ch}.html'
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f'{code}.{ch}: already cached ({os.path.getsize(path)} bytes)')
    else:
        print(f'{code}.{ch}: retrying fetch...')
        url = f'https://www.bible.com/fr/bible/873/{code}.{ch}.MBP'
        req = urllib.request.Request(url, headers=headers)
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            data = resp.read().decode('utf-8', errors='replace')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(data)
            print(f'  -> {len(data)} bytes saved')
        except Exception as e:
            print(f'  ERROR: {e}')

# Verify output file
output = 'output/baiboly_mbp.html'
size = os.path.getsize(output)
print(f'\nOutput file: {size/1024/1024:.1f} MB')

with open(output, 'r', encoding='utf-8') as f:
    content = f.read()
    error_cnt = content.count('Tsy hita')
    print(f'Error messages ("Tsy hita"): {error_cnt}')
    
    for keyword in ['Genesisy', 'Toko 1', 'Salamo', 'Matio', 
                    'TESTAMENTA TALOHA', 'TESTAMENTA VAOVAO',
                    'Apokalipsy', 'Toko 22']:
        count = content.count(keyword)
        print(f'  "{keyword}": {count} occurrences')
    
    # Count verse numbers present
    verse_nums = len(re.findall(r'<sup class="verse-num">(\d+)</sup>', content))
    print(f'\nTotal verse tags found: {verse_nums}')
    
    # Count books
    books = len(re.findall(r'<h2 class="book-title" id="\w+">', content))
    print(f'Books found: {books}')

print('\nVerification complete!')
