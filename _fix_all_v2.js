const fs = require('fs');
let c = fs.readFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html').toString('utf8');
let fixes = 0;

function replaceExact(from, to, desc) {
  const re = new RegExp(from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
  const m = c.match(re);
  if (m) { c = c.replace(re, to); fixes += m.length; console.log('  ' + desc + ': ' + m.length + 'x'); }
}

// === 1. AI HELP TEXT (Haiko block) ===
// This is in a JS string: 'Haiko:\n• ?? Référence: ...'
const aiHelpBlock = c.indexOf('Haiko:');
if (aiHelpBlock !== -1) {
  // Find the full help string - it's likely in a template literal or single-quoted string
  // Let's find the end of the Haiko block
  let blockEnd = c.indexOf("';const", aiHelpBlock);
  if (blockEnd === -1) blockEnd = c.indexOf("';", aiHelpBlock);
  if (blockEnd === -1) blockEnd = c.indexOf("`;", aiHelpBlock);
  
  if (blockEnd !== -1 && blockEnd - aiHelpBlock < 500) {
    let block = c.substring(aiHelpBlock, blockEnd + 2);
    let oldBlock = block;
    
    // Fix the icons in the Haiko text
    block = block.replace(/• \?\? Référence/g, '• 🔍 Référence');
    block = block.replace(/• \?\? Teny/g, '• 🔤 Teny');
    block = block.replace(/• \?\? Lohahevitra/g, '• 📖 Lohahevitra');
    block = block.replace(/• \?\? Olona/g, '• 👤 Olona');
    block = block.replace(/• \?\? Vakio/g, '• 📖 Vakio');
    block = block.replace(/• \?\? Aléatoire/g, '• 🎲 Aléatoire');
    block = block.replace(/• \?\? Androany/g, '• 📅 Androany');
    block = block.replace(/\? Favorites: "fav"/g, '⭐ Favorites: "fav"');
    block = block.replace(/\? Vaovao v3: \? Favorites, \?\? Fihainoana, \?\? Plan vakiteny/g, '⭐ Vaovao v3: ⭐ Favorites, 🎵 Fihainoana, 📖 Plan vakiteny');
    
    c = c.substring(0, aiHelpBlock) + block + c.substring(blockEnd + 2);
    fixes++;
    console.log('  AI help text block: 1x (~15 icons)');
  }
}

// === 2. THEME ICONS - direct icon replacement ===
// Instead of matching by keyword, find ALL icon:'?+' in theme definitions
let themeFixCount = 0;
let searchStart = 0;
// Find each THEMES entry and fix icon
let entryStart = c.indexOf("'fanantenana':", 0);
if (entryStart === -1) entryStart = c.indexOf("'fanantenan':", 0);
if (entryStart === -1) entryStart = c.indexOf("const THEMES", 0);
if (entryStart >= 0) {
  // Find the end of THEMES object
  let themesEnd = c.indexOf(";// ---", entryStart);
  if (themesEnd === -1) themesEnd = c.indexOf("];", entryStart);
  if (themesEnd === -1) themesEnd = entryStart + 50000;
  
  let themesBlock = c.substring(entryStart, themesEnd);
  let origThemes = themesBlock;
  
  // Map of theme label to icon
  function iconForLabel(label) {
    const l = label.toLowerCase();
    if (l.includes('fananten') || l.includes('espoir') || l.includes('hope')) return '🌟';
    if (l.includes('vavaka') || l.includes('prière') || l.includes('prayer')) return '🙏';
    if (l.includes('famonjen') || l.includes('salut') || l.includes('salvation')) return '✝️';
    if (l.includes('fiadan') || l.includes('paix') || l.includes('peace')) return '🕊️';
    if (l.includes('fahendren') || l.includes('sagesse') || l.includes('wisdom')) return '💡';
    if (l.includes('finoana') || l.includes('foi') || l.includes('faith')) return '🙏';
    if (l.includes('herim') || l.includes('courage') || l.includes('strength') || l.includes('hery') || l.includes('force')) return '💪';
    if (l.includes('famelan') || l.includes('pardon') || l.includes('forgive')) return '❤️';
    if (l.includes('harena') || l.includes('richesse') || l.includes('riche') || l.includes('wealth')) return '💰';
    if (l.includes('fahafatesan') || l.includes('mort') || l.includes('death')) return '⚰️';
    if (l.includes('fitsangan') || l.includes('résurrect') || l.includes('resurrect')) return '✝️';
    if (l.includes('jesosy') || l.includes('jésus') || l.includes('jesus') || l.includes('mpamonjy') || l.includes('sauveur')) return '👑';
    if (l.includes('sabat') || l.includes('sabbat') || l.includes('sabbath')) return '📖';
    if (l.includes('fahatongav') || l.includes('avèn') || l.includes('advent') || l.includes('avenir') || l.includes('fiavian')) return '🌄';
    if (l.includes('fitsaran') || l.includes('jugement') || l.includes('judgment')) return '⚖️';
    if (l.includes('anjaran') || l.includes('destin')) return '⚖️';
    if (l.includes('fanjakan') || l.includes('royaume') || l.includes('kingdom') || l.includes('mpanjaka')) return '👑';
    if (l.includes('batisa') || l.includes('baptême') || l.includes('baptism')) return '💧';
    if (l.includes('ampahafolo') || l.includes('dîme') || l.includes('tithe') || l.includes('vola') || l.includes('zara') || l.includes('fizarana')) return '💰';
    if (l.includes('fikelez') || l.includes('jeûne') || l.includes('fast') || l.includes('mofo') || l.includes('divay')) return '🍞';
    if (l.includes('fanabeazan') || l.includes('éducat') || l.includes('education')) return '📚';
    if (l.includes('fiangonan') || l.includes('église') || l.includes('church') || l.includes('mpitory')) return '⛪';
    if (l.includes('fianakavi') || l.includes('famille') || l.includes('family') || l.includes('mpivady') || l.includes('mariage') || l.includes('fanambadian') || l.includes('vady')) return '👨‍👩‍👧‍👦';
    if (l.includes('asa') || l.includes('travail') || l.includes('work')) return '🔧';
    if (l.includes('fahaval') || l.includes('ennemi') || l.includes('enemy')) return '👿';
    if (l.includes('fahamarinan') || l.includes('vérité') || l.includes('truth') || l.includes('justice')) return '⚖️';
    if (l.includes('fifalian') || l.includes('joie') || l.includes('joy')) return '😊';
    if (l.includes('fahatahor') || l.includes('crainte') || l.includes('fear')) return '🙏';
    if (l.includes('fitiav') || l.includes('amour') || l.includes('love')) return '❤️';
    if (l.includes('fanetren') || l.includes('humilité') || l.includes('humility') || l.includes('fahalem')) return '🙇';
    if (l.includes('fanahin') || l.includes('esprit') || l.includes('spirit') || l.includes('maminany') || l.includes('prophétie') || l.includes('prophecy')) return '🔮';
    if (l.includes('firehetam') || l.includes('zèle') || l.includes('zeal') || l.includes('firaisana') || l.includes('unité') || l.includes('unite')) return '🔥';
    if (l.includes('fanalefahan') || l.includes('épreuve') || l.includes('trial') || l.includes('persécution') || l.includes('persecution')) return '⚔️';
    if (l.includes('rano-ain') || l.includes('eau') || l.includes('water') || l.includes('fiainana')) return '💧';
    if (l.includes('fahazavan') || l.includes('lumière') || l.includes('light') || l.includes('arozona') || l.includes('afo') || l.includes('feu')) return '💡';
    if (l.includes('fenon') || l.includes('plénitude') || l.includes('fullness') || l.includes('feno') || l.includes('rempli')) return '💯';
    if (l.includes('mandrakizay') || l.includes('éternel') || l.includes('eternal') || l.includes('maharitra')) return '♾️';
    if (l.includes('fifohazan') || l.includes('réveil') || l.includes('revival') || l.includes('mifoha')) return '🔥';
    if (l.includes('fahasoavan') || l.includes('grâce') || l.includes('grace')) return '🌟';
    if (l.includes('fahafahan') || l.includes('liberté') || l.includes('freedom') || l.includes('fanafahana')) return '🕊️';
    if (l.includes('fitsaharan') || l.includes('repos') || l.includes('rest')) return '📖';
    if (l.includes('fanompoan') || l.includes('servi') || l.includes('service') || l.includes('pivavahana') || l.includes('culte') || l.includes('worship')) return '⛪';
    if (l.includes('fihavanan') || l.includes('communi') || l.includes('fellowship') || l.includes('tambatra')) return '🤝';
    if (l.includes('fahadiovan') || l.includes('pureté') || l.includes('purity') || l.includes('hadio')) return '✨';
    if (l.includes('fahari') || l.includes('patience') || l.includes('paharetana') || l.includes('endurance')) return '💪';
    if (l.includes('fampihavanan') || l.includes('réconci') || l.includes('reconciliation')) return '🕊️';
    if (l.includes('fahatsoran') || l.includes('simplicité') || l.includes('simplicity') || l.includes('ambany')) return '🌱';
    if (l.includes('firaisan') || l.includes('saina') || l.includes('miray') || l.includes('unité') || l.includes('unite')) return '🤝';
    if (l.includes('fahatokian') || l.includes('confian') || l.includes('trust') || l.includes('itokiana')) return '🤝';
    if (l.includes('famindram') || l.includes('miséricorde') || l.includes('mercy') || l.includes('fiantrana')) return '❤️';
    if (l.includes('fankalaz') || l.includes('louange') || l.includes('praise')) return '🙌';
    if (l.includes('fideran') || l.includes('louange') || l.includes('praise')) return '🙌';
    if (l.includes('fifampitso') || l.includes('pardon') || l.includes('forgive')) return '❤️';
    return '📖';  // default
  }
  
  // Find all icon:'??' patterns and fix based on label
  let iconIdx = 0;
  while ((iconIdx = themesBlock.indexOf("icon:'", iconIdx)) !== -1) {
    let start = iconIdx + 6;
    let end = themesBlock.indexOf("'", start);
    if (end > start) {
      let currentIcon = themesBlock.substring(start, end);
      if (currentIcon.match(/^\?+$/)) {
        // Find the label of this theme
        let entryStart2 = themesBlock.lastIndexOf("'", iconIdx - 20);
        let entryEnd2 = themesBlock.indexOf("'", entryStart2 + 1);
        if (entryEnd2 > entryStart2 && entryStart2 >= 0) {
          // Find the label field after the entry
          let labelStart = themesBlock.indexOf("label:'", iconIdx - 300);
          if (labelStart === -1 || labelStart > iconIdx) labelStart = themesBlock.indexOf('label:"', iconIdx - 300);
          if (labelStart !== -1 && labelStart < iconIdx) {
            let labelStartVal = labelStart + 7;
            let labelEnd = themesBlock.indexOf("'", labelStartVal);
            if (labelEnd === -1 || labelEnd > iconIdx) {
              labelStartVal = labelStart + 7;
              labelEnd = themesBlock.indexOf('"', labelStartVal);
            }
            if (labelEnd > labelStartVal && labelEnd < iconIdx) {
              let label = themesBlock.substring(labelStartVal, labelEnd);
              let newIcon = iconForLabel(label);
              themesBlock = themesBlock.substring(0, start) + newIcon + themesBlock.substring(end);
              themeFixCount++;
            }
          }
        }
      }
    }
    iconIdx++;
  }
  
  if (themeFixCount > 0) {
    c = c.substring(0, entryStart) + themesBlock + c.substring(themesEnd);
    fixes += themeFixCount;
    console.log('  theme icons (label-based): ' + themeFixCount + 'x');
  }
}

// === 3. CONTROL BUTTONS (day/night, font toggle) ===
replaceExact("textContent = isDayMode ? '??' : '??'", "textContent = isDayMode ? '☀️' : '🌙'", 'ctrl mode');
replaceExact("textContent = isSansSerif ? '??' : '??'", "textContent = isSansSerif ? '📝' : '📜'", 'ctrl font');
replaceExact("'?? Police moderne' : '?? Police classique'", "'📝 Police moderne' : '📜 Police classique'", 'ctrl police toast');

// === 4. HIGHLIGHT TOASTS ===
replaceExact("already ? '?? Surlignage retiré' : '?? ' + c.label", "already ? '❌ Surlignage retiré' : '✅ ' + c.label", 'highlight toast');

// === 5. NOTES ===
replaceExact("innerHTML = `?? Fanamarihana", "innerHTML = `📝 Fanamarihana", 'note header');
replaceExact("delBtn.textContent = '??'", "delBtn.textContent = '🗑️'", 'del btn');

// === 6. READING PLAN ICONS ===
replaceExact("label: '7 Andro', icon: '??'", "label: '7 Andro', icon: '📖'", 'plan 7j');
replaceExact("label: 'SDA — Sabata', icon: '??'", "label: 'SDA — Sabata', icon: '📖'", 'plan sab');
replaceExact("label: '30 Salamo', icon: '??'", "label: '30 Salamo', icon: '📖'", 'plan 30');

// === 7. VERSE SELECTOR ACTIONS ===
replaceExact('aria-label="Copier les versets">?? Adikao</button>', 'aria-label="Copier les versets">📋 Adikao</button>', 'vsb copy');
replaceExact('aria-label="Partager les versets">?? Zarao</button>', 'aria-label="Partager les versets">📤 Zarao</button>', 'vsb share');

// === 8. EMPTY STATE / LOADING ===
// The large ?? in empty states
replaceExact('font-size:48px;margin-bottom:16px">??</div>', 'font-size:48px;margin-bottom:16px">📖</div>', 'empty state');

// === 9. FAB STATUS ICON ===  
replaceExact("status==='listening'?'🎤':status==='thinking'?'?':'??'", "status==='listening'?'🎤':status==='thinking'?'🤔':'💬'", 'fab status');

// === 10. MEMO BUTTONS ===
replaceExact("alreadyMemo ? '?? Tadidiana' : '?? Tadidio'", "alreadyMemo ? '✅ Tadidiana' : '🧠 Tadidio'", 'memo toggle');

// === 11. TOAST: Neporina / Nesorina ===
replaceExact("'?? Nesorina tamin'\\''ny tadidy'", "'🗑️ Nesorina tamin\\'ny tadidy'", 'toast memo removed');

// === 12. FAVORITES BNAV ICON (fixed directly) ===
replaceExact("favItem.querySelector('.bnav-icon').textContent = '??'", "favItem.querySelector('.bnav-icon').textContent = '⭐'", 'fav bnav icon');

// === 13. BOOKMARK TOAST ===
replaceExact("showToast(`?? ${book.name} ${chapter}:${vn}`)", "showToast(`✅ ${book.name} ${chapter}:${vn}`)", 'toast bookmark');

// === 14. FOCUS MODE: Plein écran ===
replaceExact("focusMode?'❌ Hiala amin'\\''ny fomba feno':'?? Plein écran'", "focusMode?'❌ Hiala amin\\'ny fomba feno':'🖥️ Plein écran'", 'focus plein ecran');

// === 15. QUICK CHIPS: L'amour ===
replaceExact("label:'?? L\\'amour'", "label:'❤️ L\\'amour'", 'chip amour');

// === 16. STATS BUTTON ===
replaceExact('style="cursor:pointer;font-family:var(--font-ui)">?? Statistika</button>', 'style="cursor:pointer;font-family:var(--font-ui)">📊 Statistika</button>', 'stats button');

// === 17. AI WELCOME - remaining ?? in the welcome text ===
// Find all ? in the WELCOME string
let welStart = c.indexOf("const WELCOME='");
if (welStart === -1) welStart = c.indexOf('const WELCOME="');
if (welStart >= 0) {
  // Find end of the welcome string
  let quoteChar = c[welStart + 15]; // ' or "
  let welEnd = c.indexOf(quoteChar + ';', welStart + 16);
  if (welEnd !== -1) {
    let welBlock = c.substring(welStart, welEnd + 1);
    // Fix remaining ?? in welcome
    welBlock = welBlock.replace(/• \?\?/g, '• 🔍');
    welBlock = welBlock.replace(/• \?/g, '• ⭐');
    c = c.substring(0, welStart) + welBlock + c.substring(welEnd + 1);
    fixes++;
    console.log('  WELCOME text: 1x');
  }
}

// === 18. CSS CONTENT with ?? ===
// Fix CSS content that has ?? (likely decorations)
replaceExact("content: '??';", "content: '⭐';", 'CSS content');

// === 19. AI: Text messages with ?? ===
replaceExact("text:'?? Tsy mbola nisy fikarohana nataonareo", "text:'🔍 Tsy mbola nisy fikarohana nataonareo", 'ai no search');

console.log('\nTotal fixes in this pass: ' + fixes);
fs.writeFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html', c);
console.log('Written.');
