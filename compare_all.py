"""
Compare HTML songs against PDF songs to find differences.
Only compares songs that exist in BOTH.
"""
import json
import re

# ── Load HTML data ──
with open('fihirana_advantista.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('var FIHIRANA_DATA =')
start = content.find('{', start)
depth = 0
end = start
for i in range(start, len(content)):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end = i + 1
            break
while end < len(content) and content[end] != ';':
    end += 1
json_str = content[start:end].rstrip(';')
html_data = json.loads(json_str)

html_songs = {}
for s in html_data['hira']:
    num = s['numero']
    verses = {}
    for p in s['paroles']:
        c = p['couplet']
        verses[c] = p['texte']
    html_songs[num] = {
        'titre': s['titre'],
        'verses': verses,
        'verse_count': len(verses),
        'paroles': s['paroles']
    }

print(f'HTML songs: {len(html_songs)}')

# ── Load PDF data ──
with open('pdf_parsed.json', 'r', encoding='utf-8') as f:
    pdf_data = json.load(f)

pdf_songs = {}
for k, v in pdf_data.items():
    num = int(k)
    pdf_songs[num] = v

print(f'PDF songs: {len(pdf_songs)}')

# ── Compare ──
common_nums = sorted(set(html_songs.keys()) & set(pdf_songs.keys()))
print(f'Common songs: {len(common_nums)}')

differences = []

for num in common_nums:
    h = html_songs[num]
    p = pdf_songs[num]
    
    # Compare verse count
    h_vcount = h['verse_count']
    p_vcount = len(p['verses'])
    
    if h_vcount != p_vcount:
        differences.append({
            'num': num,
            'titre_html': h['titre'],
            'titre_pdf': p['titre'],
            'issue': 'verse_count',
            'html_count': h_vcount,
            'pdf_count': p_vcount,
            'html_verses': list(h['verses'].keys()),
            'pdf_verses': list(p['verses'].keys()),
            'detail': {}
        })
        continue
    
    # Compare verse content
    for vnum in sorted(set(list(h['verses'].keys()) + list(p['verses'].keys()))):
        h_text = h['verses'].get(vnum, '')
        p_text = p['verses'].get(vnum, '')
        
        if h_text != p_text:
            # Check the difference
            h_lines = h_text.split('\n')
            p_lines = p_text.split('\n')
            
            if len(h_lines) != len(p_lines):
                key = f'verse_{vnum}'
                if not differences or differences[-1]['num'] != num or differences[-1]['issue'] != 'verse_content':
                    differences.append({
                        'num': num,
                        'titre_html': h['titre'],
                        'titre_pdf': p['titre'],
                        'issue': 'verse_content',
                        'html_count': h_vcount,
                        'pdf_count': p_vcount,
                        'html_verses': list(h['verses'].keys()),
                        'pdf_verses': list(p['verses'].keys()),
                        'detail': {}
                    })
                differences[-1]['detail'][key] = {
                    'html': h_text[:200],
                    'pdf': p_text[:200]
                }
                continue
            
            # Word-by-word comparison
            for li, (hl, pl) in enumerate(zip(h_lines, p_lines)):
                if hl.strip() != pl.strip():
                    # Check for missing words
                    h_words = set(hl.lower().split())
                    p_words = set(pl.lower().split())
                    missing = p_words - h_words
                    extra = h_words - p_words
                    if missing or extra:
                        key = f'verse_{vnum}_line_{li}'
                        if not differences or differences[-1]['num'] != num or differences[-1]['issue'] != 'word_diff':
                            differences.append({
                                'num': num,
                                'titre_html': h['titre'],
                                'titre_pdf': p['titre'],
                                'issue': 'word_diff',
                                'html_count': h_vcount,
                                'pdf_count': p_vcount,
                                'html_verses': list(h['verses'].keys()),
                                'pdf_verses': list(p['verses'].keys()),
                                'detail': {}
                            })
                        differences[-1]['detail'][key] = {
                            'html': hl.strip(),
                            'pdf': pl.strip(),
                            'missing': list(missing)[:5],
                            'extra': list(extra)[:5]
                        }

print(f'\nDifferences found: {len(differences)}')

# Categorize
by_issue = {}
for d in differences:
    issue = d['issue']
    if issue not in by_issue:
        by_issue[issue] = []
    by_issue[issue].append(d['num'])

for issue, nums in sorted(by_issue.items()):
    print(f'  {issue}: {len(nums)} songs - {nums[:20]}')

# Save full report
with open('comparison_report.txt', 'w', encoding='utf-8') as f:
    f.write(f'HTML songs: {len(html_songs)}\n')
    f.write(f'PDF songs: {len(pdf_songs)}\n')
    f.write(f'Common songs: {len(common_nums)}\n')
    f.write(f'Differences: {len(differences)}\n\n')
    
    for d in differences:
        f.write(f'\n=== Song {d["num"]}: {d["titre_html"]} ===\n')
        f.write(f'Issue: {d["issue"]}\n')
        f.write(f'HTML: {d["html_count"]} verses - {d["html_verses"]}\n')
        f.write(f'PDF:  {d["pdf_count"]} verses - {d["pdf_verses"]}\n')
        for k, v in d['detail'].items():
            f.write(f'  [{k}]\n')
            if 'html' in v:
                f.write(f'    HTML: {v["html"][:150]}\n')
                f.write(f'    PDF:  {v["pdf"][:150]}\n')
            if 'missing' in v:
                f.write(f'    Missing words: {v["missing"]}\n')
                f.write(f'    Extra words: {v["extra"]}\n')

print('\nReport saved to comparison_report.txt')

# Summary of significant issues
print('\n=== SONGS WITH VERSE COUNT MISMATCH ===')
count_diffs = [d for d in differences if d['issue'] == 'verse_count']
for d in sorted(count_diffs, key=lambda x: abs(x['html_count'] - x['pdf_count']), reverse=True)[:30]:
    print(f'  {d["num"]}: {d["titre_html"]} - HTML:{d["html_count"]}v vs PDF:{d["pdf_count"]}v')
    print(f'    HTML verses: {d["html_verses"]}')
    print(f'    PDF verses:  {d["pdf_verses"]}')
