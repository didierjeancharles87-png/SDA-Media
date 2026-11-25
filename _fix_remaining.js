const fs = require('fs');
let c = fs.readFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html').toString('utf8');
let total = 0;

function fix(from, to, desc) {
  const re = new RegExp(from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
  const matches = c.match(re);
  if (matches) {
    c = c.replace(re, to);
    total += matches.length;
    console.log(desc + ': ' + matches.length + 'x');
  }
}

// === REMAINING THEME ICONS ===
// These were missed by the keyword approach
const moreIcons = {
  'fandriampahalemana': '🕊️',
  'fahendrena': '💡',
  'famelan-keloka': '❤️',
  'harena': '💰',
  'fahafatesana': '⚰️',
  'fahafatesan': '⚰️',  // alternate spelling
  'fitsanganan\'ny maty': '✝️',
  'fitsanganana': '✝️',
  'fiavian\'ny tomp\'': '🌄',
  'fiavian\'ny tomp': '🌄',
  'fitsaran\'': '⚖️',
  'fitsarana': '⚖️',
  'batisan\'': '💧',
  'batisa': '💧',
  'fikelezam-aina': '🍞',
  'fikelezan-kena': '🍞',
  'fanabeazan\'': '📚',
  'fanabeazana': '📚',
  'fanambadian\'': '💑',
  'fanambadiana': '💑',
  'fitiavanana': '❤️',  // variant
  'fitiavana': '❤️',
  'fanetren-tena': '🙇',
  'fahalemem-panah': '🙇',
  'fahalemem-panahy': '🙇',
  'firehetam-po': '🔥',
  'fifohazana': '🔥',
  'fifohazan\'': '🔥',
  'herin\'': '⚡',
  'heriny': '⚡',
  'fahasoavan\'': '🌟',
  'fahasoavana': '🌟',
  'fahatsaran\'': '🌟',
  'fahatsarana': '🌟',
  'fahafahan\'': '🕊️',
  'fahafahana': '🕊️',
  'fitsaharan\'': '📖',
  'fitsaharana': '📖',
  'fanompoan\'': '⛪',
  'fanompoana': '⛪',
  'fihavanan\'': '🤝',
  'fihavanana': '🤝',
  'fahadiovan\'': '✨',
  'fahadiovana': '✨',
  'fahari-toky': '💪',
  'fahari-to': '💪',
  'fampihavanan\'': '🕊️',
  'fampihavanana': '🕊️',
  'fahatsoran\'': '🌱',
  'fahatsorana': '🌱',
  'firaisan-tsain\'': '🤝',
  'firaisan-tsaina': '🤝',
  'fahatokian\'': '🤝',
  'fahatokiana': '🤝',
  'famindram-pon\'': '❤️',
  'famindram-po': '❤️',
  // More Adventiste entries
  'fitsaran\'ny': '⚖️',
  'anjaran\'': '⚖️',
  'anjaran': '⚖️',
  'fanjakan\'': '👑',
  'fanjakany': '👑',
  'fiangonan\'': '⛪',
  'fiangonana': '⛪',
  'mpitory': '⛪',
  // Pratique
  'fanambadian\'ny': '💑',
  'mpivady': '💑',
  'fianakavian\'': '👨‍👩‍👧‍👦',
  'fianakaviana': '👨‍👩‍👧‍👦',
  'asan\'ny': '🔧',
  'asa': '🔧',
  'fahavalon\'': '👿',
  'fahavalo': '👿',
  'fahamarinan\'': '⚖️',
  'fahamarinana': '⚖️',
  'fifalian\'': '😊',
  'fifaliana': '😊',
  'fahatahoran\'': '🙏',
  'fahatahorana': '🙏',
  'fanahin\'ny faminanian\'': '🔮',
  'fanahin\'ny faminaniana': '🔮',
  'maminany': '🔮',
  'fanalefahan\'': '⚔️',
  'fanalefahana': '⚔️',
  'rano-ain\'': '💧',
  'rano-aina': '💧',
  'fahazavan\'': '💡',
  'fahazavana': '💡',
  'fenon\'': '💯',
  'feno': '💯',
  'fiainan\'': '♾️',
  'fiainana': '♾️',
  'ampahafolon\'': '💰',
  'ampahafolony': '💰',
  'fizaràn\'': '💰',
};

// Process remaining THEMES icons
let themeCount = 0;
for (const [key, icon] of Object.entries(moreIcons)) {
  // Search for key followed by :{ with icon:'??' after it
  const pattern = `'${key}':{`;
  let idx = 0;
  while ((idx = c.indexOf(pattern, idx)) !== -1) {
    // Find icon field within brackets... find the matching closing brace
    let braceDepth = 0;
    let j = idx + pattern.length;
    while (j < c.length) {
      if (c[j] === '{') braceDepth++;
      else if (c[j] === '}') {
        braceDepth--;
        if (braceDepth < 0) break;
      } else if (braceDepth === 0 && c[j] === ',') break;
      j++;
    }
    let block = c.substring(idx + pattern.length, j + 1);
    let iconIdx = block.indexOf("icon:'");
    if (iconIdx !== -1) {
      let start = iconIdx + 6;
      let end = block.indexOf("'", start);
      if (end > start) {
        let currentIcon = block.substring(start, end);
        if (currentIcon.match(/^\?+$/)) {
          let globalStart = idx + pattern.length + iconIdx + 6;
          let globalEnd = globalStart + (end - iconIdx - 6);
          c = c.substring(0, globalStart) + icon + c.substring(globalEnd);
          themeCount++;
        }
      }
    }
    idx++;
  }
}
if (themeCount > 0) { total += themeCount; console.log('  more theme icons: ' + themeCount + 'x'); }

// === AI ASSISTANT HELP TEXT ===
fix("'• ?? Référence: \"Genesisy 1:1\"'", "'• 🔍 Référence: \"Genesisy 1:1\"'", 'ai help ref');
fix("'• ?? Teny: \"fitiavana ny fahavalo\"'", "'• 🔤 Teny: \"fitiavana ny fahavalo\"'", 'ai help mot');
fix("'• ?? Lohahevitra: \"andininy momba ny sabata\"'", "'• 📖 Lohahevitra: \"andininy momba ny sabata\"'", 'ai help theme');
fix("'• ?? Olona: \"andininy momba i Mosesy\"'", "'• 👤 Olona: \"andininy momba i Mosesy\"'", 'ai help pers');
fix("'• ?? Vakio: \"vakio ny Jaona 3\"'", "'• 📖 Vakio: \"vakio ny Jaona 3\"'", 'ai help lire');
fix("'• ?? Aléatoire: \"verset mampahery\"'", "'• 🎲 Aléatoire: \"verset mampahery\"'", 'ai help alea');
fix("'• ?? Androany: \"verset androany\"'", "'• 📅 Androany: \"verset androany\"'", 'ai help today');

// === AI HEADER: Favorites, Fihainoana, Plan ===
fix("'? Favorites, ?? Fihainoana, ?? Plan vakiteny'", "'⭐ Favorites, 🎵 Fihainoana, 📖 Plan vakiteny'", 'ai header info');

// === AI: Chat history ===  
fix("text:'?? Tsy mbola nisy fikarohana nataonareo'", "text:'🔍 Tsy mbola nisy fikarohana nataonareo'", 'ai no search (2)');
fix("text:'?? Fikarohanao farany:", "text:'🔍 Fikarohanao farany:", 'ai recent search (2)');

// === AI: Found books/verses with ?? ===
fix("text:\`?? \${found.book.name} \${found.chapter}:", "text:\`📖 \${found.book.name} \${found.chapter}:", 'ai found chapter');
fix("text:\`?? \${found.book.name} Toko \${found.chapter}", "text:\`📖 \${found.book.name} Toko \${found.chapter}", 'ai found toko');

// === FOCUS BUTTON ===
fix("mode':'?? Plein écran'", "mode':'🖥️ Plein écran'", 'focus plein ecran (2)');

// === AI ASSISTANT WELCOME (restructured) ===
// The welcome text has • with ?? before various descriptions
fix("• ?? Rechercher des versets sur un thème", "• 🔍 Rechercher des versets sur un thème", 'ai welcome search');
fix("• ?? Expliquer des passages bibliques", "• 📖 Expliquer des passages bibliques", 'ai welcome explain');
fix("• ?? Vous accompagner dans", "• 🤝 Vous accompagner dans", 'ai welcome accompany');
fix("• ??? Écouter vos questions", "• 🎤 Écouter vos questions", 'ai welcome listen');

// Also fix the : ? prefix in the welcome text for the bot greeting
fix("'? Bonjour ! Je suis votre assistant IA'", "'👋 Bonjour ! Je suis votre assistant IA'", 'ai welcome greeting');

// === AI: ? before Favorites in welcome ===
fix("'• ? Favorites, ?? Fihainoana", "'• ⭐ Favorites, 🎵 Fihainoana", 'ai welcome features');

// === MORE FIXES: plan icons with ?? in reading plan ===
fix("{ label: '?? A — Sabata'", "{ label: '📖 A — Sabata'", 'plan sabata item');

// === READING PLAN ITEM ICONS ===
fix("day.icon||'??'", "day.icon||'📖'", 'plan day icon (more)');

// === AI READING CONTEXT ===
fix("text:\`?? \${bookMatch.name}", "text:\`📖 \${bookMatch.name}", 'ai book reading context');

// === AI: Search result headers ===
fix("??'}),{type:'bot',text:'?? Nahita andininy", "'📖'}),{type:'bot',text:'🔍 Nahita andininy", 'ai search results');

// === PopOver chips in search overlay ===
fix("'{label:'?? Androany',val:'verset androany'}", "'{label:'📅 Androany',val:'verset androany'}", 'pop chip day');
fix("'{label:'?? Mampahery',val:'verset mampahery'}", "'{label:'💪 Mampahery',val:'verset mampahery'}", 'pop chip encour');
fix("'{label:'?? Fitiavana',val:'andininy momba ny fitiavana'}", "'{label:'❤️ Fitiavana',val:'andininy momba ny fitiavana'}", 'pop chip love');
fix("'{label:'?? Vavaka',val:'andininy momba ny vavaka'}", "'{label:'🙏 Vavaka',val:'andininy momba ny vavaka'}", 'pop chip prayer');
fix("'{label:'?? Sabata',val:'andininy momba ny sabata'}", "'{label:'📖 Sabata',val:'andininy momba ny sabata'}", 'pop chip sabbath');
fix("'{label:'?? Fahatongavany',val:'andininy momba ny fahatongavan'}", "'{label:'👑 Fahatongavany',val:'andininy momba ny fahatongavan'}", 'pop chip advent');
fix("'{label:'?? Mosesy',val:'andininy momba i Mosesy'}", "'{label:'👤 Mosesy',val:'andininy momba i Mosesy'}", 'pop chip moses');
fix("'{label:'?? Davida',val:'andininy momba i Davida'}", "'{label:'👤 Davida',val:'andininy momba i Davida'}", 'pop chip david');
fix("'{label:'?? Aléatoire',val:'verset maimaimpoana'}", "'{label:'🎲 Aléatoire',val:'verset maimaimpoana'}", 'pop chip random');

// === MORE POP CHIPS (the simpler version without val) ===
fix("'{label:'?? Androany',val:'verset androany'}", "'{label:'📅 Androany',val:'verset androany'}", 'popover today');

// === FAB: status icon ===
fix("'???'}", "status==='thinking'?'🤔':'💬'}", 'fab thinking');
// Fix the FAB inner icon too
fix("status==='listening'?'🎤':'💬'}", "status==='listening'?'🎤':'💬'", 'fab inner');

// === Bible verse corruption (data quality issue - minimal fix) ===
// These are in the actual Bible verses and should be proper text
// We can try to fix common patterns: 'tat??' -> 'tany', etc.
// But this is too risky without knowing the original text

console.log('\nTotal additional fixes: ' + total);
fs.writeFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html', c);
console.log('Written to baibolyMG_v2.html');
