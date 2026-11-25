import re, json

with open('baibolyMG_v2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the BIBLE_DATA JSON
start = content.index('window.BIBLE_DATA = ') + len('window.BIBLE_DATA = ')
# The structure is: {"testamenta_taloha":[...],"testamenta_vaovao":[...]...} followed by ;
# Let's find the semicolon after the end of the object
depth = 0
i = start
while i < len(content):
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end = i + 1
            break
    elif content[i] == ';' and depth == 0:
        end = i
        break
    i += 1

json_str = content[start:end]
data = json.loads(json_str)

taloha = data['testamenta_taloha']
vaovao = data['testamenta_vaovao']
total_books = len(taloha) + len(vaovao)
total_chapters = 0
total_verses = 0
for b in taloha + vaovao:
    chs = b['chapters']
    total_chapters += len(chs)
    for ch_num, verses in chs.items():
        total_verses += len(verses)

print(f'Books: {total_books} (Taloha: {len(taloha)}, Vaovao: {len(vaovao)})')
print(f'Chapters: {total_chapters}')
print(f'Verses: {total_verses}')
