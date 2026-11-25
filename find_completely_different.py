"""Find verses where the FULL TEXT is completely different between v2 and MBP.
Not just punctuation/spacing/footnotes/capitalization differences,
but where the actual content/translation differs significantly.
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

def clean_text(t):
    """Remove footnote markers, normalize quotes, lowercase for comparison."""
    t = re.sub(r'[*#]\d*\.?\d*\s*[^.;,!?]*\.', '', t)  # remove footnote refs
    t = re.sub(r'[*#]', '', t)
    t = t.replace('\u2019', "'").replace('\u2018', "'")
    t = t.replace('\u201c', '"').replace('\u201d', '"')
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t

def word_overlap(t1, t2):
    """Jaccard-like word overlap score (0-1)."""
    w1 = set(clean_text(t1).split())
    w2 = set(clean_text(t2).split())
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / len(w1 | w2)

v2_raw = load_v2('baibolyMG_v2.html')
mbp_raw = load_mbp('output/baiboly_mbp.html')

# Build v2 lookup
v2_verses = {}
v2_book_names = {}
for t in v2_raw:
    for b in v2_raw[t]:
        bid = b['id']
        v2_book_names[bid] = b['name']
        for ch in b['chapters']:
            for v in b['chapters'][ch]:
                v2_verses[(bid, ch, v)] = b['chapters'][ch][v]

# Map MBP codes to v2 IDs
mbp_to_v2id = {}
for code, mbp_book in mbp_raw.items():
    mbp_name = mbp_book['name'].lower().strip()
    for bid, vname in v2_book_names.items():
        if vname.lower().strip() == mbp_name:
            mbp_to_v2id[code] = bid
            break

# Build MBP lookup
mbp_verses = {}
for code, mbp_book in mbp_raw.items():
    bid = mbp_to_v2id.get(code)
    if not bid:
        continue
    for ch in mbp_book['chapters']:
        for v in mbp_book['chapters'][ch]:
            mbp_verses[(bid, ch, v)] = mbp_book['chapters'][ch][v]

# MIN_LENGTH: both texts must have at least this many chars to compare
# LOW_OVERLAP: texts with less than this word overlap are "completely different"
MIN_LENGTH = 50
LOW_OVERLAP = 0.30

completely_different = []
num_shifted = []

all_refs = sorted(set(list(v2_verses.keys()) + list(mbp_verses.keys())))

for ref in all_refs:
    bid, ch, v = ref
    t_v2 = v2_verses.get(ref, '')
    t_mbp = mbp_verses.get(ref, '')

    if not t_v2 or not t_mbp:
        continue  # only in one file

    if len(t_v2) < MIN_LENGTH or len(t_mbp) < MIN_LENGTH:
        continue  # too short to judge

    score = word_overlap(t_v2, t_mbp)

    if score < LOW_OVERLAP:
        # Check if this might be a verse-numbering shift
        # Look at adjacent verses to see if text matches nearby verse numbers
        name = v2_book_names.get(bid, bid)
        completely_different.append((bid, name, ch, v, score, t_v2[:100], t_mbp[:100]))

# Sort by overlap score (lowest first)
completely_different.sort(key=lambda x: x[4])

print(f"Total verses with < {LOW_OVERLAP*100:.0f}% word overlap and both >= {MIN_LENGTH} chars: {len(completely_different)}")
print()

if completely_different:
    print("=" * 80)
    print("VERSETS AU TEXTE COMPLÈTEMENT DIFFÉRENT")
    print("=" * 80)
    for bid, name, ch, v, score, t_v2, t_mbp in completely_different:
        print(f"\n--- {name} {ch}:{v} (overlap: {score:.0%}) ---")
        print(f"  v2:  {t_v2}...")
        print(f"  mbp: {t_mbp}...")
else:
    print("Aucun verset trouvé avec un texte complètement différent.")
    print("Toutes les différences sont des variations de ponctuation,")
    print("d'orthographe, de notes de bas de page, ou des versets tronqués.")
