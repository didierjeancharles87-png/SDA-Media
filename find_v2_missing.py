"""Find words missing in V2 compared to MBP."""
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

def clean(t):
    t = re.sub(r'[*#]\d*\.?\d*[^.;,!?]*[.;,!?]', '', t)
    t = re.sub(r'[*#]', '', t)
    t = t.replace('\u2019', "'").replace('\u2018', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t

def word_overlap(t1, t2):
    w1 = set(clean(t1).split())
    w2 = set(clean(t2).split())
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / len(w1 | w2)

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

MIN_WORD_OVERLAP = 0.40  # must share 40% words to be same verse
MIN_MBP_WORDS = 5        # MBP must have at least this many words

v2_missing_words = []      # same verse, MBP has more words
v2_missing_verses = []     # verse exists in MBP but not in V2
v2_missing_chapters = []   # chapter exists in MBP but not in V2

# 1. Same verse: MBP has more words
all_refs = sorted(set(list(v2_verses.keys()) + list(mbp_verses.keys())))
for ref in all_refs:
    bid, ch, v = ref
    t_v2 = v2_verses.get(ref, '')
    t_mbp = mbp_verses.get(ref, '')
    name = v2_book_names.get(bid, bid)

    if not t_v2 and t_mbp:
        # Verse only in MBP
        if len(t_mbp.split()) >= MIN_MBP_WORDS:
            v2_missing_verses.append((bid, name, ch, v, t_mbp))
        continue

    if not t_v2 or not t_mbp:
        continue

    w_v2 = len(norm(t_v2).split())
    w_mbp = len(norm(t_mbp).split())

    if w_mbp <= w_v2:
        continue  # MBP is shorter or equal, no words missing in V2

    if w_mbp - w_v2 < 3:
        continue  # less than 3 words difference, not significant

    # Check they're the same verse (word overlap)
    score = word_overlap(t_v2, t_mbp)
    if score < MIN_WORD_OVERLAP:
        continue  # different verses, skip

    # Find the missing words in V2
    mbp_words = norm(t_mbp).split()
    v2_words = norm(t_v2).split()

    # Find the extra words in MBP
    v2_set = set(clean(t_v2).split())
    mbp_set = set(clean(t_mbp).split())
    extra = mbp_set - v2_set

    v2_missing_words.append((bid, name, ch, v, w_v2, w_mbp, score, t_v2, t_mbp, sorted(extra)[:15]))

# 2. Chapter exists in MBP but not in V2
mbp_books_by_v2id = {}
for code, mbp_book in mbp_raw.items():
    bid = mbp_to_v2id.get(code)
    if bid:
        mbp_books_by_v2id[bid] = mbp_book

for bid, vname in v2_book_names.items():
    v2_chapters = set()
    for t in v2_raw:
        for b in v2_raw[t]:
            if b['id'] == bid:
                v2_chapters = set(b['chapters'].keys())
                break
    mbp_book = mbp_books_by_v2id.get(bid)
    if not mbp_book:
        continue
    for ch in mbp_book['chapters']:
        if ch not in v2_chapters:
            v2_missing_chapters.append((bid, vname, ch, len(mbp_book['chapters'][ch])))

# Generate report
lines = []
lines.append('=' * 80)
lines.append('MOTS MANQUANTS DANS V2 PAR RAPPORT À MBP')
lines.append('=' * 80)
lines.append('')
lines.append(f'Versets où MBP a plus de mots que V2 (même verset, chevauchement >= {MIN_WORD_OVERLAP:.0%}): {len(v2_missing_words)}')
lines.append(f'Versets présents dans MBP mais absents de V2: {len(v2_missing_verses)}')
lines.append(f'Chapitres présents dans MBP mais absents de V2: {len(v2_missing_chapters)}')
lines.append('')

# Summary by book
from collections import Counter
book_counts = Counter(item[1] for item in v2_missing_words)
if v2_missing_words:
    lines.append('--- Répartition par livre (versets avec mots manquants) ---')
    lines.append(f'{"Livre":35s} {"Nb":>6s} {"Mots v2":>8s} {"Mots mbp":>8s}')
    lines.append('-' * 57)
    book_stats = {}
    for bid, name, ch, v, wv, wm, sc, tv, tm, ex in v2_missing_words:
        if name not in book_stats:
            book_stats[name] = [0, 0, 0]
        book_stats[name][0] += 1
        book_stats[name][1] += wv
        book_stats[name][2] += wm
    for name in sorted(book_stats.keys()):
        cnt, wv, wm = book_stats[name]
        lines.append(f'{name:35s} {cnt:6d} {wv:8d} {wm:8d}')
    lines.append('')

# Detailed verses with missing words
if v2_missing_words:
    lines.append('=' * 80)
    lines.append('DÉTAIL — VERSETS AVEC MOTS MANQUANTS DANS V2')
    lines.append('=' * 80)
    lines.append('')
    for bid, name, ch, v, wv, wm, score, t_v2, t_mbp, extra in v2_missing_words:
        lines.append(f'--- {name} {ch}:{v} (v2:{wv}mots, mbp:{wm}mots, overlap:{score:.0%}) ---')
        lines.append(f'  Mots en plus dans MBP: {", ".join(extra[:10])}')
        lines.append(f'  v2:  {t_v2[:200]}')
        lines.append(f'  mbp: {t_mbp[:200]}')
        lines.append('')

# Missing verses
if v2_missing_verses:
    lines.append('=' * 80)
    lines.append('DÉTAIL — VERSETS PRÉSENTS DANS MBP MAIS ABSENTS DE V2')
    lines.append('=' * 80)
    lines.append('')
    for bid, name, ch, v, t_mbp in v2_missing_verses:
        lines.append(f'{name} {ch}:{v} = {t_mbp[:200]}')
    lines.append('')

# Missing chapters
if v2_missing_chapters:
    lines.append('=' * 80)
    lines.append('DÉTAIL — CHAPITRES PRÉSENTS DANS MBP MAIS ABSENTS DE V2')
    lines.append('=' * 80)
    lines.append('')
    for bid, name, ch, nv in v2_missing_chapters:
        lines.append(f'{name} chapitre {ch} ({nv} versets)')
    lines.append('')

report = '\n'.join(lines)
with open('v2_missing_words_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(f'Report: v2_missing_words_report.txt ({len(lines)} lines)')
print(f'Versets où MBP est plus long: {len(v2_missing_words)}')
print(f'Versets manquants dans V2: {len(v2_missing_verses)}')
print(f'Chapitres manquants dans V2: {len(v2_missing_chapters)}')
