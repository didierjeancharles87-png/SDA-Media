(function () {
  if (window._voiceSearchLoaded) return;
  window._voiceSearchLoaded = true;

  var BOOKS = [
    [10, 'Genesisy', 'Genese', ['gn', 'gen', 'gene', 'genes', 'genesis', 'genese', 'geneze']],
    [20, 'Eksodosy', 'Exode', ['ex', 'eks', 'exo', 'exod', 'eksodosy', 'exode', 'eksodosi']],
    [30, 'Levitikosy', 'Levitique', ['lv', 'lev', 'levi', 'levitikosy', 'levitique', 'levitikosi']],
    [40, 'Nomery', 'Nombres', ['nb', 'nom', 'nome', 'nomb', 'nomery', 'nombres', 'nombr']],
    [50, 'Deoteronomia', 'Deuteronome', ['dt', 'deo', 'deot', 'deut', 'deoteronomia', 'deuteronome']],
    [60, 'Josoa', 'Josue', ['js', 'jos', 'joso', 'josu', 'josoa', 'josue', 'josoua']],
    [70, 'Mpitsara', 'Juges', ['jg', 'mpi', 'mpit', 'mpis', 'juge', 'juges', 'mpitsara']],
    [80, 'Rota', 'Ruth', ['rt', 'rot', 'rota', 'ruth', 'rout']],
    [90, '1 Samoela', '1 Samuel', ['1s', '1sa', '1sam', '1samoela', '1samuel', 'samoela', 'samuel']],
    [100, '2 Samoela', '2 Samuel', ['2s', '2sa', '2sam', '2samoela', '2samuel']],
    [110, '1 Mpanjaka', '1 Rois', ['1r', '1roi', '1rois', '1mp', '1mpa', '1mpanjaka', 'roi', 'rois', 'mpanjaka']],
    [120, '2 Mpanjaka', '2 Rois', ['2r', '2roi', '2rois', '2mp', '2mpa', '2mpanjaka']],
    [130, '1 Tantara', '1 Chroniques', ['1ch', '1chr', '1chronique', '1chroniques', '1ta', '1tan', '1tantara', 'chronique', 'chroniques', 'tantara']],
    [140, '2 Tantara', '2 Chroniques', ['2ch', '2chr', '2chronique', '2chroniques', '2ta', '2tan', '2tantara']],
    [150, 'Ezra', 'Esdras', ['esd', 'ezr', 'ezra', 'esdr', 'esdras']],
    [160, 'Nehemia', 'Nehemie', ['ne', 'neh', 'nehe', 'nehemia', 'nehemie']],
    [190, 'Estera', 'Esther', ['est', 'este', 'estera', 'esther']],
    [220, 'Joba', 'Job', ['jb', 'job', 'joba']],
    [230, 'Salamo', 'Psaumes', ['ps', 'slm', 'sal', 'sala', 'salamo', 'psaume', 'psaumes', 'psau']],
    [240, 'Ohabolana', 'Proverbes', ['pr', 'prov', 'proverbe', 'proverbes', 'oha', 'ohab', 'ohabolana']],
    [250, 'Mpitoriteny', 'Ecclesiaste', ['ec', 'ecc', 'qo', 'eccl', 'ecclesiaste', 'mpt', 'mpitoriteny', 'mpitouriteny']],
    [260, "Tonon-kiran'i Solomona", 'Cantique des Cantiques', ['ct', 'cant', 'ton', 'tono', 'tonon', 'tononkiranisolomona', 'cantiquedescantiques']],
    [290, 'Isaia', 'Esaie', ['is', 'isa', 'isai', 'isaia', 'esaie', 'esai']],
    [300, 'Jeremia', 'Jeremie', ['jr', 'jer', 'jere', 'jeremia', 'jeremie']],
    [310, 'Fitomaniana', 'Lamentations', ['lm', 'lame', 'fit', 'fito', 'fitomaniana', 'lamentation', 'lamentations']],
    [330, 'Ezekiela', 'Ezechiel', ['ez', 'eze', 'ezek', 'ezec', 'ezekiela', 'ezechiel']],
    [340, 'Daniela', 'Daniel', ['dn', 'dan', 'dani', 'daniela', 'daniel']],
    [350, 'Hosea', 'Osee', ['os', 'ose', 'hos', 'hose', 'hosea', 'osee']],
    [360, 'Joela', 'Joel', ['jl', 'joe', 'joel', 'joela']],
    [370, 'Amosa', 'Amos', ['am', 'amo', 'amos', 'amosa']],
    [380, 'Obadia', 'Abdias', ['ab', 'oba', 'obad', 'obadia', 'abdias', 'abdi']],
    [390, 'Jona', 'Jonas', ['jon', 'jona', 'jonas']],
    [400, 'Mika', 'Michee', ['mi', 'mik', 'mika', 'michee', 'mich']],
    [410, 'Nahoma', 'Nahum', ['na', 'nah', 'naho', 'nahoma', 'nahum', 'nahoum']],
    [420, 'Habakoka', 'Habacuc', ['ha', 'hab', 'haba', 'habakoka', 'habacuc', 'habakouka']],
    [430, 'Zefania', 'Sophonie', ['so', 'soph', 'zef', 'zefa', 'zefania', 'sophonie']],
    [440, 'Hagay', 'Aggee', ['ag', 'hag', 'haga', 'hagay', 'aggee', 'agge']],
    [450, 'Zakaria', 'Zacharie', ['za', 'zach', 'zak', 'zaka', 'zakaria', 'zacharie']],
    [460, 'Malakia', 'Malachie', ['ml', 'mal', 'mala', 'malakia', 'malachie', 'malak']],
    [470, 'Matio', 'Matthieu', ['mt', 'matt', 'mat', 'mati', 'matio', 'matthieu', 'matieu']],
    [480, 'Marka', 'Marc', ['mc', 'mar', 'mark', 'marka', 'marc']],
    [490, 'Lioka', 'Luc', ['lc', 'lio', 'liok', 'lioka', 'luc', 'louk']],
    [500, 'Jaona', 'Jean', ['jn', 'jao', 'jaon', 'jaona', 'jean', 'joana', 'joany', 'dzona']],
    [510, "Asan'ny Apostoly", 'Actes', ['ac', 'acte', 'actes', 'asa', 'apos', 'asan', 'asannyapostoly', 'asanapostoly', 'apostoly', 'apotre']],
    [520, 'Romana', 'Romains', ['rm', 'rom', 'roma', 'romana', 'romain', 'romains']],
    [530, '1 Korintiana', '1 Corinthiens', ['1co', '1cor', '1corinthiens', '1corintiens', '1kor', '1korintiana', 'korintiana', 'corinthiens', 'corintiens']],
    [540, '2 Korintiana', '2 Corinthiens', ['2co', '2cor', '2corinthiens', '2corintiens', '2kor', '2korintiana']],
    [550, 'Galatiana', 'Galates', ['ga', 'gal', 'gala', 'galatiana', 'galate', 'galates']],
    [560, 'Efesiana', 'Ephesiens', ['ep', 'eph', 'efe', 'efes', 'efesiana', 'ephesien', 'ephesiens']],
    [570, 'Filipiana', 'Philippiens', ['ph', 'philippien', 'philippiens', 'philipien', 'fil', 'fili', 'filipiana']],
    [580, 'Kolosiana', 'Colossiens', ['col', 'colo', 'kol', 'kolo', 'kolosiana', 'colossien', 'colossiens']],
    [590, '1 Tesaloniana', '1 Thessaloniciens', ['1th', '1the', '1thess', '1thessaloniciens', '1te', '1tes', '1tesaloniana', 'thess', 'thessaloniciens', 'tesaloniana']],
    [600, '2 Tesaloniana', '2 Thessaloniciens', ['2th', '2the', '2thess', '2thessaloniciens', '2te', '2tes', '2tesaloniana']],
    [610, '1 Timoty', '1 Timothee', ['1tm', '1tim', '1timothee', '1ti', '1timoty', 'timo', 'timote', 'timothy', 'timothee', 'timoty']],
    [620, '2 Timoty', '2 Timothee', ['2tm', '2tim', '2timothee', '2ti', '2timoty']],
    [630, 'Titosy', 'Tite', ['tt', 'tit', 'tito', 'titosy', 'tite', 'titus']],
    [640, 'Filemona', 'Philemon', ['phm', 'flm', 'file', 'filemona', 'philemon', 'philem']],
    [650, 'Hebreo', 'Hebreux', ['he', 'heb', 'hebr', 'hebreo', 'hebreux']],
    [660, 'Jakoba', 'Jacques', ['jc', 'jacq', 'jak', 'jako', 'jakoba', 'jacques']],
    [670, '1 Petera', '1 Pierre', ['1p', '1pe', '1pet', '1pier', '1pierre', '1petera', 'petera', 'pierre']],
    [680, '2 Petera', '2 Pierre', ['2p', '2pe', '2pet', '2pier', '2pierre', '2petera']],
    [690, '1 Jaona', '1 Jean', ['1jn', '1ja', '1jao', '1jaona', '1jean']],
    [700, '2 Jaona', '2 Jean', ['2jn', '2ja', '2jao', '2jaona', '2jean']],
    [710, '3 Jaona', '3 Jean', ['3jn', '3ja', '3jao', '3jaona', '3jean']],
    [720, 'Joda', 'Jude', ['jud', 'jod', 'joda', 'jude']],
    [730, 'Apokalypsy', 'Apocalypse', ['ap', 'apo', 'apok', 'apokalypsy', 'apocalypse', 'apokalipsa']]
  ];

  var NUM_FR = {
    zero: 0, un: 1, une: 1, premier: 1, premiere: 1, deux: 2, second: 2, seconde: 2,
    trois: 3, quatre: 4, cinq: 5, six: 6, sept: 7, huit: 8, neuf: 9, dix: 10,
    onze: 11, douze: 12, treize: 13, quatorze: 14, quinze: 15, seize: 16,
    vingt: 20, trente: 30, quarante: 40, cinquante: 50, soixante: 60,
    cent: 100, cents: 100, mille: 1000
  };
  var NUM_MG = {
    aotra: 0, iray: 1, roa: 2, telo: 3, efatra: 4, dimy: 5, enina: 6, fito: 7,
    valo: 8, sivy: 9, folo: 10, roapolo: 20, telopolo: 30, efapolo: 40,
    dimampolo: 50, enimpolo: 60, fitopolo: 70, valopolo: 80, sivifolo: 90,
    zato: 100, arivo: 1000
  };
  var SONG_KW = { hira: 1, fihirana: 1, chant: 1, chants: 1, chanson: 1, chansons: 1, cantique: 1, cantiques: 1, song: 1, numero: 1, numero_faha: 1, numero: 1, num: 1, no: 1 };
  var STOP = {
    toko: 1, faha: 1, andininy: 1, verset: 1, versets: 1, chapitre: 1, chapitres: 1,
    livre: 1, livres: 1, boky: 1, de: 1, du: 1, des: 1, la: 1, le: 1, les: 1, l: 1,
    un: 1, une: 1, d: 1, i: 1, ny: 1, sy: 1, an: 1, ao: 1, amin: 1, paoly: 1,
    voalohan: 1, faharoan: 1, fahatelon: 1, evanjely: 1, evanjelin: 1, evangile: 1,
    epistola: 1, epistolan: 1, selon: 1, lettre: 1, lettres: 1, aux: 1, au: 1
  };

  function norm(s) {
    return (s || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[''`]/g, ' ')
      .replace(/[^a-z0-9]+/g, ' ')
      .trim();
  }
  function alnum(s) {
    return (s || '').toLowerCase().replace(/[^a-z0-9]/g, '');
  }
  function combineNums(seq) {
    var total = 0, cur = 0;
    for (var i = 0; i < seq.length; i++) {
      var v = seq[i];
      if (v === 1000) { total += (cur || 1) * 1000; cur = 0; }
      else if (v === 100) { cur = (cur || 1) * 100; }
      else if (cur >= 10 && v < 10) { cur += v; total += cur; cur = 0; }
      else if (cur === 0) { cur = v; }
      else { total += cur; cur = v; }
    }
    return total + cur;
  }
  function convertSpoken(tokens) {
    var out = [], seq = [];
    function flush() { if (seq.length) { out.push(String(combineNums(seq))); seq = []; } }
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      var om = /^(\d+)(er|ere|re|eme|e|ieme)$/i.exec(t);
      if (om) { flush(); out.push(om[1]); continue; }
      if (t === 'ambin' && tokens[i + 1] === 'ny' && i >= 1 && i + 2 < tokens.length) {
        var unit = NUM_MG[tokens[i - 1]], tens = NUM_MG[tokens[i + 2]];
        if (unit !== undefined && tens !== undefined) {
          if (seq.length) seq[seq.length - 1] = tens + unit;
          else seq.push(tens + unit);
          i += 2;
          continue;
        }
      }
      if (t === 'et') continue;
      var v = NUM_FR[t] !== undefined ? NUM_FR[t] : (NUM_MG[t] !== undefined ? NUM_MG[t] : null);
      if (v !== null) seq.push(v);
      else { flush(); out.push(t); }
    }
    flush();
    return out;
  }

  function findBook(tokens) {
    var joined = '', offsets = [];
    for (var i = 0; i < tokens.length; i++) { offsets.push(joined.length); joined += tokens[i]; }
    var starts = {};
    for (var s = 0; s < offsets.length; s++) starts[offsets[s]] = true;
    var best = null;
    for (var bi = 0; bi < BOOKS.length; bi++) {
      var b = BOOKS[bi], aliases = b[3];
      for (var ai = 0; ai < aliases.length; ai++) {
        var an = alnum(aliases[ai]);
        if (!an) continue;
        var idx = joined.indexOf(an);
        while (idx >= 0) {
          if (starts[idx]) {
            var st = null, en = null;
            for (var ti = 0; ti < tokens.length; ti++) {
              var ts = offsets[ti], te = ts + tokens[ti].length;
              if (te > idx && ts < idx + an.length) { if (st === null) st = ti; en = ti; }
            }
            if (!best || an.length > best.len) best = { book: b, len: an.length, al: an, st: st, en: en };
            break;
          }
          idx = joined.indexOf(an, idx + 1);
        }
      }
    }
    return best;
  }

  function parse(text) {
    var tokens = norm(text).split(' ').filter(function (w) { return w.length > 0; });
    tokens = convertSpoken(tokens);

    var match = findBook(tokens);
    if (match) {
      var book = match.book;
      var rest = [];
      for (var i = 0; i < tokens.length; i++) {
        if (i < match.st || i > match.en) {
          var t = tokens[i];
          if (STOP[t] || /^[a-z]+$/.test(t)) continue;
          rest.push(t);
        }
      }
      var nums = [];
      for (var j = 0; j < rest.length; j++) {
        if (/^\d+$/.test(rest[j])) nums.push(parseInt(rest[j], 10));
      }
      var ch = nums.length ? nums[0] : 1;
      var vs = nums.length > 1 ? nums[1] : null;
      var cantSong = book[0] === 260 && (match.al === 'cant' || match.al === 'cantique' || match.al === 'cantiques') && ch > 8;
      if (!cantSong) {
        return {
          type: 'bible',
          url: 'baibolyMG_v2.html?name=' + encodeURIComponent(book[1]) + '&ch=' + ch + (vs ? '&vs=' + vs : ''),
          label: book[1] + ' ' + ch + (vs ? ':' + vs : '')
        };
      }
    }

    var nums = [], hasKw = false;
    for (var k = 0; k < tokens.length; k++) {
      var tk = tokens[k];
      if (/^\d+$/.test(tk)) nums.push(parseInt(tk, 10));
      if (SONG_KW[tk]) hasKw = true;
    }
    if ((hasKw || (nums.length === 1 && tokens.length === 1)) && nums.length) {
      var n = nums[nums.length - 1];
      return { type: 'song', url: 'fihirana_advantista.html?num=' + n, label: 'Hira n°' + n };
    }
    return null;
  }

  function ensureUI() {
    if (document.getElementById('vsPanel')) return;
    var css = document.createElement('style');
    css.id = 'vsStyle';
    css.textContent =
      '#vsPanel{position:fixed;left:14px;bottom:14px;z-index:2147483646;width:300px;max-width:calc(100vw - 28px);background:rgba(15,20,35,0.94);border:1px solid rgba(255,255,255,0.16);border-radius:16px;box-shadow:0 16px 48px rgba(0,0,0,0.55);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;color:#fff;padding:12px;display:none;backdrop-filter:blur(14px)}' +
      '#vsPanel.open{display:block}' +
      '#vsHead{display:flex;align-items:center;justify-content:space-between;font-size:13px;font-weight:600;margin-bottom:8px;color:rgba(255,255,255,0.9)}' +
      '#vsStatus{font-size:11px;color:rgba(255,255,255,0.45);margin:6px 0;min-height:14px}' +
      '#vsInput{width:100%;padding:9px 12px;border-radius:10px;border:1px solid rgba(255,255,255,0.14);background:rgba(255,255,255,0.07);color:#fff;font-size:14px;outline:none;box-sizing:border-box}' +
      '#vsInput:focus{border-color:#34d399}' +
      '#vsBtns{display:flex;gap:8px;margin-top:10px;align-items:center}' +
      '#vsOk{flex:1;background:#34d399;color:#052e1f;border:none;border-radius:10px;padding:8px 14px;font-weight:700;font-size:13px;cursor:pointer}' +
      '#vsOk:hover{filter:brightness(1.08)}' +
      '#vsX{background:transparent;border:none;color:rgba(255,255,255,0.5);font-size:16px;cursor:pointer;padding:2px 6px;border-radius:6px}' +
      '#vsX:hover{color:#fff;background:rgba(255,255,255,0.1)}' +
      '#vsHint{font-size:10px;color:rgba(255,255,255,0.28);margin-top:8px;text-align:center}';
    document.head.appendChild(css);

    var panel = document.createElement('div');
    panel.id = 'vsPanel';

    var head = document.createElement('div');
    head.id = 'vsHead';
    head.innerHTML = '🔍 Recherche Baiboly';
    var x = document.createElement('button');
    x.id = 'vsX';
    x.textContent = '✕';
    x.title = 'Fermer (Alt+Maj+V)';
    head.appendChild(x);

    var input = document.createElement('input');
    input.id = 'vsInput';
    input.placeholder = 'Ex : "gen 1 3" ou "Salamo 23:1" ou "Hira 125"…';

    var status = document.createElement('div');
    status.id = 'vsStatus';

    var btns = document.createElement('div');
    btns.id = 'vsBtns';
    var ok = document.createElement('button');
    ok.id = 'vsOk';
    ok.textContent = 'OK';
    btns.appendChild(ok);

    var hint = document.createElement('div');
    hint.id = 'vsHint';
    hint.textContent = 'Nom de livre → Baiboly · Numéro → Fihirana · Alt+Maj+V pour fermer · Entrée pour valider';

    panel.appendChild(head);
    panel.appendChild(input);
    panel.appendChild(status);
    panel.appendChild(btns);
    panel.appendChild(hint);
    document.body.appendChild(panel);

    x.addEventListener('click', close);
    ok.addEventListener('click', validate);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') validate(); });
  }

  function setStatus(msg) {
    var el = document.getElementById('vsStatus');
    if (!el) return;
    el.textContent = msg;
  }

  function open() {
    ensureUI();
    document.getElementById('vsPanel').classList.add('open');
    document.getElementById('vsInput').value = '';
    document.getElementById('vsInput').focus();
    setStatus('');
  }

  function close() {
    var p = document.getElementById('vsPanel');
    if (p) p.classList.remove('open');
  }

  function validate() {
    var input = document.getElementById('vsInput');
    var text = input ? input.value.trim() : '';
    if (!text) { setStatus('Entrez un nom de livre et des numéros (ex : gen 1 3)'); return; }
    var res = parse(text);
    if (!res) {
      setStatus('Non reconnu : "' + text + '" — corrigez puis OK');
      return;
    }
    window.location.href = res.url;
  }

  document.addEventListener('keydown', function (e) {
    if (e.altKey && e.shiftKey && (e.code === 'KeyV' || e.key === 'V' || e.key === 'v')) {
      e.preventDefault();
      var p = document.getElementById('vsPanel');
      if (p && p.classList.contains('open')) close();
      else open();
    }
    if (e.key === 'Escape') {
      var q = document.getElementById('vsPanel');
      if (q && q.classList.contains('open')) close();
    }
  });

  window.voiceSearchOpen = open;
  window.voiceSearchClose = close;
  window.voiceSearchParse = parse;
})();
