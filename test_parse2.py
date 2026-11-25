#!/usr/bin/env python3
"""Test updated verse parsing."""
import re, html as html_mod

with open('bible_cache/GEN.1.html', 'r', encoding='utf-8') as f:
    data = f.read()

pattern = re.compile(
    r'<span[^>]*data-usfm="GEN\.1\.(\d+)"[^>]*>'
    r'\s*<span[^>]*class="[^"]*label[^"]*"[^>]*>(\d+)</span>'
    r'\s*<span[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</span>'
    r'\s*</span>',
    re.DOTALL
)

verses = {}
for match in pattern.finditer(data):
    vnum = match.group(1)
    text = match.group(3)
    text = re.sub(r'<[^>]+>', '', text)
    text = html_mod.unescape(text)
    text = text.strip()
    if text:
        if vnum in verses:
            verses[vnum] += " " + text
        else:
            verses[vnum] = text

result = sorted(verses.items(), key=lambda x: int(x[0]))
print(f"Found {len(result)} verses in GEN.1")
for vn, vt in result[:5]:
    print(f'  {vn}: {vt[:100]}')
print('  ...')
for vn, vt in result[-3:]:
    print(f'  {vn}: {vt[:100]}')

# Test MAT.1
with open('bible_cache/MAT.1.html', 'r', encoding='utf-8') as f:
    data2 = f.read()

pattern2 = re.compile(
    r'<span[^>]*data-usfm="MAT\.1\.(\d+)"[^>]*>'
    r'\s*<span[^>]*class="[^"]*label[^"]*"[^>]*>(\d+)</span>'
    r'\s*<span[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</span>'
    r'\s*</span>',
    re.DOTALL
)

verses2 = {}
for match in pattern2.finditer(data2):
    vnum = match.group(1)
    text = match.group(3)
    text = re.sub(r'<[^>]+>', '', text)
    text = html_mod.unescape(text)
    text = text.strip()
    if text:
        if vnum in verses2:
            verses2[vnum] += " " + text
        else:
            verses2[vnum] = text

result2 = sorted(verses2.items(), key=lambda x: int(x[0]))
print(f"\nFound {len(result2)} verses in MAT.1")
for vn, vt in result2[:3]:
    print(f'  {vn}: {vt[:100]}')
print('  ...')

# Test PSA.119 (should have many verses)
with open('bible_cache/PSA.119.html', 'r', encoding='utf-8') as f:
    pass
# Fetch if not cached
if False:
    pass

# Also test a chapter from later books
print("\nFetching REV.22...")
import urllib.request
headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://www.bible.com/fr/bible/873/REV.22.MBP'
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=30)
data3 = resp.read().decode('utf-8', errors='replace')

pattern3 = re.compile(
    r'<span[^>]*data-usfm="REV\.22\.(\d+)"[^>]*>'
    r'\s*<span[^>]*class="[^"]*label[^"]*"[^>]*>(\d+)</span>'
    r'\s*<span[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</span>'
    r'\s*</span>',
    re.DOTALL
)

verses3 = {}
for match in pattern3.finditer(data3):
    vnum = match.group(1)
    text = match.group(3)
    text = re.sub(r'<[^>]+>', '', text)
    text = html_mod.unescape(text)
    text = text.strip()
    if text:
        if vnum in verses3:
            verses3[vnum] += " " + text
        else:
            verses3[vnum] = text

result3 = sorted(verses3.items(), key=lambda x: int(x[0]))
print(f"Found {len(result3)} verses in REV.22")
for vn, vt in result3[:3]:
    print(f'  {vn}: {vt[:100]}')
print('  ...')
for vn, vt in result3[-2:]:
    print(f'  {vn}: {vt[:100]}')
