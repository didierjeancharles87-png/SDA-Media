#!/usr/bin/env python3
"""Quick test: fetch first chapter and parse verses."""

import urllib.request
import re
import html as html_mod
import os

os.makedirs('bible_cache', exist_ok=True)
os.makedirs('output', exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Test 1: Fetch Gen 1
print("Fetching GEN.1...")
url = 'https://www.bible.com/fr/bible/873/GEN.1.MBP'
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=30)
data = resp.read().decode('utf-8', errors='replace')

with open('bible_cache/GEN.1.html', 'w', encoding='utf-8') as f:
    f.write(data)
print(f'GEN.1 fetched: {len(data)} bytes')

# Test 2: Parse verses using data-usfm pattern
pattern = re.compile(
    r'<span[^>]*data-usfm="GEN\.1\.(\d+)"[^>]*>'
    r'.*?<span[^>]*class="[^"]*label[^"]*"[^>]*>(\d+)</span>'
    r'\s*<span[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</span>',
    re.DOTALL
)
verses = []
for match in pattern.finditer(data):
    vnum = match.group(1)
    text = match.group(3)
    text = re.sub(r'<[^>]+>', '', text)
    text = html_mod.unescape(text)
    text = text.strip()
    if text:
        verses.append((vnum, text))

print(f'Found {len(verses)} verses in GEN.1')
for vn, vt in verses[:3]:
    print(f'  {vn}: {vt[:80]}')
if len(verses) > 3:
    print('  ...')
    for vn, vt in verses[-2:]:
        print(f'  {vn}: {vt[:80]}')

# Test 3: Try also fetching Mat 1
print("\nFetching MAT.1...")
url2 = 'https://www.bible.com/fr/bible/873/MAT.1.MBP'
req2 = urllib.request.Request(url2, headers=headers)
resp2 = urllib.request.urlopen(req2, timeout=30)
data2 = resp2.read().decode('utf-8', errors='replace')

with open('bible_cache/MAT.1.html', 'w', encoding='utf-8') as f:
    f.write(data2)
print(f'MAT.1 fetched: {len(data2)} bytes')

pattern2 = re.compile(
    r'<span[^>]*data-usfm="MAT\.1\.(\d+)"[^>]*>'
    r'.*?<span[^>]*class="[^"]*label[^"]*"[^>]*>(\d+)</span>'
    r'\s*<span[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</span>',
    re.DOTALL
)
verses2 = []
for match in pattern2.finditer(data2):
    vnum = match.group(1)
    text = match.group(3)
    text = re.sub(r'<[^>]+>', '', text)
    text = html_mod.unescape(text)
    text = text.strip()
    if text:
        verses2.append((vnum, text))

print(f'Found {len(verses2)} verses in MAT.1')
for vn, vt in verses2[:3]:
    print(f'  {vn}: {vt[:80]}')
