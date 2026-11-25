const fs = require('fs');

function fixFile(filePath) {
  let buf = fs.readFileSync(filePath);
  let c = buf.toString('utf8');
  
  const fixes = [];
  
  if (filePath.includes('fihirana_advantista.html')) {
    // Favorite: isFav?'❤️':'🤍'
    fixes.push({ from: "isFav?'?':'?'", to: "isFav?'\u2764\uFE0F':'\uD83E\uDD0D'" });
    // Copy: '📋 Kopa' / '✅ Voakopy'
    fixes.push({ from: "'?? Kopa'", to: "'\uD83D\uDCCB Kopa'" });
    fixes.push({ from: "'? Voakopy'", to: "'\u2705 Voakopy'" });
    // Focus: '❌ Hiala' / '🖥️ Feno'
    fixes.push({ from: "focusMode?'?? Hiala':'?? Feno'", to: "focusMode?'\u274C Hiala':'\uD83D\uDDA5\uFE0F Feno'" });
  }
  
  if (filePath.includes('baibolyMG_v2.html')) {
    // Check for broken emojis in buttons first
    ['Voakopy', 'Nalaina', 'Kopa', 'Feno', 'Hiala'].forEach(word => {
      let idx = 0;
      while ((idx = c.indexOf(word, idx)) !== -1) {
        let start = Math.max(0, idx - 80);
        let end = Math.min(c.length, idx + 20);
        let snippet = c.substring(start, end);
        if (snippet.includes('?')) console.log('Baiboly ' + word + ' context: ' + snippet);
        idx++;
      }
    });
    
    // Check for floating buttons / FABs
    ['fab', 'float-btn', 'FAB', 'floating'].forEach(p => {
      let i = 0;
      while ((i = c.indexOf(p, i)) !== -1) {
        let start = Math.max(0, i - 5);
        let end = Math.min(c.length, i + 100);
        let snippet = c.substring(start, end);
        if (snippet.includes('?')) console.log('Baiboly ' + p + ' with ?: ' + snippet);
        i++;
      }
    });
  }
  
  if (filePath.includes('search-bar.js')) {
    // Check for ? in button content
    let idx = 0;
    let lineNum = 1;
    while ((idx = c.indexOf('\n', idx)) !== -1) { lineNum++; idx++; }
    const lines = c.split('\n');
    lines.forEach((l, ln) => {
      if (l.includes('?') && (l.includes('button') || l.includes('btn') || l.includes('FAB'))) {
        console.log('search-bar.js L' + (ln+1) + ': ' + l.trim().substring(0, 120));
      }
    });
  }
  
  let changed = false;
  for (const f of fixes) {
    const escaped = f.from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(escaped, 'g');
    if (regex.test(c)) {
      c = c.replace(regex, f.to);
      const name = filePath.replace(/\\/g, '/').split('/').pop();
      console.log(name + ': ' + f.from + ' -> ' + f.to + ' (fixed)');
      changed = true;
    } else {
      console.log('NOT FOUND: ' + f.from + ' in ' + filePath.replace(/\\/g, '/').split('/').pop());
    }
  }
  
  if (changed) fs.writeFileSync(filePath, c);
  else console.log(filePath.replace(/\\/g, '/').split('/').pop() + ': no changes needed');
}

fixFile('G:\\SDA\\fihirana\\fihirana_advantista.html');
fixFile('G:\\SDA\\fihirana\\baibolyMG_v2.html');
fixFile('G:\\SDA\\fihirana\\search-bar.js');

try { fs.unlinkSync('G:\\SDA\\fihirana\\_temp_check.js'); } catch(e) {}
try { fs.unlinkSync('G:\\SDA\\fihirana\\_temp_check2.js'); } catch(e) {}
