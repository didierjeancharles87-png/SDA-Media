import os
os.chdir(r'G:\SDA\fihirana')

with open('baibolyMG_v2.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

line_1858 = lines[1857]  # 0-indexed: line 1858 is index 1857

if '</script>' not in line_1858:
    # The line ends with: ...,"chapter_count":22}]};\n
    # We need to add </script> after the semicolon
    lines[1857] = line_1858.rstrip('\n').rstrip('\r') + '</script>\n'
    print("Fixed: added </script> to line 1858")
    print("Line 1858 last 80 chars:", lines[1857][-80:])
else:
    print("Line 1858 already has </script>")

# Verify lines around it
print("\nLine 1857:", repr(lines[1856][:50]))
print("Line 1858 last 50:", repr(lines[1857][-50:]))
print("Line 1859:", repr(lines[1858][:50]))

with open('baibolyMG_v2.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nDone! HTML fixed.")
