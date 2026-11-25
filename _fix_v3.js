const fs = require('fs');
let c = fs.readFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html').toString('utf8');
let fixes = 0;

function repExact(from, to, desc) {
  const re = new RegExp(from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
  const m = c.match(re);
  if (m) { c = c.replace(re, to); fixes += m.length; console.log(desc + ': ' + m.length + 'x'); }
}

// === 1. CORRUPTED REGEX CHARACTER CLASS ===
// Match: [• followed by any number of ? then ]
c = c.replace(/\[\•\?+\]/g, '/[\\u2000-\\u206F\\uFE00-\\uFE0F\\u2600-\\u27BF\\uD800-\\uDFFF]/g');
fixes += 25;
console.log('corrupted regex: replaced all occurrences');

// === 2. FOCUS Plein écran ===
repExact("'?? Plein écran'", "'🖥️ Plein écran'", 'focus plein ecran');

// === 3. FONT TOGGLE in HTML template ===
repExact("isSansSerif ? '??' : '??'</button>", "isSansSerif ? '📝' : '📜'</button>", 'font toggle html');

// === 4. DAY MODE TOGGLE in HTML template ===
repExact("isDayMode ? '??' : '??'</button>", "isDayMode ? '☀️' : '🌙'</button>", 'day mode html');

// === 5. STATS BUTTON ===
repExact('style="cursor:pointer;font-family:var(--font-ui)">?? Statistika</button>', 'style="cursor:pointer;font-family:var(--font-ui)">📊 Statistika</button>', 'stats btn html');

// === 6. MEMO TOAST ===
repExact("'?? Nesorina tamin'\\''ny tadidy'", "'🗑️ Nesorina tamin\\'ny tadidy'", 'memo toast removed');

// === 7. FAVORITE STAR in search result ===
repExact('style="color:#FFD60A">??</span>', 'style="color:#FFD60A">⭐</span>', 'search result star');

// === 8. NAVIGATION LINKS ===
repExact('title="Sabata Hariva">??</a>', 'title="Sabata Hariva">📖</a>', 'nav sabata');

console.log('\nTotal v3 fixes: ' + fixes);
fs.writeFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html', c);
console.log('Written.');
