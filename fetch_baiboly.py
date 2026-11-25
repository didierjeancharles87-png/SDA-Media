#!/usr/bin/env python3
"""Fetch complete MBP Malagasy Protestant Bible and generate HTML."""

import urllib.request
import urllib.error
import re
import html as html_mod
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# === BOOK DATA: code, malagasy_name, chapters ===
BOOKS = [
    # Old Testament
    ("GEN", "Genesisy", 50),
    ("EXO", "Eksodosy", 40),
    ("LEV", "Levitikosy", 27),
    ("NUM", "Nomery", 36),
    ("DEU", "Deoteronomia", 34),
    ("JOS", "Josoa", 24),
    ("JDG", "Mpitsara", 21),
    ("RUT", "Rota", 4),
    ("1SA", "1 Samoela", 31),
    ("2SA", "2 Samoela", 24),
    ("1KI", "1 Mpanjaka", 22),
    ("2KI", "2 Mpanjaka", 25),
    ("1CH", "1 Tantara", 29),
    ("2CH", "2 Tantara", 36),
    ("EZR", "Ezra", 10),
    ("NEH", "Nehemia", 13),
    ("EST", "Estera", 10),
    ("JOB", "Joba", 42),
    ("PSA", "Salamo", 150),
    ("PRO", "Ohabolana", 31),
    ("ECC", "Mpitoriteny", 12),
    ("SNG", "Tononkiran'i Solomona", 8),
    ("ISA", "Isaia", 66),
    ("JER", "Jeremia", 52),
    ("LAM", "Fitomaniana", 5),
    ("EZK", "Ezekiela", 48),
    ("DAN", "Daniela", 12),
    ("HOS", "Hosea", 14),
    ("JOL", "Joela", 3),
    ("AMO", "Amosa", 9),
    ("OBA", "Obadia", 1),
    ("JON", "Jona", 4),
    ("MIC", "Mika", 7),
    ("NAM", "Nahoma", 3),
    ("HAB", "Habakoka", 3),
    ("ZEP", "Zefania", 3),
    ("HAG", "Hagay", 2),
    ("ZEC", "Zakaria", 14),
    ("MAL", "Malakia", 4),
    # New Testament
    ("MAT", "Matio", 28),
    ("MRK", "Marka", 16),
    ("LUK", "Lioka", 24),
    ("JHN", "Jaona", 21),
    ("ACT", "Asan'ny Apostoly", 28),
    ("ROM", "Romana", 16),
    ("1CO", "1 Korintiana", 16),
    ("2CO", "2 Korintiana", 13),
    ("GAL", "Galatiana", 6),
    ("EPH", "Efesiana", 6),
    ("PHP", "Filipiana", 4),
    ("COL", "Kolosiana", 4),
    ("1TH", "1 Tesaloniana", 5),
    ("2TH", "2 Tesaloniana", 3),
    ("1TI", "1 Timoty", 6),
    ("2TI", "2 Timoty", 4),
    ("TIT", "Titosy", 3),
    ("PHM", "Filemona", 1),
    ("HEB", "Hebreo", 13),
    ("JAS", "Jakoba", 5),
    ("1PE", "1 Petera", 5),
    ("2PE", "2 Petera", 3),
    ("1JN", "1 Jaona", 5),
    ("2JN", "2 Jaona", 1),
    ("3JN", "3 Jaona", 1),
    ("JUD", "Joda", 1),
    ("REV", "Apokalipsy", 22),
]

CACHE_DIR = "bible_cache"
URL_TEMPLATE = "https://www.bible.com/fr/bible/873/{code}.{ch}.MBP"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
WRITE_LOCK = Lock()
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs("output", exist_ok=True)


def fetch_chapter(code, ch):
    """Fetch a single chapter from bible.com."""
    url = URL_TEMPLATE.format(code=code, ch=ch)
    cache_file = os.path.join(CACHE_DIR, f"{code}.{ch}.html")
    
    # Check cache first
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()
    
    # Fetch from web
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8", errors="replace")
            # Cache it
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(data)
            return data
    except Exception as e:
        print(f"  ERROR fetching {code}.{ch}: {e}")
        return None


def parse_verses_from_html(html_content, code, ch):
    """Parse verse labels and text from HTML content."""
    if not html_content:
        return []
    
    verses = {}
    
    # Pattern: match complete verse spans that contain BOTH label and content
    # Uses \s* between opening and label span to avoid cross-verse matching
    verse_pattern = re.compile(
        r'<span[^>]*data-usfm="' + re.escape(code) + r'\.' + str(ch) + r'\.(\d+)"[^>]*>'
        r'\s*<span[^>]*class="[^"]*label[^"]*"[^>]*>(\d+)</span>'
        r'\s*<span[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</span>'
        r'\s*</span>',
        re.DOTALL
    )
    
    for match in verse_pattern.finditer(html_content):
        verse_num = match.group(1)
        label = match.group(2)
        text = match.group(3)
        text = re.sub(r'<[^>]+>', '', text)
        text = html_mod.unescape(text)
        text = text.strip()
        if text:
            if verse_num in verses:
                verses[verse_num] += " " + text
            else:
                verses[verse_num] = text
    
    # Sort by verse number
    result = sorted(verses.items(), key=lambda x: int(x[0]))
    return result


def process_book(code, name, chapters, progress, total):
    """Process all chapters of a book, return book HTML."""
    book_html_parts = []
    book_html_parts.append(f'<div class="book">')
    book_html_parts.append(f'<h2 class="book-title" id="{code}">{name}</h2>')
    
    # Fetch all chapters in parallel using thread pool
    chapter_results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        fut_map = {}
        for ch in range(1, chapters + 1):
            fut = executor.submit(fetch_chapter, code, ch)
            fut_map[fut] = ch
        
        for fut in as_completed(fut_map):
            ch = fut_map[fut]
            chapter_results[ch] = fut.result()
            with WRITE_LOCK:
                progress[0] += 1
                done = progress[0]
                print(f"[{done}/{total}] {name} {ch}")
    
    for ch in range(1, chapters + 1):
        html_content = chapter_results.get(ch)
        if not html_content:
            book_html_parts.append(f'<div class="chapter"><h3>Toko {ch}</h3><p class="error">Tsy hita</p></div>')
            continue
        
        verses = parse_verses_from_html(html_content, code, ch)
        
        if not verses:
            book_html_parts.append(f'<div class="chapter"><h3>Toko {ch}</h3><p class="error">Tsy hita ny andininy</p></div>')
            continue
        
        book_html_parts.append(f'<div class="chapter">')
        book_html_parts.append(f'<h3 class="chapter-title">Toko {ch}</h3>')
        
        for vnum, vtext in verses:
            book_html_parts.append(f'<p class="verse"><sup class="verse-num">{vnum}</sup> {vtext}</p>')
        
        book_html_parts.append(f'</div>')
    
    book_html_parts.append(f'</div>')
    return '\n'.join(book_html_parts)


def main():
    total_chapters = sum(b[2] for b in BOOKS)
    progress = [0]
    
    print(f"Total chapters to fetch: {total_chapters}")
    print(f"Total books: {len(BOOKS)}")
    print()
    
    # HTML header
    html_parts = []
    html_parts.append('''<!DOCTYPE html>
<html lang="mg">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Baiboly Masina - Protestanta Malagasy (MBP)</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #f5f5f5;
    color: #222;
    line-height: 1.8;
  }
  .container {
    max-width: 800px;
    margin: 0 auto;
    background: #fff;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
  }
  .header {
    background: #2c3e50;
    color: white;
    padding: 40px 30px;
    text-align: center;
  }
  .header h1 { font-size: 2em; margin-bottom: 8px; }
  .header p { opacity: 0.85; font-size: 0.95em; }
  .nav {
    background: #34495e;
    padding: 12px 20px;
    position: sticky;
    top: 0;
    z-index: 100;
    text-align: center;
  }
  .nav select {
    padding: 8px 16px;
    font-size: 1em;
    border-radius: 4px;
    border: none;
    max-width: 100%;
  }
  .content { padding: 20px 30px 60px; }
  .testament-label {
    background: #e74c3c;
    color: white;
    padding: 12px 20px;
    margin: 30px 0 20px;
    font-size: 1.2em;
    border-radius: 4px;
    text-align: center;
  }
  .testament-label.ot { background: #2980b9; }
  .testament-label.nt { background: #c0392b; }
  .book {
    margin-bottom: 40px;
    page-break-before: always;
  }
  .book-title {
    font-size: 1.5em;
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
    padding-bottom: 8px;
    margin: 30px 0 20px;
    cursor: pointer;
  }
  .book-title:hover { color: #3498db; }
  .chapter {
    margin-bottom: 25px;
    padding: 15px 0;
  }
  .chapter-title {
    font-size: 1.15em;
    color: #7f8c8d;
    margin-bottom: 12px;
    font-weight: 600;
  }
  .verse {
    margin-bottom: 4px;
    text-align: justify;
    font-size: 1.05em;
  }
  .verse .verse-num {
    font-size: 0.7em;
    vertical-align: super;
    line-height: 1;
    color: #e74c3c;
    font-weight: bold;
    margin-right: 3px;
  }
  .footer {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 25px;
    font-size: 0.85em;
  }
  @media print {
    .nav { display: none; }
    .container { box-shadow: none; }
    .book { page-break-before: always; }
  }
</style>
</head>
<body>
<div class="container">
<div class="header">
  <h1>Baiboly Masina</h1>
  <p>Ny Baiboly Protestanta Malagasy (MBP) — Fivadihan'ny Baiboly</p>
</div>
<div class="nav">
  <select id="book-nav" onchange="document.getElementById(this.value).scrollIntoView({behavior:'smooth'})">
    <option value="">-- Safidio ny boky --</option>''')
    
    # Add OT books to nav
    html_parts.append('<optgroup label="--- Testamenta Taloha ---">')
    for code, name, _ in BOOKS[:39]:
        html_parts.append(f'<option value="{code}">{name}</option>')
    html_parts.append('</optgroup>')
    
    # Add NT books to nav
    html_parts.append('<optgroup label="--- Testamenta Vaovao ---">')
    for code, name, _ in BOOKS[39:]:
        html_parts.append(f'<option value="{code}">{name}</option>')
    html_parts.append('</optgroup>')
    
    html_parts.append('''  </select>
</div>
<div class="content">''')
    
    # Open output file for streaming
    output_file = "output/baiboly_mbp.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('\n'.join(html_parts))
        f.write('\n')
        
        # Process Old Testament
        f.write('<div class="testament-label ot">TESTAMENTA TALOHA</div>\n')
        for idx, (code, name, chapters) in enumerate(BOOKS[:39]):
            print(f"\n--- {name} ({code}) ---")
            book_html = process_book(code, name, chapters, progress, total_chapters)
            f.write(book_html)
            f.write('\n')
            f.flush()
        
        # Process New Testament
        f.write('<div class="testament-label nt">TESTAMENTA VAOVAO</div>\n')
        for idx, (code, name, chapters) in enumerate(BOOKS[39:]):
            print(f"\n--- {name} ({code}) ---")
            book_html = process_book(code, name, chapters, progress, total_chapters)
            f.write(book_html)
            f.write('\n')
            f.flush()
        
        # Footer
        f.write('''</div>
<div class="footer">
  <p>Baiboly Protestanta Malagasy (MBP)</p>
  <p>Nalaina tao amin\'ny <a href="https://www.bible.com/fr/bible/873" style="color:#3498db;">YouVersion Bible.com</a></p>
  <p>Fivadihan\'ny Baiboly &copy; Malagasy Bible Society</p>
</div>
</div>
<script>
document.getElementById("book-nav").addEventListener("change", function() {
  var id = this.value;
  if (id) {
    var el = document.getElementById(id);
    if (el) el.scrollIntoView({behavior: "smooth"});
  }
});
</script>
</body>
</html>''')
    
    print("\n\n=== VITA! ===")
    print(f"Output: {output_file}")
    file_size = os.path.getsize(output_file)
    print(f"File size: {file_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
