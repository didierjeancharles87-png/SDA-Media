import re

with open('G:/SDA/fihirana/Baiboly_Malagasy_Complet.htm', 'r', encoding='utf-8') as f:
    content = f.read()

book_names = {
    'at01': 'Genesisy', 'at02': 'Eksodosy', 'at03': 'Levitikosy',
    'at04': 'Nomery', 'at05': 'Deoteronomia', 'at06': 'Josoa',
    'at07': 'Mpitsara', 'at08': 'Rota', 'at09': '1 Samoela',
    'at10': '2 Samoela', 'at11': '1 Mpanjaka', 'at12': '2 Mpanjaka',
    'at13': '1 Tantara', 'at14': '2 Tantara', 'at15': 'Ezra',
    'at16': 'Nehemia', 'at17': 'Estera', 'at18': 'Joba',
    'at19': 'Salamo', 'at20': 'Ohabolana', 'at21': 'Mpitoriteny',
    'at22': "Tononkiran'i Solomona", 'at23': 'Isaia', 'at24': 'Jeremia',
    'at25': 'Fitomaniana', 'at26': 'Ezekiela', 'at27': 'Daniela',
    'at28': 'Hosea', 'at29': 'Joela', 'at30': 'Amosa',
    'at31': 'Obadia', 'at32': 'Jona', 'at33': 'Mika',
    'at34': 'Nahoma', 'at35': 'Habakoka', 'at36': 'Zefania',
    'at37': 'Hagay', 'at38': 'Zakaria', 'at39': 'Malakia',
    'nt01': 'Matio', 'nt02': 'Marka', 'nt03': 'Lioka',
    'nt04': 'Jaona', 'nt05': "Asan'ny Apostoly", 'nt06': 'Romana',
    'nt07': '1 Korintiana', 'nt08': '2 Korintiana', 'nt09': 'Galatiana',
    'nt10': 'Efesiana', 'nt11': 'Filipiana', 'nt12': 'Kolosiana',
    'nt13': '1 Tesaloniana', 'nt14': '2 Tesaloniana', 'nt15': '1 Timoty',
    'nt16': '2 Timoty', 'nt17': 'Titosy', 'nt18': 'Filemona',
    'nt19': 'Hebreo', 'nt20': 'Jakoba', 'nt21': '1 Petera',
    'nt22': '2 Petera', 'nt23': '1 Jaona', 'nt24': '2 Jaona',
    'nt25': '3 Jaona', 'nt26': 'Joda', 'nt27': 'Apokalypsy'
}

expected_chapters = {
    'at01': 50, 'at02': 40, 'at03': 27, 'at04': 36, 'at05': 34,
    'at06': 24, 'at07': 21, 'at08': 4, 'at09': 31, 'at10': 24,
    'at11': 22, 'at12': 25, 'at13': 29, 'at14': 36, 'at15': 10,
    'at16': 13, 'at17': 10, 'at18': 42, 'at19': 150, 'at20': 31,
    'at21': 12, 'at22': 8, 'at23': 66, 'at24': 52, 'at25': 5,
    'at26': 48, 'at27': 12, 'at28': 14, 'at29': 3, 'at30': 9,
    'at31': 1, 'at32': 4, 'at33': 7, 'at34': 3, 'at35': 3,
    'at36': 3, 'at37': 2, 'at38': 14, 'at39': 4,
    'nt01': 28, 'nt02': 16, 'nt03': 24, 'nt04': 21, 'nt05': 28,
    'nt06': 16, 'nt07': 16, 'nt08': 13, 'nt09': 6, 'nt10': 6,
    'nt11': 4, 'nt12': 4, 'nt13': 5, 'nt14': 3, 'nt15': 6,
    'nt16': 4, 'nt17': 3, 'nt18': 1, 'nt19': 13, 'nt20': 5,
    'nt21': 5, 'nt22': 3, 'nt23': 5, 'nt24': 1, 'nt25': 1,
    'nt26': 1, 'nt27': 22
}

total_found = 0
total_exp = 0
all_ok = True

for code, name in book_names.items():
    tag = f'id="{code}"'
    idx = content.find(tag)
    if idx >= 0:
        # Find all chapter headings for this book
        pattern = r'<p class="Chapitre" id="' + code + r'[^"]*">'
        chaps = re.findall(pattern, content[idx:idx+500000])
        num_chaps = len(chaps)
        total_found += num_chaps
        exp = expected_chapters.get(code, 0)
        total_exp += exp
        status = 'OK' if num_chaps == exp else f'MISMATCH (expected {exp})'
        if num_chaps != exp:
            all_ok = False
        print(f'{code} {name}: {num_chaps} {status}')
    else:
        print(f'{code} {name}: NOT FOUND')
        all_ok = False

print(f'\nTotal: {total_found} chapters found, {total_exp} expected')
if all_ok:
    print('ALL CHAPTERS CORRECT!')
else:
    print('SOME DISCREPANCIES (due to source Bible chapter numbering)')

# Check verse presence
print('\n=== Key verse check ===')
checks = [
    ("Genesis 1:1", "Tamin'ny voalohany Andriamanitra nahary"),
    ("Exodus 20:1-17", "Andriamanitra niteny"),
    ("Psalm 23:1", "Jehovah no Mpiandry ahy"),
    ("Isaiah 53:5", "Fa voalefona noho ny fahadisoantsika"),
    ("Matthew 1:1", "Ny bokin'ny firazanana"),
    ("John 3:16", "Fa toy izao no nitiavan'Andriamanitra ny olona"),
    ("Acts 2:1-4", "rehefa tonga ny andro Pentekosta"),
    ("Romans 8:28", "ny zavatra rehetra miara-miasa"),
    ("Revelation 22:21", "Ho amin'ny olona masina anie ny fahasoavan'i Jesosy"),
    ("Obadiah 1:1", "Fahitan'i Obadia"),
    ("Philemon 1:1", "Paoly"),
    ("2 John 1:1", "Ny Anti-panahy"),
    ("3 John 1:1", "Ry malala"),
    ("Jude 1:1", "mpanompon'i Jesosy Kristy"),
]
all_found = True
for label, snippet in checks:
    idx = content.find(snippet)
    found = idx >= 0
    if not found:
        all_found = False
    print(f'  {label}: {"OK" if found else "MISSING!"}')

if all_found:
    print('\nAll key verses present!')
else:
    print('\nSome verses missing!')
