import re
import json
import os
import sys

WORK_DIR = r'G:\SDA\fihirana'

MD_FILES = [
    'BibleMalagasy-at01-Genese-Genesisy.md',
    'BibleMalagasy-at02-Exode-Eksodosy.md',
    'BibleMalagasy-at03-Levitique-Levitikosy.md',
    'BibleMalagasy-at04-Nombres-Nomery.md',
    'BibleMalagasy-at11-1Rois-1Mpanjaka.md',
    'BibleMalagasy-at13-1Chroniques-1Tantara.md',
    'BibleMalagasy-at16-Nehemie-Nehemia.md',
    'BibleMalagasy-at18-Job-Joba.md',
    'BibleMalagasy-at19-Psaumes-Salamo.md',
    'BibleMalagasy-at26-Ezechiel-Ezekiela.md',
    'BibleMalagasy-at27-Daniel-Daniela.md',
]

def parse_md(filepath):
    chapters = {}
    current_chapter = None
    book_name = None
    book_name_read = False

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            raw = line
            line = line.strip()

            if not book_name_read and line.startswith('# '):
                book_name = line[2:].strip()
                book_name_read = True

            if not line:
                continue

            if line.startswith('#') or line.startswith('>') or line.startswith('Accès'):
                continue

            if line.startswith('LIVRE') or line == '*' or line.startswith('Psaume'):
                continue

            ch_match = re.match(r'^Chapitre (\d+)$', line)
            ps_match = re.match(r'^PSAUME (\d+)\*?$', line)

            if ch_match:
                current_chapter = int(ch_match.group(1))
                chapters[current_chapter] = {}
                continue
            elif ps_match:
                current_chapter = int(ps_match.group(1))
                chapters[current_chapter] = {}
                continue

            if current_chapter is not None:
                verse_match = re.match(r'^(\d+)\s+(.*)', line)
                if verse_match:
                    verse_num = int(verse_match.group(1))
                    verse_text = verse_match.group(2).strip()
                    if verse_text:
                        chapters[current_chapter][verse_num] = verse_text

    return book_name, chapters


def extract_json(line, start):
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(line)):
        ch = line[i]
        if escape:
            escape = False
        elif ch == '\\' and in_string:
            escape = True
        elif ch == '"':
            in_string = not in_string
        elif not in_string:
            if ch == '{' or ch == '[':
                depth += 1
            elif ch == '}' or ch == ']':
                depth -= 1
                if depth == 0:
                    return line[start:i+1]
        if i > start + 6000000:
            raise ValueError("JSON too long without closing")
    raise ValueError("Could not find end of JSON")


def main():
    os.chdir(WORK_DIR)

    print("Reading HTML...")
    with open('baibolyMG_v2.html', 'r', encoding='utf-8') as f:
        html = f.read()

    lines = html.split('\n')
    bible_idx = None
    for i, line in enumerate(lines):
        if 'window.BIBLE_DATA' in line and '=' in line:
            bible_idx = i
            break

    if bible_idx is None:
        print("ERROR: BIBLE_DATA line not found")
        sys.exit(1)

    line = lines[bible_idx]
    prefix = 'window.BIBLE_DATA = '
    start = line.index(prefix) + len(prefix)

    print("Extracting JSON...")
    json_str = extract_json(line, start)

    print("Parsing JSON...")
    data = json.loads(json_str)

    for md_file in MD_FILES:
        md_path = os.path.join(WORK_DIR, md_file)
        if not os.path.exists(md_path):
            print(f"SKIP: {md_file} not found")
            continue

        print(f"\n=== {md_file} ===")
        book_name, chapters = parse_md(md_path)

        if not book_name:
            print(f"  ERROR: Could not read book name")
            continue

        print(f"  Book: {book_name}")
        print(f"  Chapters parsed: {len(chapters)}")

        book_found = None
        for book in data['testamenta_taloha']:
            if book['name'] == book_name:
                book_found = book
                break

        if book_found is None:
            print(f"  ERROR: '{book_name}' not found in BIBLE_DATA")
            continue

        saved_ch37 = None
        if book_name == 'Salamo':
            old_ch37 = book_found['chapters'].get('37')
            if old_ch37:
                saved_ch37 = old_ch37
                print(f"  Saved original Salamo chapter 37 ({len(saved_ch37)} verses)")

        chapters_str = {}
        for ch_num in sorted(chapters.keys()):
            ch_key = str(ch_num)
            verses = chapters[ch_num]
            verses_str = {}
            for v_num in sorted(verses.keys()):
                verses_str[str(v_num)] = verses[v_num]
            chapters_str[ch_key] = verses_str

        old_count = book_found['chapter_count']
        book_found['chapters'] = chapters_str
        book_found['chapter_count'] = len(chapters_str)

        if saved_ch37 is not None:
            book_found['chapters']['37'] = saved_ch37
            print(f"  Restored Salamo chapter 37")

        total_verses = sum(len(v) for v in chapters_str.values())
        print(f"  Updated: {book_found['chapter_count']} chapters, {total_verses} verses")
        print(f"  (was {old_count} chapters)")

    print("\nSerializing JSON...")
    new_json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    new_line = prefix + new_json_str + ';'
    lines[bible_idx] = new_line
    new_html = '\n'.join(lines)

    print("Writing HTML...")
    with open('baibolyMG_v2.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    print("\nDone! All 11 books replaced.")


if __name__ == '__main__':
    main()
