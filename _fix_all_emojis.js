const fs = require('fs');
let c = fs.readFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html').toString('utf8');
let totalFixes = 0;

function fix(from, to, desc) {
  const re = new RegExp(from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
  const matches = c.match(re);
  if (matches) {
    c = c.replace(re, to);
    totalFixes += matches.length;
    console.log('  ' + desc + ': ' + matches.length + 'x');
  }
}

// === NAVIGATION DRAWER (nd-icon) ===
// Each nd-icon with ?? needs context-based emoji
// Look at patterns like: <span class="nd-icon">??</span><span>Fandraisana</span>
fix('<span class="nd-icon">??</span><span>Fandraisana</span>', '<span class="nd-icon">🏠</span><span>Fandraisana</span>', 'nd-icon Fandraisana');
fix('<span class="nd-icon">??</span><span>Fihirana Advantista</span>', '<span class="nd-icon">🎵</span><span>Fihirana Advantista</span>', 'nd-icon Fihirana');
fix('<span class="nd-icon">???</span><span>Mode Projection</span>', '<span class="nd-icon">🖥️</span><span>Mode Projection</span>', 'nd-icon Projection');
fix('<span class="nd-icon">??</span><span>Fitsipi-pifehezana</span>', '<span class="nd-icon">⚙️</span><span>Fitsipi-pifehezana</span>', 'nd-icon Settings');
fix('<span class="nd-icon">??</span><span>Plan de lecture</span>', '<span class="nd-icon">📖</span><span>Plan de lecture</span>', 'nd-icon Plan');
fix('<span class="nd-icon">??</span><span>Rechercher</span>', '<span class="nd-icon">🔍</span><span>Rechercher</span>', 'nd-icon Search');

// === BOTTOM NAV ICONS (bnav-icon) ===
// <span class="bnav-icon">??</span>
// Need to fix ALL bnav-icon instances
let bnavCount = 0;
let ci = 0;
while ((ci = c.indexOf('bnav-icon', ci)) !== -1) {
  let startTag = c.indexOf('>', ci) + 1;
  let endTag = c.indexOf('<', startTag);
  if (endTag > startTag) {
    let content = c.substring(startTag, endTag);
    if (content.match(/^\?+$/)) {
      let contextStart = Math.max(0, ci - 150);
      let context = c.substring(contextStart, endTag + 10);
      let icon;
      if (context.includes('Fandraisana') || context.includes('Accueil')) icon = '🏠';
      else if (context.includes('Baiboly') || context.includes('Bible')) icon = '📖';
      else if (context.includes('Fihirana') || context.includes('Hymne')) icon = '🎵';
      else if (context.includes('Annonce') || context.includes('Annonces')) icon = '📢';
      else if (context.includes('Sabata')) icon = '📖';
      else if (context.includes('Chat') || context.includes('Assistant')) icon = '💬';
      else if (context.includes('Fikarohana') || context.includes('Recherche')) icon = '🔍';
      else if (context.includes('Nalaina') || context.includes('Favoris')) icon = '⭐';
      else if (context.includes('Projets')) icon = '📋';
      else if (context.includes('Param') || context.includes('Régl')) icon = '⚙️';
      else icon = '📖';
      c = c.substring(0, startTag) + icon + c.substring(endTag);
      bnavCount++;
    }
  }
  ci++;
}
if (bnavCount > 0) { totalFixes += bnavCount; console.log('  bnav-icon: ' + bnavCount + 'x'); }

// === SETTINGS TITLE ===
fix('class="settings-title">?? Fitsipi-pifehezana</div>', 'class="settings-title">⚙️ Fitsipi-pifehezana</div>', 'settings title');

// === THEME LABELS ===
fix('label="Loko mainty">?? Alina</div>', 'label="Loko mainty">🌙 Alina</div>', 'theme dark');
fix('label="Loko mazava">?? Mazava</div>', 'label="Loko mazava">☀️ Mazava</div>', 'theme light');
fix('label="Loko sepia">?? Sépia</div>', 'label="Loko sepia">📜 Sépia</div>', 'theme sepia');

// === VERSET SELECTOR BUTTONS ===
fix('"Tsinjory ny sary">?? Tsinjory ny sary</button>', '"Tsinjory ny sary">🖼️ Tsinjory ny sary</button>', 'view image btn');

// === PWA OFFLINE BAR ===
fix('id="pwa-offline-bar">?? Tsy misy internet', 'id="pwa-offline-bar">📡 Tsy misy internet', 'offline bar');

// === WELCOME MESSAGE ===
fix("const WELCOME='?? Salama!", "const WELCOME='👋 Salama!", 'welcome message');

// === ASSISTANT WELCOME ===
// ? Bonjour ! ... ? Rechercher des versets ... ? Expliquer ... ? Vous accompagner ... ? Écouter
let old = "Bonjour ! Je suis votre assistant IA pour la Bible Malgache.\n\nJe peux vous aider à :\n• ?? Rechercher des versets sur un thème\n• ?? Expliquer des passages bibliques\n• ?? Vous accompagner dans l'étude de la Parole\n• ??? Écouter vos questions à voix haute";
let nw = "Bonjour ! Je suis votre assistant IA pour la Bible Malgache.\n\nJe peux vous aider à :\n• 🔍 Rechercher des versets sur un thème\n• 📖 Expliquer des passages bibliques\n• 🤝 Vous accompagner dans l'étude de la Parole\n• 🎤 Écouter vos questions à voix haute";
if (c.includes(old)) { c = c.replace(old, nw); totalFixes += 4; console.log('  assistant welcome: 4x'); }

// === ASSISTANT QUICK CHIPS ===
fix("quickChips=[{label:'?? Verset du jour'", "quickChips=[{label:'📖 Verset du jour'", 'quickChip verset jour');
fix("label:'?? Encouragement'", "label:'💪 Encouragement'", 'quickChip encouragement');
fix("label:'?? L'amour'", "label:'❤️ L'amour'", 'quickChip amour');
fix("label:'?? Saint-Esprit'", "label:'🕊️ Saint-Esprit'", 'quickChip Saint-Esprit');
fix("label:'?? Jean 3:16'", "label:'📖 Jean 3:16'", 'quickChip Jean 3:16');

// === ASSISTANT AI STATUS ===
fix("status==='listening'?'??? Écoute en cours...'", "status==='listening'?'🎤 Écoute en cours...'", 'listening status');
fix("status==='thinking'?'?? Réflexion en cours...'", "status==='thinking'?'🤔 Réflexion en cours...'", 'thinking status');

// === ASSISTANT AI VOICE BUTTON ===
fix("isSpeaking?'? Ajanony':'?? Henoy'", "isSpeaking?'⏹️ Ajanony':'🎵 Henoy'", 'voice button');

// === FOCUS MODE BUTTON ===
fix("mode':'?? Plein écran'", "mode':'🖥️ Plein écran'", 'focus plein ecran');

// === SHARE BUTTON ===
fix("shareBtn.innerHTML = '?? Zarao'", "shareBtn.innerHTML = '📤 Zarao'", 'share button');

// === COPY BUTTONS ===
fix("'>?? Adikao</button>", "'>📋 Adikao</button>", 'copy button (vsb)');

// Vact-btn copy (already fixed fihirana pattern, fix baiboly version)
fix("copied?'\u2705 Voakopy':'\uD83D\uDCCB Kopa'", "copied?'✅ Voakopy':'📋 Kopa'", 'vact copy (unicode)');

// Also handle the toast messages
fix("showToast('?? Voakopy!')", "showToast('✅ Voakopy!')", 'toast copy success');
fix("showToastPro('?? Voakopy ho zaraina!')", "showToastPro('✅ Voakopy ho zaraina!')", 'toast share success');
fix("showToast('?? Rohy voakopy!')", "showToast('🔗 Rohy voakopy!')", 'toast link copy');

// === TOAST: Surlignage / Highlights ===
fix("showToast(already ? '?? Surlignage retiré' : '?? ')", "showToast(already ? '❌ Surlignage retiré' : '✅ ')", 'toast highlight');
fix("showToast('?? Voatahiry ny fanamarihana')", "showToast('✅ Voatahiry ny fanamarihana')", 'toast note saved');
fix("showToast('?? Voafafa ny fanamarihana')", "showToast('🗑️ Voafafa ny fanamarihana')", 'toast note deleted');
fix("showToast('?? Nesorina tamin\'ny tadidy')", "showToast('🗑️ Nesorina tamin\'ny tadidy')", 'toast memo removed');
fix("showToast('?? Voasora ho tadidiana!')", "showToast('✅ Voasora ho tadidiana!'", 'toast memo saved');

// === PWA BANNER ===
fix('id="pwa-banner-icon">??</div>', 'id="pwa-banner-icon">📲</div>', 'pwa banner icon');

// === MEMO / TADIDY BUTTONS ===
fix("memoBtn.innerHTML = '?? Tadidio'", "memoBtn.innerHTML = '🧠 Tadidio'", 'memo memorize');
fix("memoBtn.innerHTML = '?? Tadidiana'", "memoBtn.innerHTML = '✅ Tadidiana'", 'memo memorized');

// === READ CHAPTER BUTTON ===
fix("readBtn.innerHTML = '?? Vakio toko'", "readBtn.innerHTML = '📖 Vakio toko'", 'read chapter btn');

// === FLASHCARD ===
fix('class="flashcard-hint">?? Tsindrio hahita', 'class="flashcard-hint">👆 Tsindrio hahita', 'flashcard hint');

// === FLASHCARD MODE TITLE ===
fix('<span>?? Fomba famakiana', '<span>📖 Fomba famakiana', 'reading mode title');

// === FLASHCARD NAVIGATION ===
fix(`innerHTML = \`<span>?? Fomba famakiana`, `innerHTML = \`<span>📖 Fomba famakiana`, 'reading mode title (2)');

// === STATISTICS ===
fix('<h3>?? Statistika Vakiteny</h3>', '<h3>📊 Statistika Vakiteny</h3>', 'stats header');
fix('"><span>??</span></div>', '"><span>📊</span></div>', 'stats icon');
fix('style="font-size:18px">??</span></div>', 'style="font-size:18px">📊</span></div>', 'stats icon 2');

// Streak fire emoji
fix('class="streak-fire">??</span>', 'class="streak-fire">🔥</span>', 'streak fire');

// === READING PLAN ICONS ===
fix("icon: '??',\n    days: [\n      { label: '7 Andro'", "icon: '📖',\n    days: [\n      { label: '7 Andro'", 'plan 7 days');
fix("icon: '??',\n    days: [\n      { label: 'A — Sabata'", "icon: '📖',\n    days: [\n      { label: 'A — Sabata'", 'plan sabata');
fix("icon: '??',\n    days: [\n      {label: '30 Salamo'", "icon: '📖',\n    days: [\n      {label: '30 Salamo'", 'plan 30 psalms');

// === RECENT READING ===
fix('class="recent-label">?? Novakiana farany</div>', 'class="recent-label">🕐 Novakiana farany</div>', 'recent reads');

// === FAVORITES BUTTON (AI assistant) ===
fix("favItem.textContent = '??'", "favItem.textContent = '⭐'", 'fav item star');

// === AI: Favorites, Audio, Plan in header ===
fix("'? Favorites, ?? Fihainoana, ?? Plan vakiteny", "'⭐ Favorites, 🎵 Fihainoana, 📖 Plan vakiteny", 'ai header info');

// === AI: Fikarohana ===
fix("text:'?? Fikarohanao farany'", "text:'🔍 Fikarohanao farany'", 'ai recent searches');
fix("text:'?? Tsy nahita ny boky'", "text:'🔍 Tsy nahita ny boky'", 'ai book not found');
fix("text:'?? Tsy nisy fikarohana natao'", "text:'🔍 Tsy nisy fikarohana natao'", 'ai no search');

// === AI: Book/chapter suggestions ===
fix("text:`?? \${bookMatch.name}", "text:`📖 \${bookMatch.name}", 'ai book match');
fix("text:`?? \${char.name}", "text:`👤 \${char.name}", 'ai character match');
fix("text:`?? Nahita boky", "text:`📖 Nahita boky", 'ai found books');
// Nahita andininy (with fuzzy flag check)
fix("label=found.fuzzy?\`?? Nahita andininy", "label=found.fuzzy?\`🔍 Nahita andininy", 'ai found fuzzy');
fix("\`?? Nahita andininy \${r.length}", "\`📖 Nahita andininy \${r.length}", 'ai found verses');

// === AI: Clear history ===
fix("text:'??? Voafafa ny tantaran", "text:'🗑️ Voafafa ny tantaran", 'ai clear history');

// === AI: Next verse ===
fix("text:'?? Tsy misy andininy manaraka", "text:'⏭️ Tsy misy andininy manaraka", 'ai no next verse');

// === AI: Quick chips (search suggestions) ===
// '?? Androany', '?? Mampahery', '?? Fitiavana', '?? Vavaka', '?? Sabata', etc.
// These appear in suggested searches
fix("label:'?? Androany'", "label:'📅 Androany'", 'chip aujourd hui');
fix("label:'?? Mampahery'", "label:'💪 Mampahery'", 'chip encouragement');
fix("label:'?? Fitiavana'", "label:'❤️ Fitiavana'", 'chip amour');
fix("label:'?? Vavaka'", "label:'🙏 Vavaka'", 'chip priere');
fix("label:'?? Sabata'", "label:'📖 Sabata'", 'chip sabbat');
fix("label:'?? Fahatongavany'", "label:'👑 Fahatongavany'", 'chip avenement');
fix("label:'?? Mosesy'", "label:'👤 Mosesy'", 'chip Moise');
fix("label:'?? Davida'", "label:'👤 Davida'", 'chip David');
fix("label:'?? Aléatoire'", "label:'🎲 Aléatoire'", 'chip aleatoire');
// Also the 'popOver' version in baiboly search
fix("{label:'?? Androany',val:'verset androany'}", "{label:'📅 Androany',val:'verset androany'}", 'pop chip aujourdhui');
fix("{label:'?? Mampahery',val:'verset mampahery'}", "{label:'💪 Mampahery',val:'verset mampahery'}", 'pop chip encouragement');
fix("{label:'?? Fitiavana',val:'andininy momba ny fitiavana'}", "{label:'❤️ Fitiavana',val:'andininy momba ny fitiavana'}", 'pop chip amour');
fix("{label:'?? Vavaka',val:'andininy momba ny vavaka'}", "{label:'🙏 Vavaka',val:'andininy momba ny vavaka'}", 'pop chip priere');
fix("{label:'?? Sabata',val:'andininy momba ny sabata'}", "{label:'📖 Sabata',val:'andininy momba ny sabata'}", 'pop chip sabbat');
fix("{label:'?? Fahatongavany',val:'andininy momba ny fahatongavan'}", "{label:'👑 Fahatongavany',val:'andininy momba ny fahatongavan'}", 'pop chip avenement');
fix("{label:'?? Mosesy',val:'andininy momba i Mosesy'}", "{label:'👤 Mosesy',val:'andininy momba i Mosesy'}", 'pop chip Moise');
fix("{label:'?? Davida',val:'andininy momba i Davida'}", "{label:'👤 Davida',val:'andininy momba i Davida'}", 'pop chip David');
fix("{label:'?? Aléatoire',val:'verset maimaimpoana'}", "{label:'🎲 Aléatoire',val:'verset maimaimpoana'}", 'pop chip aleatoire');

// === AI: Chip labels ===
fix("chips.push({label:\`?? \${char.name}\`", "chips.push({label:\`👤 \${char.name}\`", 'chip char name');
fix("chips.push({label:'?? Verset androany'", "chips.push({label:'📅 Verset androany'", 'chip verset androany');
fix("chips.push({label:'?? Verset mampahery'", "chips.push({label:'💪 Verset mampahery'", 'chip verset mampahery');
fix("chips.push({label:'?? Vakio toko...'", "chips.push({label:'📖 Vakio toko...'", 'chip vakio toko');

// === AI: Verset du jour / random ===
fix("isVod:true,text:\`?? Verset androany", "isVod:true,text:\`📅 Verset androany", 'ai verse du jour');
fix("chips.push({ html: '?? Verset androany'", "chips.push({ html: '📅 Verset androany'", 'chip html verset jour');
fix("chips.push({ html: '?? Verset mampahery'", "chips.push({ html: '💪 Verset mampahery'", 'chip html encouragement');
fix("chips.push({ html: '?? Vakio toko...'", "chips.push({ html: '📖 Vakio toko...'", 'chip html vakio');

// === AI: Found books / verses ===
fix("chips.push({ html: \`\${t.icon || '???'} \${t.label}", "chips.push({ html: \`\${t.icon || '📖'} \${t.label}", 'chip theme fallback');
fix("chips.push({ html: \`?? \${c.name}\`", "chips.push({ html: \`👤 \${c.name}\`", 'chip character');
fix("'<span style=\"color:#FFD60A\">??</span> <strong>\${r.book", "'<span style=\"color:#FFD60A\">⭐</span> <strong>\${r.book", 'chip book result');

// === AI: Reading mode indicator ===
fix("showToastPro('?? Fomba famakiana", "showToastPro('📖 Fomba famakiana", 'reading mode toast');

// === AI: Multi-select ===
fix("showToastPro(\`?? \${multiSelectState.selected", "showToastPro(\`✅ \${multiSelectState.selected", 'multi-select toast');
fix("showToastPro('?? Misokatra ny varimbazaha", "showToastPro('🌐 Misokatra ny varimbazaha", 'browser open toast');

// === AI: Filter buttons ===
fix("createFilterBtn('?? Rehetra'", "createFilterBtn('📋 Rehetra'", 'filter all');
fix("createFilterBtn('?? TT'", "createFilterBtn('📜 TT'", 'filter AT');
fix("createFilterBtn('?? Boky'", "createFilterBtn('📖 Boky'", 'filter book');

// === DAY PLAN LABELS ===
// Fix the pattern: `${day.icon||'??'} ${day.label}`
fix("day.icon||'??'", "day.icon||'📖'", 'day plan icon');

// === STATS BUTTON ===
fix("statsBtn.innerHTML = '??'", "statsBtn.innerHTML = '📊'", 'stats btn');

// === CLOSE FOCUS BUTTON ===
fix("close-fc\">? Hiala</button>", "close-fc\">❌ Hiala</button>", 'close flashcard');

// === CANCEL BUTTON ===
fix('"ms-cancel" aria-label="Hiala">?</button>', '"ms-cancel" aria-label="Hiala">❌</button>', 'cancel btn');

// === NAVIGATION FOOTER BOTTOM LINKS ===
// <a href="..." title="Fandraisana">??</a>
// <a href="index.html?page=baiboly" title="Baiboly">??</a>
// etc.
let navLinks = c.match(/<a\s+href="[^"]*"\s*(?:class="[^"]*"\s*)?title="([^"]*)">\?(\?+)?<\/a>/g);
if (navLinks) {
  navLinks.forEach(link => {
    const titleMatch = link.match(/title="([^"]+)"/);
    if (titleMatch) {
      const title = titleMatch[1];
      let icon;
      if (title.includes('Fandraisana') || title.includes('Accueil')) icon = '🏠';
      else if (title.includes('Baiboly') || title.includes('Bible')) icon = '📖';
      else if (title.includes('Fihirana') || title.includes('Hymne') || title.includes('Hira')) icon = '🎵';
      else if (title.includes('Annonce')) icon = '📢';
      else if (title.includes('Chat') || title.includes('Assistant')) icon = '💬';
      else if (title.includes('Sabata')) icon = '📖';
      else icon = '🔗';
      const newLink = link.replace(/>\?+<\/a>/, `>${icon}</a>`);
      c = c.replace(link, newLink);
      totalFixes++;
      console.log('  nav link ' + title + ': ' + link.match(/>\?+<\/a>/) + ' → ' + icon);
    }
  });
}

// === THEME ICONS (THEMES array) ===
// These are in the format: 'keyword':{label:'...',keys:[...],icon:'??',cat:'...'}
// The icon field has ?? that needs to be replaced based on the theme keyword
const themeIconMap = {
  'fanantenana': '🌟',  // hope
  'antenaina': '🌟',
  'vavaka': '🙏',      // prayer
  'famonjena': '✝️',   // salvation
  'fanavotana': '✝️',
  'fandriam-pahalemana': '🕊️', // peace
  'mampiadana': '🕊️',
  'fahendrena': '💡',   // wisdom
  'finoana': '🙏',      // faith
  'tsy mino': '❓',
  'herim-panahy': '💪', // strength
  'hery': '⚡',
  'famela-keloka': '❤️', // forgiveness
  'tsaratsara': '❤️',
  'harena': '💰',      // riches
  'farimbolana': '💰',
  'fahafatesana': '⚰️', // death
  'tombondrena': '⚰️',
  'fitsanganana': '✝️', // resurrection
  'mitsangana': '✝️',
  'jesosy': '👑',      // Jesus
  'mpamonjy': '👑',
  'mpanavot': '👑',
  'mpiasan': '👑',
  'fiavian': '🌄',     // coming
  'fanantenan': '🌟',
  'andro': '📅',
  'fitsarana': '⚖️',   // judgment
  'anjaran': '⚖️',
  'fanjakany': '👑',   // kingdom
  'batisa': '💧',      // baptism
  'rano': '💧',
  'ampahafolony': '💰', // tithe
  'fizarana': '💰',
  'zara': '💰',
  'fikelezan-kena': '🍞', // fasting
  'tsy misotro': '🍞',
  'fanabeazana': '📚',  // education
  'mianatra': '📚',
  'fiangonana': '⛪',   // church
  'mpitory': '⛪',
  'fanambadiana': '💑', // marriage
  'mpivady': '💑',
  'fianakavia': '👨‍👩‍👧‍👦', // family
  'tanana': '👨‍👩‍👧‍👦',
  'asa': '🔧',         // work
  'fahavalo': '👿',    // enemy
  'fahamarinana': '⚖️', // truth
  'mampihatra': '⚖️',
  'fifaliana': '😊',   // joy
  'setriny': '😊',
  'fahatahorana': '🙏', // fear of God
  'driamanitra': '✝️',
  'fitiavana': '❤️',   // love
  'ankatiavana': '❤️',
  'fanetren-tena': '🙇', // humility
  'fahalemem-panahy': '🙇',
  'lemy fanahy': '🙇',
  'fanahin': '🔮',     // spirit of prophecy
  'maminany': '🔮',
  'firehetam-po': '🔥', // zeal
  'iraisan': '🤝',
  'fanalefahana': '⚔️', // trial
  'miatrika': '⚔️',
  'rano-aina': '💧',   // water of life
  'fiainana': '💧',
  'fahazavana': '💡',  // light
  'arozona': '💡',
  'afo': '🔥',
  'feno': '💯',       // fullness
  'tompon': '👑',
  'fiainana mandrakizay': '♾️', // eternal life
  'maharitra': '♾️',
  'fifohazam-panahy': '🔥', // revival
  'mifoha': '🔥',
  'heriny': '⚡',      // power
  'fahasoavana': '🌟',  // grace
  'fahatsarana': '🌟',
  'fahafahana': '🕊️',  // freedom
  'fanafahana': '🕊️',
  'fitsaharana': '📖',  // rest/sabbath
  'an-tsasatra': '📖',
  'fanompoana': '⛪',   // worship
  'pivavahana': '⛪',
  'fihavanana': '🤝',  // fellowship
  'tambatra': '🤝',
  'fahadiovana': '✨',  // purity
  'hadio': '✨',
  'fahari-toky': '💪', // patience
  'paharetana': '💪',
  'fampihavanana': '🕊️', // reconciliation
  'fahatsorana': '🌱',  // simplicity
  'ambany': '🌱',
  'firaisan-tsaina': '🤝', // unity
  'miray saina': '🤝',
  'fahatokiana': '🤝',  // trust
  'itokiana': '🤝',
  'famindram-po': '❤️', // mercy
  'fiantrana': '❤️',
};

// Process THEMES object entries with icon:'??'
// Match pattern: 'keyword':{label:'...',keys:[...],icon:'??',cat:'...'}
let themeCount = 0;
for (const [key, icon] of Object.entries(themeIconMap)) {
  // Try to match: 'key':{...icon:'??',...}
  const pattern = `'${key}':{`;
  let idx = 0;
  while ((idx = c.indexOf(pattern, idx)) !== -1) {
    // Find the icon field within this theme entry
    let iconIdx = c.indexOf("icon:'", idx);
    if (iconIdx !== -1) {
      let iconStart = iconIdx + 6;
      let iconEnd = c.indexOf("'", iconStart);
      if (iconEnd > iconStart) {
        let currentIcon = c.substring(iconStart, iconEnd);
        if (currentIcon.match(/^\?+$/)) {
          c = c.substring(0, iconStart) + icon + c.substring(iconEnd);
          themeCount++;
        }
      }
    }
    idx++;
  }
}
if (themeCount > 0) { totalFixes += themeCount; console.log('  theme icons: ' + themeCount + 'x'); }

// === CSS PSEUDO-ELEMENTS (content:"??") ===
fix('content:"???";font-size:15px;line-height:1', 'content:"📖";font-size:15px;line-height:1', 'CSS pseudo book');
// There are 3 identical ones, all replaced at once

// === DAY MODE TOGGLE ===
fix("const modeBtnInner = isDayMode ? '??' : '??'", "const modeBtnInner = isDayMode ? '☀️' : '🌙'", 'mode toggle sun/moon');
fix("showToast(isDayMode ? '?? Mode Andro' : '?? Mode Alina')", "showToast(isDayMode ? '☀️ Mode Andro' : '🌙 Mode Alina')", 'mode toast');

// === FONT TOGGLE ===
fix("fontBtnInner = isSansSerif ? '??' : '??'", "fontBtnInner = isSansSerif ? '📝' : '📜'", 'font toggle');

// === SHARE BUTTON (inline) ===
fix('aria-label="Partager">??</button>', 'aria-label="Partager">📤</button>', 'share btn aria');

// === CANVAS WATERMARK ===
fix("ctx.fillText('??  Baiboly Malagasy'", "ctx.fillText('📖  Baiboly Malagasy'", 'canvas watermark');

// === BOOK NAME FRENCH (already has proper accented chars from encoding fix) ===
// These lines look OK now, but let me check

// === ERROR MESSAGES ===
fix("return{error:'?? Clé API Groq invalide", "return{error:'❌ Clé API Groq invalide", 'groq invalid key');
fix("return{error:'?? Pas de connexion internet", "return{error:'🌐 Pas de connexion internet", 'groq no internet');
fix("text:'??? Votre navigateur ne prend", "text:'⚠️ Votre navigateur ne prend", 'browser not supported');

// === MULTI-SELECT VERSE ACTIONS ===
fix("'>?? Zarao</button>", "'>📤 Zarao</button>", 'vsb share');
fix('id="ms-cancel" aria-label="Hiala">?</button>', 'id="ms-cancel" aria-label="Hiala">❌</button>', 'vsb cancel');

// === BIBLE SEARCH CHIPS ===
fix("html: \`<span style=\"color:#5AC8FA\">??</span> \${b.name}\`", "html: \`<span style=\"color:#5AC8FA\">📖</span> \${b.name}\`", 'search chip book');

// === READING PLAN STATS ===
fix('class="plan-stat-icon" style="font-size:18px">??</span>', 'class="plan-stat-icon" style="font-size:18px">📊</span>', 'plan stat icon');
fix('class="plan-stat-icon" style="font-size:18px">??</span>', 'class="plan-stat-icon" style="font-size:18px">📊</span>', 'plan stat icon (already done)');

// === DAY LABEL IN PLAN ===
fix("day.icon||'??'", "day.icon||'📖'", 'day plan fallback');

// === FLOATING AI FAB ===
// The FAB has a status-based icon
fix("status==='listening'?'???'", "status==='listening'?'🎤'", 'fab listening');
fix("status==='thinking'?'??'", "status==='thinking'?'🤔'", 'fab thinking');
fix(":'?'", ":'💬'", 'fab idle');

// === ND-LOGO ===
fix('class="nd-logo-icon">??</div>', 'class="nd-logo-icon">📖</div>', 'nd logo icon');

// === STATS RECENT ===
fix('class="recent-label">?? Novakiana farany</div>', 'class="recent-label">🕐 Novakiana farany</div>', 'recent label (again)');

// === FILTER BUTTONS ===
// Already handled some, but let me check for '?? Rehetra' etc more broadly
let filtIdx = 0;
while ((filtIdx = c.indexOf('createFilterBtn', filtIdx)) !== -1) {
  let parenStart = c.indexOf('(', filtIdx);
  let parenEnd = c.indexOf(')', parenStart);
  if (parenStart !== -1 && parenEnd !== -1) {
    let args = c.substring(parenStart + 1, parenEnd);
    let parts = args.split(',').map(s => s.trim().replace(/^'(.*)'$/, '$1'));
    if (parts.length >= 2 && parts[0].match(/^\?+$/)) {
      let label = parts[1] || '';
      let icon;
      if (label === 'Rehetra') icon = '📋';
      else if (label === 'TT' || label === 'taloha') icon = '📜';
      else if (label === 'TV' || label === 'vaovao') icon = '📖';
      else if (label === 'Boky') icon = '📖';
      else icon = '📖';
      c = c.substring(0, parenStart + 1) + "'" + icon + "'" + c.substring(parenStart + 1 + parts[0].length + 2);
      totalFixes++;
      console.log('  createFilterBtn ' + label + ': ' + parts[0] + ' → ' + icon);
    }
  }
  filtIdx++;
}

// === CSS CONTENT (remaining) ===
// content: '??'; - decorations
// These are likely just emoji decorations
fix("content: '??';", "content: '⭐';", 'CSS content star');
fix("content: '??';", "content: '📖';", 'CSS content book (2star pattern)');

console.log('\nTotal fixes: ' + totalFixes);
fs.writeFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html', c);
console.log('Written to baibolyMG_v2.html');
