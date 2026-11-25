const fs = require('fs');
let c = fs.readFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html').toString('utf8');
let fixes = 0;

// === FONT TOGGLE in HTML template literal ===
// Pattern: ${isSansSerif ? '??' : '??'}
// Use substring matching since regex with ${} is tricky
let idx = 0;
let fontCount = 0;
while ((idx = c.indexOf("isSansSerif ? '", idx)) !== -1) {
  let start = idx;
  let end = c.indexOf("'", idx + 16);
  if (end > start) {
    // Check if this part has '??'
    let chunk = c.substring(idx, end + 20);
    if (chunk.includes("'??' : '??'") || chunk.includes("'??' : '??'")) {
      c = c.substring(0, idx + 15) + "'📝' : '📜'" + c.substring(end + 16);
      fontCount++;
      fixes++;
    }
  }
  idx++;
}
if (fontCount > 0) console.log('font toggle html: ' + fontCount + 'x');

// === DAY MODE TOGGLE in HTML template literal ===
idx = 0;
let dayCount = 0;
while ((idx = c.indexOf("isDayMode ? '", idx)) !== -1) {
  let end = c.indexOf("'", idx + 14);
  if (end > idx) {
    let chunk = c.substring(idx, end + 20);
    if (chunk.includes("'??' : '??'")) {
      c = c.substring(0, idx + 13) + "'☀️' : '🌙'" + c.substring(end + 16);
      dayCount++;
      fixes++;
    }
  }
  idx++;
}
if (dayCount > 0) console.log('day mode html: ' + dayCount + 'x');

// === STATS BUTTON (second instance) ===
// Find ?? Statistika in remaining context
idx = c.indexOf('?? Statistika');
if (idx >= 0) {
  c = c.substring(0, idx) + '📊 Statistika' + c.substring(idx + 14);
  fixes++;
  console.log('stats button (2): 1x');
}

// === MEMO TOAST ===  
idx = c.indexOf("'?? Nesorina tamin'");
if (idx >= 0) {
  // The actual string in the file: '?? Nesorina tamin\'ny tadidy'
  c = c.substring(0, idx) + "'🗑️ Nesorina tamin\\" + c.substring(idx + 3);
  fixes++;
  console.log('memo toast removed: 1x');
}

// === NAV LINK ===
idx = c.indexOf('title="Sabata Hariva">??</a>');
if (idx >= 0) {
  c = c.substring(0, idx + 22) + '📖' + c.substring(idx + 24);
  fixes++;
  console.log('nav sabata: 1x');
} else {
  // Try to find any remaining nav links with ??
  let navIdx = 0;
  while ((navIdx = c.indexOf('title="', navIdx)) !== -1) {
    let titleEnd = c.indexOf('"', navIdx + 7);
    if (titleEnd > navIdx) {
      let linkEnd = c.indexOf('</a>', titleEnd);
      if (linkEnd > titleEnd) {
        let linkContent = c.substring(titleEnd + 1, linkEnd);
        if (linkContent.trim().match(/^\?+$/)) {
          let title = c.substring(navIdx + 7, titleEnd);
          let icon;
          if (title.includes('Fandraisana') || title.includes('Accueil')) icon = '🏠';
          else if (title.includes('Baiboly') || title.includes('Bible')) icon = '📖';
          else if (title.includes('Fihirana')) icon = '🎵';
          else if (title.includes('Annonce')) icon = '📢';
          else if (title.includes('Chat') || title.includes('Assistant')) icon = '💬';
          else if (title.includes('Sabata')) icon = '📖';
          else icon = '🔗';
          c = c.substring(0, titleEnd + 1) + icon + c.substring(linkEnd);
          fixes++;
          console.log('nav link ' + title + ': 1x');
        }
      }
    }
    navIdx++;
  }
}

console.log('\nTotal v4 fixes: ' + fixes);
fs.writeFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html', c);
console.log('Written.');
