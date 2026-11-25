"""Compare baibolyMG_v2.html vs baiboly_mbp.html verse by verse.
Output: all verses where text differs.
"""
import re, json

def load_v2(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    p = html.find('window.BIBLE_DATA = ')
    js_start = p + len('window.BIBLE_DATA = ')

    def find_end(t, s):
        i = s; ins = False; esc = False; d = 0
        while i < len(t):
            c = t[i]
            if esc: esc = False; i += 1; continue
            if c == '\\' and ins: esc = True; i += 1; continue
            if c == '"': ins = not ins; i += 1; continue
            if not ins:
                if c in '[{': d += 1
                elif c in ']}':
                    d -= 1
                    if d == 0: return i + 1
            i += 1
        return len(t)

    je = find_end(html, js_start)
    return json.loads(html[js_start:je])

def load_mbp(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    book_pat = re.compile(r'<h2 class="book-title" id="(\w+)">([^<]+)</h2>')
    ch_pat = re.compile(r'<h3 class="chapter-title">Toku?o (\d+)</h3>')
    v_pat = re.compile(r'<p class="verse"><sup class="verse-num">(\d+)</sup>\s*(.*?)</p>', re.DOTALL)

    data = {}
    for bm in book_pat.finditer(html):
        code = bm.group(1)
        name = bm.group(2)
        start = bm.end()
        next_bm = book_pat.search(html, start)
        end = next_bm.start() if next_bm else len(html)
        section = html[start:end]
        data[code] = {'name': name, 'chapters': {}}
        for cm in ch_pat.finditer(section):
            ch = cm.group(1)
            ch_start = cm.end()
            next_cm = ch_pat.search(section, ch_start)
            ch_end = next_cm.start() if next_cm else len(section)
            ch_content = section[ch_start:ch_end]
            verses = {}
            for vm in v_pat.finditer(ch_content):
                v = vm.group(1)
                t = re.sub(r'\s+', ' ', vm.group(2).strip())
                verses[v] = t
            if verses:
                data[code]['chapters'][ch] = verses
    return data

def norm(t):
    return re.sub(r'\s+', ' ', t.strip())

# Load both
v2_raw = load_v2('baibolyMG_v2.html')
mbp_raw = load_mbp('output/baiboly_mbp.html')

# Build v2 lookup: (book_id, ch, v) -> text
v2_verses = {}
v2_book_names = {}
for t in v2_raw:
    for b in v2_raw[t]:
        bid = b['id']
        v2_book_names[bid] = b['name']
        for ch in b['chapters']:
            for v in b['chapters'][ch]:
                v2_verses[(bid, ch, v)] = b['chapters'][ch][v]

# Build MBP lookup similarly - but MBP uses codes, not names
# We need a mapping from MBP code to v2 book id
# Build it by matching on name
mbp_to_v2id = {}
for code, mbp_book in mbp_raw.items():
    mbp_name = mbp_book['name'].lower().strip()
    best_match = None
    for bid, vname in v2_book_names.items():
        if vname.lower().strip() == mbp_name:
            best_match = bid
            break
    if not best_match:
        # Fuzzy: first 5 chars
        for bid, vname in v2_book_names.items():
            if mbp_name[:5] == vname.lower().strip()[:5]:
                best_match = bid
                break
    if best_match:
        mbp_to_v2id[code] = best_match
    else:
        print(f'WARNING: No v2 match for MBP book {code} ({mbp_book["name"]})')

# Build MBP lookup
mbp_verses = {}
for code, mbp_book in mbp_raw.items():
    bid = mbp_to_v2id.get(code)
    if not bid:
        continue
    for ch in mbp_book['chapters']:
        for v in mbp_book['chapters'][ch]:
            mbp_verses[(bid, ch, v)] = mbp_book['chapters'][ch][v]

# Find all unique verse references
all_refs = sorted(set(list(v2_verses.keys()) + list(mbp_verses.keys())))

diff_only_v2 = []   # in v2 only
diff_only_mbp = []  # in MBP only
diff_text = []      # in both but different text

for ref in all_refs:
    bid, ch, v = ref
    t_v2 = v2_verses.get(ref, '')
    t_mbp = mbp_verses.get(ref, '')
    n_v2 = norm(t_v2)
    n_mbp = norm(t_mbp)

    if not t_v2 and t_mbp:
        diff_only_mbp.append(ref)
    elif t_v2 and not t_mbp:
        diff_only_v2.append(ref)
    elif n_v2 != n_mbp and t_v2 and t_mbp:
        diff_text.append(ref)

# Generate report
lines = []
lines.append('=' * 80)
lines.append('COMPARAISON baibolyMG_v2.html vs baiboly_mbp.html')
lines.append('=' * 80)
lines.append('')
lines.append(f'Versets dans v2 uniquement: {len(diff_only_v2)}')
lines.append(f'Versets dans MBP uniquement: {len(diff_only_mbp)}')
lines.append(f'Versets dans les DEUX mais texte DIFFÉRENT: {len(diff_text)}')
lines.append('')

# Books summary
from collections import Counter
book_diff_counts = Counter(ref[0] for ref in diff_text)
book_only_v2 = Counter(ref[0] for ref in diff_only_v2)
book_only_mbp = Counter(ref[0] for ref in diff_only_mbp)

all_books = set(list(book_diff_counts.keys()) + list(book_only_v2.keys()) + list(book_only_mbp.keys()))
lines.append('--- Résumé par livre ---')
lines.append(f'{"Livre":30s} {"Diff":>6s} {"V2 seul":>8s} {"MBP seul":>8s}')
lines.append('-' * 52)
for bid in sorted(all_books):
    name = v2_book_names.get(bid, bid)
    d = book_diff_counts.get(bid, 0)
    o2 = book_only_v2.get(bid, 0)
    om = book_only_mbp.get(bid, 0)
    if d + o2 + om > 0:
        lines.append(f'{name:30s} {d:6d} {o2:8d} {om:8d}')
lines.append('')

# Detailed diff: verses in both but different
lines.append('=' * 80)
lines.append('VERSETS DIFFÉRENTS (présents dans les deux fichiers, texte différent)')
lines.append('=' * 80)
lines.append(f'Total: {len(diff_text)}')
lines.append('')

for ref in diff_text:
    bid, ch, v = ref
    name = v2_book_names.get(bid, bid)
    t_v2 = v2_verses.get(ref, '')
    t_mbp = mbp_verses.get(ref, '')

    lines.append(f'--- {name} {ch}:{v} ---')
    # Truncate if too long but show full
    lines.append(f'  v2:  {t_v2}')
    lines.append(f'  mbp: {t_mbp}')
    lines.append('')

# Only in v2
lines.append('=' * 80)
lines.append('VERSETS PRÉSENTS UNIQUEMENT DANS v2')
lines.append('=' * 80)
lines.append(f'Total: {len(diff_only_v2)}')
lines.append('')
for ref in diff_only_v2:
    bid, ch, v = ref
    name = v2_book_names.get(bid, bid)
    t_v2 = v2_verses.get(ref, '')
    lines.append(f'{name} {ch}:{v} = {t_v2[:120]}')
lines.append('')

# Only in MBP
lines.append('=' * 80)
lines.append('VERSETS PRÉSENTS UNIQUEMENT DANS MBP')
lines.append('=' * 80)
lines.append(f'Total: {len(diff_only_mbp)}')
lines.append('')
for ref in diff_only_mbp:
    bid, ch, v = ref
    name = v2_book_names.get(bid, bid)
    t_mbp = mbp_verses.get(ref, '')
    lines.append(f'{name} {ch}:{v} = {t_mbp[:120]}')
lines.append('')

report = '\n'.join(lines)

# Write to file
with open('comparison_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

# Also print summary
print(report[:3000])
print(f'\n... (report continued in comparison_report.txt, {len(lines)} lines, {len(report)//1024} KB)')
