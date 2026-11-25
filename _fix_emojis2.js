const fs = require('fs');
let c = fs.readFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html').toString('utf8');
let count = 0;

// === VerseText copy button ===
// refCopied?'? Voakopy': -> refCopied?'✅ Voakopy':
if (c.includes("refCopied?'? Voakopy'")) {
  c = c.replace(/refCopied\?'\? Voakopy'/g, "refCopied?'\u2705 Voakopy'");
  count++;
  console.log("Fixed refCopied Voakopy");
}

// === Song slide copy button (inside fihirana-style slides in baiboly) ===
// copied?'? Voakopy':'?? Kopa' -> copied?'✅ Voakopy':'📋 Kopa'
let re = /copied\?'\? Voakopy':'\?\? Kopa'/g;
if (re.test(c)) {
  c = c.replace(re, "copied?'\u2705 Voakopy':'\uD83D\uDCCB Kopa'");
  count++;
  console.log("Fixed copied Voakopy / Kopa");
}

// === Favorite button ===
// isFav?'?':'?' -> isFav?'❤️':'🤍'
re = /isFav\?'\?':'\?'/g;
if (re.test(c)) {
  c = c.replace(re, "isFav?'\u2764\uFE0F':'\uD83E\uDD0D'");
  count++;
  console.log("Fixed isFav button");
}

// === Bottom nav Nalaina icon ===
// <span class="bnav-icon">?</span>
let idx = c.indexOf('class="bnav-icon">');
if (idx >= 0) {
  let start = c.indexOf('>', idx) + 1;
  let end = c.indexOf('<', start);
  if (end > start) { 
    let icon = c.substring(start, end);
    if (icon === '?') {
      c = c.substring(0, start) + '\u2B50' + c.substring(end);
      count++;
      console.log("Fixed bnav-icon Nalaina");
    }
  }
}

// Also check other bnav icons
let bnavIdx = 0;
bnavIdx = c.indexOf('class="bnav-icon">');
if (bnavIdx >= 0) {
  // Find all bnav-icon elements
  let ci = 0;
  while ((ci = c.indexOf('bnav-icon', ci)) !== -1) {
    let startTag = c.indexOf('>', ci) + 1;
    let endTag = c.indexOf('<', startTag);
    if (endTag > startTag) {
      let content = c.substring(startTag, endTag);
      if (content === '?') {
        // Determine which nav item this is by looking at nearby text
        let contextStart = Math.max(0, ci - 100);
        let context = c.substring(contextStart, endTag + 10);
        if (context.includes('Baiboly')) c = c.substring(0, startTag) + '\uD83D\uDCD6' + c.substring(endTag);
        else if (context.includes('Fikarohana') || context.includes('Search')) c = c.substring(0, startTag) + '\uD83D\uDD0D' + c.substring(endTag);
        else if (context.includes('Nalaina') || context.includes('Favoris') || context.includes('favori')) c = c.substring(0, startTag) + '\u2B50' + c.substring(endTag);
        else c = c.substring(0, startTag) + '\u2753' + c.substring(endTag); // fallback
        count++;
        console.log("Fixed bnav-icon");
      }
    }
    ci++;
  }
}

// === Toast messages ===
// '?? Voakopy!' -> '✅ Voakopy!'
if (c.includes("'?? Voakopy!'")) {
  c = c.replace(/'\\?\\?\? Voakopy!'/g, "'\u2705 Voakopy!'");
  count++;
  console.log("Fixed toast Voakopy");
}

// '?? Voakopy ho zaraina!' -> '✅ Voakopy ho zaraina!'
let testStr = "'?? Voakopy ho zaraina!'";
if (c.includes(testStr)) {
  c = c.replace(/'\\?\\?\? Voakopy ho zaraina!'/g, "'\u2705 Voakopy ho zaraina!'");
  count++;
  console.log("Fixed toast Voakopy ho zaraina");
}

// Use a simpler approach - find literal '?? Voakopy' patterns
// The escaped version might not work, so let's search differently
let re2 = /\?\? Voakopy/g;
let matches = c.match(re2);
if (matches) {
  console.log("Found " + matches.length + " '?? Voakopy' patterns");
  c = c.replace(/\?\? Voakopy/g, '\u2705 Voakopy');
  count++;
}

// '?? Kopa' -> '📋 Kopa' (in baiboly context too)
let re3 = /\?\? Kopa/g;
if (re3.test(c)) {
  c = c.replace(/\?\? Kopa/g, '\uD83D\uDCCB Kopa');
  count++;
  console.log("Fixed ?? Kopa");
}

// === Focus mode button ===
// '?? Hiala amin\'ny fomba famakiana' -> '❌ Hiala...'
let re4 = /focusMode\?'\?\? Hiala/g;
if (re4.test(c)) {
  c = c.replace(/focusMode\?'\?\? Hiala/g, "focusMode?'\u274C Hiala");
  count++;
  console.log("Fixed focus Hiala");
}

// '?? Feno' -> '🖥️ Feno'
let re5 = /focusMode\?'\?\? Feno/g;
if (!re5.test(c)) {
  re5 = /\?\? Feno/g;
}
if (re5.test(c)) {
  c = c.replace(re5, '\uD83D\uDDA5\uFE0F Feno');
  count++;
  console.log("Fixed ?? Feno");
}

// Actually let's be more careful - match the EXACT patterns
let allQmark = [];
let si = 0;
while ((si = c.indexOf('??', si)) !== -1) {
  let start = Math.max(0, si - 20);
  let end = Math.min(c.length, si + 30);
  allQmark.push(c.substring(start, end).replace(/\n/g, '\\n'));
  si++;
}
console.log("All ?? occurrences (" + allQmark.length + "):");
allQmark.forEach((s, i) => console.log("  " + (i+1) + ": " + s));

if (count > 0) {
  fs.writeFileSync('G:\\SDA\\fihirana\\baibolyMG_v2.html', c);
  console.log("\n" + count + " fixes applied to baibolyMG_v2.html");
} else {
  console.log("\nNo fixes applied");
}
