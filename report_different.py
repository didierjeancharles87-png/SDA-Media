"""List verses with completely different text (low word overlap)."""
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

def clean(t):
    t = re.sub(r'[*#]\d*\.?\d*[^.;,!?]*[.;,!?]', '', t)
    t = re.sub(r'[*#]', '', t)
    t = t.replace('\u2019', "'").replace('\u2018', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t

def overlap(t1, t2):
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

MIN_LENGTH = 50
LOW_OVERLAP = 0.30

completely_different = []
all_refs = sorted(set(list(v2_verses.keys()) + list(mbp_verses.keys())))

for ref in all_refs:
    bid, ch, v = ref
    t_v2 = v2_verses.get(ref, '')
    t_mbp = mbp_verses.get(ref, '')
    if not t_v2 or not t_mbp:
        continue
    if len(t_v2) < MIN_LENGTH or len(t_mbp) < MIN_LENGTH:
        continue
    score = overlap(t_v2, t_mbp)
    if score < LOW_OVERLAP:
        name = v2_book_names.get(bid, bid)
        completely_different.append((bid, name, ch, v, score))

# Group by book
from collections import Counter
book_counts = Counter(item[1] for item in completely_different)

lines = []
lines.append('=' * 80)
lines.append('VERSETS AU TEXTE COMPLÈTEMENT DIFFÉRENT')
lines.append(f'(moins de {LOW_OVERLAP*100:.0f}% de mots communs, les deux textes >= {MIN_LENGTH} caractères)')
lines.append('=' * 80)
lines.append(f'Total: {len(completely_different)} versets')
lines.append('')
lines.append('--- Répartition par livre ---')
lines.append(f'{"Livre":35s} {"Nb versets":>10s}')
lines.append('-' * 45)
for bid, cnt in book_counts.most_common():
    lines.append(f'{bid:35s} {cnt:10d}')
lines.append('')
lines.append('-' * 80)
lines.append('DÉTAIL VERSET PAR VERSET')
lines.append('-' * 80)
lines.append('')

for bid, name, ch, v, score in completely_different:
    t_v2 = v2_verses.get((bid, ch, v), '')
    t_mbp = mbp_verses.get((bid, ch, v), '')
    lines.append(f'--- {name} {ch}:{v} (chevauchement: {score:.0%}) ---')
    lines.append(f'  v2:  {t_v2}')
    lines.append(f'  mbp: {t_mbp}')
    lines.append('')

report = '\n'.join(lines)
with open('completely_different_verses.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(f'Report written: {len(completely_different)} verses, {len(lines)} lines')
print()
print('--- Répartition par livre ---')
for bid, cnt in book_counts.most_common(20):
    print(f'  {bid:35s} {cnt:5d}')
