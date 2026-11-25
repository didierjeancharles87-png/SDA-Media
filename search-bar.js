(function(){
  if (window._searchBarLoaded) return;
  window._searchBarLoaded = true;

  var STYLE_ID = 'search-bar-style';
  if (!document.getElementById(STYLE_ID)) {
    var css = document.createElement('style');
    css.id = STYLE_ID;
    css.textContent =
'#searchOverlay{position:fixed;inset:0;z-index:999999;display:none;align-items:flex-start;justify-content:center;padding:60px 16px;background:rgba(0,0,0,0.7);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);animation:searchFadeIn .25s ease}#searchOverlay.open{display:flex}'+
'@keyframes searchFadeIn{from{opacity:0;backdrop-filter:blur(0)}to{opacity:1;backdrop-filter:blur(12px)}}'+
'#searchPanel{width:100%;max-width:620px;max-height:calc(100vh - 120px);background:rgba(15,20,35,0.92);border:1px solid rgba(255,255,255,0.15);border-radius:24px;padding:16px;box-shadow:0 20px 60px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,255,255,0.1);animation:searchSlideIn .3s cubic-bezier(0.34,1.56,0.64,1);display:flex;flex-direction:column;backdrop-filter:blur(28px) saturate(180%);-webkit-backdrop-filter:blur(28px) saturate(180%)}'+
'@keyframes searchSlideIn{from{transform:translateY(-20px)scale(.96);opacity:0}to{transform:translateY(0)scale(1);opacity:1}}'+
'#searchInput{width:100%;padding:14px 18px;border-radius:16px;border:1px solid rgba(255,255,255,0.12);background:rgba(255,255,255,0.06);color:#fff;font-size:17px;font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Helvetica Neue",sans-serif;outline:none;transition:border-color .2s;margin-bottom:12px}'+
'#searchInput:focus{border-color:#0A84FF;background:rgba(10,132,255,0.08)}'+
'#searchInput::placeholder{color:rgba(255,255,255,0.35)}'+
'#searchTabs{display:flex;gap:6px;margin-bottom:10px}'+
'.search-tab{flex:1;padding:8px;border-radius:12px;border:none;background:transparent;color:rgba(255,255,255,0.5);font-size:14px;font-weight:600;font-family:inherit;cursor:pointer;transition:all .2s;text-align:center}'+
'.search-tab.active{background:rgba(10,132,255,0.18);color:#0A84FF}'+
'.search-tab:hover:not(.active){background:rgba(255,255,255,0.06);color:rgba(255,255,255,0.8)}'+
'#searchResults{flex:1;overflow-y:auto;min-height:0;scroll-behavior:smooth}'+
'#searchResults::-webkit-scrollbar{width:4px}'+
'#searchResults::-webkit-scrollbar-track{background:transparent}'+
'#searchResults::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.15);border-radius:4px}'+
'.search-empty{padding:24px;text-align:center;color:rgba(255,255,255,0.3);font-size:14px}'+
'.search-result{display:flex;align-items:flex-start;gap:12px;padding:12px 14px;border-radius:14px;cursor:pointer;transition:background .15s;border:none;background:transparent;color:#fff;width:100%;text-align:left;font-family:inherit}'+
'.search-result:hover,.search-result.highlighted{background:rgba(10,132,255,0.14)}'+
'.search-result-icon{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}'+
'.search-result-icon.song{background:rgba(90,200,250,0.18)}'+
'.search-result-icon.bible{background:rgba(52,199,89,0.18)}'+
'.search-result-body{flex:1;min-width:0}'+
'.search-result-title{font-size:15px;font-weight:600;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'+
'.search-result-snippet{font-size:12px;color:rgba(255,255,255,0.35);margin-top:2px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}'+
'.search-result.high{border-left:3px solid #30D158}'+
'.search-result.mid{border-left:3px solid #FF9F0A}'+
'.search-result.low{border-left:3px solid rgba(255,255,255,0.15)}'+
'#searchHint{text-align:center;font-size:11px;color:rgba(255,255,255,0.2);margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,0.04)}'+
'@media(max-width:480px){#searchOverlay{padding:40px 12px}#searchPanel{border-radius:20px;padding:12px}}';
    document.head.appendChild(css);
  }

  var overlay = null;
  var panel = null;
  var input = null;
  var resultsEl = null;
  var tabsEl = null;
  var activeTab = 'songs';
  var songData = null;
  var highlightIdx = -1;

  function createDOM() {
    if (overlay) return;
    overlay = document.createElement('div');
    overlay.id = 'searchOverlay';
    overlay.addEventListener('mousedown', function(e) {
      if (e.target === overlay) closeSearch();
    });

    panel = document.createElement('div');
    panel.id = 'searchPanel';

    input = document.createElement('input');
    input.id = 'searchInput';
    input.type = 'text';
    input.placeholder = 'Hitady hira na andininy...';
    input.autocomplete = 'off';
    input.autocorrect = 'off';
    input.spellcheck = false;

    tabsEl = document.createElement('div');
    tabsEl.id = 'searchTabs';

    var tabSongs = document.createElement('button');
    tabSongs.className = 'search-tab active';
    tabSongs.dataset.tab = 'songs';
    tabSongs.textContent = '\u266B Fihirana';
    tabsEl.appendChild(tabSongs);

    var tabBible = document.createElement('button');
    tabBible.className = 'search-tab';
    tabBible.dataset.tab = 'bible';
    tabBible.textContent = '\u271E Baiboly';
    tabsEl.appendChild(tabBible);

    resultsEl = document.createElement('div');
    resultsEl.id = 'searchResults';

    var hint = document.createElement('div');
    hint.id = 'searchHint';
    hint.textContent = '\u2191\u2193 navigate  \u23CE select  \u238B close';

    panel.appendChild(input);
    panel.appendChild(tabsEl);
    panel.appendChild(resultsEl);
    panel.appendChild(hint);
    overlay.appendChild(panel);
    document.body.appendChild(overlay);

    input.addEventListener('input', function() {
      highlightIdx = -1;
      doSearch();
    });

    input.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        e.preventDefault();
        closeSearch();
        return;
      }
      if (e.key === 'Enter') {
        e.preventDefault();
        var items = resultsEl.querySelectorAll('.search-result');
        if (highlightIdx >= 0 && highlightIdx < items.length) {
          items[highlightIdx].click();
        } else if (items.length > 0) {
          items[0].click();
        }
        return;
      }
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        var items = resultsEl.querySelectorAll('.search-result');
        if (items.length === 0) return;
        highlightIdx = (highlightIdx + 1) % items.length;
        updateHighlight(items);
        return;
      }
      if (e.key === 'ArrowUp') {
        e.preventDefault();
        var items = resultsEl.querySelectorAll('.search-result');
        if (items.length === 0) return;
        highlightIdx = (highlightIdx - 1 + items.length) % items.length;
        updateHighlight(items);
        return;
      }
    });

    tabsEl.addEventListener('click', function(e) {
      var btn = e.target.closest('.search-tab');
      if (!btn) return;
      tabsEl.querySelectorAll('.search-tab').forEach(function(t) { t.classList.remove('active'); });
      btn.classList.add('active');
      activeTab = btn.dataset.tab;
      highlightIdx = -1;
      input.focus();
      doSearch();
    });
  }

  function updateHighlight(items) {
    items.forEach(function(el, i) {
      el.classList.toggle('highlighted', i === highlightIdx);
    });
    if (highlightIdx >= 0 && highlightIdx < items.length) {
      items[highlightIdx].scrollIntoView({ block: 'nearest' });
    }
  }

  function openSearch(tab) {
    createDOM();
    overlay.classList.add('open');
    input.value = '';
    resultsEl.innerHTML = '<div class="search-empty">Soraty ny teny hita...</div>';
    highlightIdx = -1;
    activeTab = tab === 'bible' ? 'bible' : 'songs';
    var btns = tabsEl.querySelectorAll('.search-tab');
    for (var i = 0; i < btns.length; i++) {
      btns[i].classList.toggle('active', btns[i].dataset.tab === activeTab);
    }
    input.placeholder = activeTab === 'bible' ? 'Hitady andininy Baiboly...' : 'Hitady hira...';
    if (activeTab === 'bible' && window.BibleSearchEngine && !window.BibleSearchEngine.isReady()) {
      resultsEl.innerHTML = '<div class="search-loading">\u23F3 Ampidirina ny Baiboly...</div>';
      var data = window.BIBLE_DATA || window._BIBLE_DATA;
      if (data) {
        setTimeout(function() {
          window.BibleSearchEngine.init(data);
          if (input.value.trim()) doSearch();
        }, 50);
      }
    }
    setTimeout(function() { input.focus(); }, 100);
  }

  function closeSearch() {
    if (overlay) overlay.classList.remove('open');
    highlightIdx = -1;
  }

  function getSongData() {
    if (songData) return songData;
    var d = window.FIHIRANA_DATA;
    if (d) {
      songData = d.hiras ? d.hiras : (Array.isArray(d) ? d : null);
      return songData;
    }
    return null;
  }

  function doSearch() {
    var q = input.value.trim();
    if (!q || q.length < 1) {
      resultsEl.innerHTML = '<div class="search-empty">Soraty ny teny hita...</div>';
      return;
    }

    if (activeTab === 'songs') {
      var data = getSongData();
      if (!data) {
        resultsEl.innerHTML = '<div class="search-empty">Tsy hita ny hira</div>';
        return;
      }
      searchSongs(q, data);
    } else {
      if (!window.BibleSearchEngine) {
        resultsEl.innerHTML = '<div class="search-empty">Tsy misy motera fikarohana Baiboly</div>';
        return;
      }
      if (!window.BibleSearchEngine.isReady()) {
        var bdata = window.BIBLE_DATA || window._BIBLE_DATA;
        if (!bdata) {
          resultsEl.innerHTML = '<div class="search-empty">Tsy misy Baiboly eto. Tsidiho ny pejy Baiboly.</div>';
          return;
        }
        resultsEl.innerHTML = '<div class="search-loading">\u23F3 Ampidirina ny Baiboly...</div>';
        setTimeout(function() {
          window.BibleSearchEngine.init(bdata);
          doSearch();
        }, 50);
        return;
      }
      searchBibleEngine(q);
    }
  }

  function searchSongs(q, data) {
    var lq = q.toLowerCase();
    var results = [];
    for (var i = 0; i < data.length; i++) {
      var s = data[i];
      var num = String(s.numero);
      var titre = (s.titre || '');
      var detaille = (s.detaille || '');
      if (num.startsWith(lq) || titre.toLowerCase().indexOf(lq) !== -1 || detaille.toLowerCase().indexOf(lq) !== -1) {
        results.push(s);
        if (results.length >= 20) break;
      }
    }
    renderSongResults(results, q);
  }

  function renderSongResults(results, q) {
    if (results.length === 0) {
      resultsEl.innerHTML = '<div class="search-empty">Tsy nisy hita tamin\'ny hira</div>';
      return;
    }
    var html = '';
    for (var i = 0; i < results.length; i++) {
      var s = results[i];
      var snippet = '';
      if (s.detaille) {
        var clean = s.detaille.replace(/\r|\n|\t/g, ' ').replace(/\s+/g, ' ').trim();
        var idx = clean.toLowerCase().indexOf(q.toLowerCase());
        if (idx > -1) {
          var start = Math.max(0, idx - 40);
          var end = Math.min(clean.length, idx + 60);
          snippet = (start > 0 ? '...' : '') + clean.substring(start, end) + (end < clean.length ? '...' : '');
        }
      }
      html +=
        '<button class="search-result" data-num="' + s.numero + '" data-type="song">' +
          '<div class="search-result-icon song">\u266B</div>' +
          '<div class="search-result-body">' +
            '<div class="search-result-title">N\u00B0' + s.numero + ' - ' + escHtml(s.titre || '') + '</div>' +
            (snippet ? '<div class="search-result-snippet">' + escHtml(snippet) + '</div>' : '') +
          '</div>' +
        '</button>';
    }
    resultsEl.innerHTML = html;
    var items = resultsEl.querySelectorAll('.search-result');
    for (var k = 0; k < items.length; k++) {
      items[k].addEventListener('click', (function(num) {
        return function() {
          closeSearch();
          window.location.href = 'fihirana_advantista.html?num=' + num;
        };
      })(items[k].dataset.num));
    }
  }

  function searchBibleEngine(q) {
    var result = window.BibleSearchEngine.search(q);
    if (!result) {
      resultsEl.innerHTML = '<div class="search-empty">Tsy nisy hita tamin\'ny Baiboly</div>';
      return;
    }
    if (result.type === 'direct') {
      var bookName = result.book.name || result.book.id;
      renderBibleResults([{
        book: bookName, bookId: result.book.id,
        chapter: result.chapter, verse: result.verse,
        text: result.text, relevance: 1
      }], q);
    } else if (result.type === 'chapter') {
      resultsEl.innerHTML = '<div class="search-empty">Toko ' + result.chapter + ' ao amin\'ny ' + result.book.name + ' - Tsindrio ny boky hisafidianana</div>';
    } else if (result.type === 'books') {
      var html = '';
      for (var i = 0; i < result.books.length; i++) {
        var b = result.books[i];
        html +=
          '<button class="search-result" data-book="' + escHtml(b.name || b.id) + '" data-type="bible-book">' +
            '<div class="search-result-icon bible">\u271E</div>' +
            '<div class="search-result-body">' +
              '<div class="search-result-title">' + escHtml(b.name || b.id) + '</div>' +
            '</div>' +
          '</button>';
      }
      resultsEl.innerHTML = html || '<div class="search-empty">Tsy nisy boky hita</div>';
    } else if (result.type === 'theme') {
      // Theme results - show verses
      if (result.results && result.results.length) {
        renderBibleResults(result.results, q);
      } else {
        resultsEl.innerHTML = '<div class="search-empty">Tsy nisy andininy momba io lohahevitra io</div>';
      }
    } else if (result.type === 'verses') {
      if (result.results && result.results.length) {
        renderBibleResults(result.results, q);
      } else {
        resultsEl.innerHTML = '<div class="search-empty">Tsy nisy hita tamin\'ny Baiboly</div>';
      }
    } else {
      resultsEl.innerHTML = '<div class="search-empty">Tsy nisy hita tamin\'ny Baiboly</div>';
    }
  }

  function renderBibleResults(results, q) {
    var html = '';
    for (var i = 0; i < Math.min(results.length, 30); i++) {
      var r = results[i];
      var bookName = r.book || r.bookId || '?';
      var snippet = r.text;
      var lq = q.toLowerCase();
      var idx = r.text.toLowerCase().indexOf(lq);
      if (idx > -1) {
        var start = Math.max(0, idx - 40);
        var end = Math.min(r.text.length, idx + 60);
        snippet = (start > 0 ? '...' : '') + r.text.substring(start, end) + (end < r.text.length ? '...' : '');
      }
      var relevance = r.relevance || 0;
      var relClass = relevance > 0.7 ? 'high' : (relevance > 0.3 ? 'mid' : 'low');
      html +=
        '<button class="search-result ' + relClass + '" data-book="' + escHtml(bookName) + '" data-ch="' + r.chapter + '" data-vs="' + r.verse + '" data-type="bible">' +
          '<div class="search-result-icon bible">\u271E</div>' +
          '<div class="search-result-body">' +
            '<div class="search-result-title">' + escHtml(bookName) + ' ' + r.chapter + ':' + r.verse + '</div>' +
            '<div class="search-result-snippet">' + escHtml(snippet) + '</div>' +
          '</div>' +
        '</button>';
    }
    resultsEl.innerHTML = html || '<div class="search-empty">Tsy nisy hita tamin\'ny Baiboly</div>';
    var items = resultsEl.querySelectorAll('.search-result');
    for (var k = 0; k < items.length; k++) {
      (function(el) {
        el.addEventListener('click', function() {
          var book = el.dataset.book;
          var ch = el.dataset.ch;
          var vs = el.dataset.vs;
          closeSearch();
          window.location.href = 'baibolyMG_v2.html?name=' + encodeURIComponent(book) + '&ch=' + ch + '&vs=' + vs;
        });
      })(items[k]);
    }
  }

  function escHtml(str) {
    var d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }

  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === 'f' || e.key === 'F')) {
      e.preventDefault();
      if (overlay && overlay.classList.contains('open')) {
        closeSearch();
      } else {
        openSearch('songs');
      }
      return;
    }
    if ((e.ctrlKey || e.metaKey) && (e.key === 'b' || e.key === 'B')) {
      e.preventDefault();
      if (overlay && overlay.classList.contains('open')) {
        if (activeTab !== 'bible') {
          activeTab = 'bible';
          var btns = tabsEl.querySelectorAll('.search-tab');
          for (var i = 0; i < btns.length; i++) {
            btns[i].classList.toggle('active', btns[i].dataset.tab === 'bible');
          }
          input.placeholder = 'Hitady andininy Baiboly...';
          input.value = '';
          resultsEl.innerHTML = '<div class="search-loading">\u23F3 Ampidirina ny Baiboly...</div>';
          highlightIdx = -1;
          if (window.BibleSearchEngine && !window.BibleSearchEngine.isReady()) {
            var bd = window.BIBLE_DATA || window._BIBLE_DATA;
            if (bd) setTimeout(function() { window.BibleSearchEngine.init(bd); }, 50);
          }
          input.focus();
        } else {
          closeSearch();
        }
      } else {
        openSearch('bible');
      }
      return;
    }
    if (e.key === 'Escape' && overlay && overlay.classList.contains('open')) {
      closeSearch();
    }
  });

  window.searchBarOpen = openSearch;
  window.searchBarClose = closeSearch;
})();
