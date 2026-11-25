"""Find words genuinely missing in V2 (filter out footnotes & dialect)."""
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

def strip_footnotes(t):
    """Remove MBP footnote references starting with #"""
    t = re.sub(r'#.*', '', t)  # strip from # to end
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def normalize_dialect(t):
    """Normalize dialect variations"""
    t = re.sub(r'\bhianareo\b', 'ianareo', t)
    t = re.sub(r'\bhianao\b', 'ianao', t)
    t = re.sub(r'\bhianareo\b', 'ianareo', t)
    t = re.sub(r'\bhianao\b', 'ianao', t)
    t = re.sub(r'\bHianareo\b', 'Ianareo', t)
    t = re.sub(r'\bHianao\b', 'Ianao', t)
    t = re.sub(r'\bHianareo\b', 'Ianareo', t)
    t = re.sub(r'\bHianao\b', 'Ianao', t)
    return t

def compare_texts(t_v2, t_mbp):
    """Compare after normalizing."""
    a = strip_footnotes(t_mbp)
    a = normalize_dialect(a)
    b = normalize_dialect(t_v2)
    a = re.sub(r'\s+', ' ', a).strip()
    b = re.sub(r'\s+', ' ', b).strip()
    return a, b

v2_raw = load_v2('baibolyMG_v2.html')
mbp_raw = load_mbp('output/baiboly_mbp.html')

v2_verses = {}
v2_book_names = {}
for t in v2_raw:
    for b in v2_raw[t]:
        bid = b['id']
        v2_book_names[bid] = b['name']
        for ch in b['chapters']:
            for v in b['chapters'][ch]:
                v2_verses[(bid, ch, v)] = b['chapters'][ch][v]

mbp_to_v2id = {}
for code, mbp_book in mbp_raw.items():
    mbp_name = mbp_book['name'].lower().strip()
    for bid, vname in v2_book_names.items():
        if vname.lower().strip() == mbp_name:
            mbp_to_v2id[code] = bid
            break

mbp_verses = {}
for code, mbp_book in mbp_raw.items():
    bid = mbp_to_v2id.get(code)
    if not bid:
        continue
    for ch in mbp_book['chapters']:
        for v in mbp_book['chapters'][ch]:
            mbp_verses[(bid, ch, v)] = mbp_book['chapters'][ch][v]

all_refs = sorted(set(list(v2_verses.keys()) + list(mbp_verses.keys())))

genuinely_missing = []

for ref in all_refs:
    bid, ch, v = ref
    t_v2 = v2_verses.get(ref, '')
    t_mbp_raw = mbp_verses.get(ref, '')
    name = v2_book_names.get(bid, bid)

    if not t_v2 and t_mbp_raw:
        # Verse only in MBP - but check if after stripping footnotes it's non-empty
        t_mbp = strip_footnotes(t_mbp_raw)
        if len(t_mbp.split()) >= 3:
            genuinely_missing.append((bid, name, ch, v, '[Verset entier manquant]', t_mbp_raw, t_mbp))
        continue

    if not t_v2 or not t_mbp_raw:
        continue

    # Compare with normalization
    t_mbp_clean, t_v2_norm = compare_texts(t_v2, t_mbp_raw)
    t_mbp_norm = normalize_dialect(strip_footnotes(t_mbp_raw))

    # Also strip * from V2 for fair comparison
    t_v2_clean = re.sub(r'[*]', '', t_v2_norm)

    w_v2 = len(t_v2_clean.split())
    w_mbp = len(t_mbp_norm.split())

    if w_mbp <= w_v2 + 1:  # allow 1 word difference for minor variations
        continue

    # Find actual extra words
    v2_words = set(t_v2_clean.lower().split())
    mbp_words = set(t_mbp_norm.lower().split())
    extra = mbp_words - v2_words

    # Filter out punctuation-only extras
    extra = {w for w in extra if re.search(r'[a-zàâéèêëîôûù]', w)}
    if not extra:
        continue

    # Minimum difference of 2+ significant words
    if len(extra) < 2:
        # Check total word count difference
        if w_mbp - w_v2 < 3:
            continue

    genuinely_missing.append((bid, name, ch, v, w_v2, w_mbp, sorted(extra), t_v2_clean[:200], t_mbp_norm[:200]))

from collections import Counter
book_counts = Counter(item[1] for item in genuinely_missing)

lines = []
lines.append('=' * 80)
lines.append('VERSETS OÙ V2 A DES MOTS MANQUANTS (vs MBP, après filtrage notes et dialecte)')
lines.append('=' * 80)
lines.append(f'Total: {len(genuinely_missing)}')
lines.append('')
lines.append('--- Répartition par livre ---')
lines.append(f'{"Livre":35s} {"Nb":>6s} {"Mots v2":>8s} {"Mots mbp":>8s}')
lines.append('-' * 57)
for name in sorted(book_counts.keys()):
    items = [x for x in genuinely_missing if x[1] == name]
    cnt = len(items)
    wv = sum(x[4] for x in items if isinstance(x[4], (int, float)))
    wm = sum(x[5] for x in items if isinstance(x[5], (int, float)))
    lines.append(f'{name:35s} {cnt:6d} {wv:8d} {wm:8d}')
lines.append('')

for item in genuinely_missing:
    if len(item) == 9:  # verse with word comparison
        bid, name, ch, v, wv, wm, extra, t_v2, t_mbp = item
        lines.append(f'--- {name} {ch}:{v} (v2:{wv}mots, mbp:{wm}mots) ---')
        lines.append(f'  Mots en plus dans MBP: {", ".join(extra[:20])}')
        lines.append(f'  v2:  {t_v2}')
        lines.append(f'  mbp: {t_mbp}')
    elif len(item) == 7:  # verse only in MBP
        bid, name, ch, v, label, t_raw, t_clean = item
        lines.append(f'--- {name} {ch}:{v} ---')
        lines.append(f'  {label}')
        lines.append(f'  mbp (brut): {t_raw[:200]}')
        lines.append(f'  mbp (propre): {t_clean[:200]}')
    lines.append('')

report = '\n'.join(lines)
with open('v2_genuinely_missing.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(f'Report: v2_genuinely_missing.txt ({len(lines)} lines)')
print(f'Versets avec mots manquants: {len(genuinely_missing)}')

if genuinely_missing:
    print('\nApercu (10 premiers):')
    for item in genuinely_missing[:10]:
        if len(item) == 9:
            bid, name, ch, v, wv, wm, extra, tv, tm = item
            print(f'  {name} {ch}:{v} - {", ".join(extra[:5])}')
        elif len(item) == 7:
            bid, name, ch, v, label, traw, tclean = item
            print(f'  {name} {ch}:{v} - {label}')
