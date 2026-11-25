(function(){
if (window.BibleSearchEngineReady) return;

// ---- Malagasy NLP ----
var MG_PREFIXES=['ampaha','ampan','ampar','ampal','ampam','anampan','ihafahana','ifaharana','ifahazana','hanaovan','hamelan','hampiasa','hanalan','hanaiky','hiady','hiasa','hihaino','hiavy','hifidy','hihira','manaovan','mamelan','mampiasa','manalan','manaiky','mifanka','mifan','miray','miara','mifamp','mamp','mana','mami','mamo','man','mam','mia','mif','mih','mik','mil','min','mir','mis','mit','miv','mi','ma','mp','mpi','fana','fam','fah','fan','fif','fim','fin','fir','fis','fit','fiv','fa','fi','fe','ana','am','an','tsy','pa','ha','ho'];
var MG_SUFFIXES=['areo','nay','nao','ko','azy','iny','izy','any','aho','ana','ina','ony','eny','andy','amby','ny','na','ka','ra','za'];
var MG_STEMS={'mifankatia':'katia','mifankatiana':'katia','fifankatiavana':'katia','fifankatiana':'katia','tia':'tia','tiako':'tia','tianao':'tia','tiany':'tia','tiana':'tia','tian':'tia','mino':'no','minoa':'no','finoana':'no','tsy mino':'no','mivavaka':'vavaka','vavaka':'vavaka','mivavak':'vavaka','mamonjy':'vonjy','famonjiana':'vonjy','voavonjy':'vonjy','mamonjia':'vonjy','mifaly':'faly','fifaliana':'faly','mifalifaly':'faly','mahery':'hery','heriny':'hery','herin':'hery','mahasoa':'soa','fahasoan':'soa','soa':'soa','mahatonga':'tonga','tonga':'tonga','hatongavan':'tonga','mahafoy':'foy','mifoy':'foy','mitsangana':'tsangana','fitsanganana':'tsangana','nitsangana':'tsangana','maty':'maty','fahafatesana':'maty','mahafaty':'maty','manana':'ana','manankarena':'karena','mpanankarena':'karena','mampianatra':'natra','mianatra':'natra','fanabeazana':'natra','miteny':'teny','tenin':'teny','teny':'teny','mitory':'tory','fitoriana':'tory','mitoria':'tory','miandry':'andry','mpiandry':'andry','mangataka':'gataka','angatahy':'gataka','manetry':'netry','fanetrentena':'netry','mifona':'fona','mamela':'ela','famelan':'ela','mahafaly':'faly','hafalian':'faly','hafali':'faly','faly':'faly','mahatanteraka':'tanteraka','tanteraka':'tanteraka','fahatanterahan':'tanteraka','mankalaza':'kalaza','fankalazana':'kalaza','mankalaza':'kalaza','mifidy':'fidy','fifidianana':'fidy','voafidy':'fidy','mpifidy':'fidy','manompo':'tompo','fanompoana':'tompo','mpanompo':'tompo','mijaly':'fijaly','fahoriana':'fijaly','fijaliana':'fijaly','mihaino':'heno','heno':'heno','henoy':'heno','mandre':'heno','reny':'reny','rainy':'ray','ray':'ray','zanaka':'zanaka','zanako':'zanaka','zanany':'zanaka','mpianatra':'natra','mianatra':'natra','mpampianatra':'natra','miandry':'andry','miambina':'andry','mpiandry':'andry','mitandrina':'tandrina','tandremo':'tandrina','harato':'harato','mpanjato':'harato','miara':'miara','miaraka':'miara','iraisan':'iray','iray':'iray','miray':'iray','mampisy':'misy','misy':'misy','nisy':'misy','hisy':'misy','velona':'velona','velom':'velona','mandrakizay':'mandrakizay','mandrakizay':'mandrakizay'};

function normalize(str){
  return (str||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[''`]/g,"'").replace(/[^a-z0-9\s'-]/g,' ').replace(/\s+/g,' ').trim();
}

function lemmatize(word){
  var w=word.toLowerCase().trim();
  if(MG_STEMS[w]) return MG_STEMS[w];
  var stem=w;
  for(var p=0;p<MG_PREFIXES.length;p++){
    if(stem.indexOf(MG_PREFIXES[p])===0){
      stem=stem.slice(MG_PREFIXES[p].length);
      break;
    }
  }
  for(var s=0;s<MG_SUFFIXES.length;s++){
    if(stem.length>3&&stem.slice(-MG_SUFFIXES[s].length)===MG_SUFFIXES[s]){
      stem=stem.slice(0,-MG_SUFFIXES[s].length);
      break;
    }
  }
  return stem||w;
}

function tokenize(str){
  return normalize(str).split(' ').filter(function(w){return w.length>=3;});
}

function tokenizeLemma(str){
  return tokenize(str).map(lemmatize);
}

// ---- Fuzzy & Spell ----
function levenshtein(a,b){
  var la=a.length,lb=b.length;
  if(Math.abs(la-lb)>3) return 99;
  if(la===0) return lb; if(lb===0) return la;
  var prev=[],curr=[];
  for(var i=0;i<=lb;i++) prev[i]=i;
  for(var i=1;i<=la;i++){
    curr[0]=i;
    for(var j=1;j<=lb;j++){
      var cost=a[i-1]===b[j-1]?0:1;
      curr[j]=Math.min(prev[j]+1,curr[j-1]+1,prev[j-1]+cost);
    }
    var tmp=prev;prev=curr;curr=tmp;
  }
  return prev[lb];
}

var _spellCache=new Map();
function spellCorrect(word,dictionary){
  if(dictionary.has(word)) return word;
  if(_spellCache.has(word)) return _spellCache.get(word);
  var candidates=[];
  for(var w of dictionary){
    if(Math.abs(w.length-word.length)<=2) candidates.push(w);
  }
  var best=word,bestDist=3;
  for(var i=0;i<candidates.length;i++){
    var d=levenshtein(word,candidates[i]);
    if(d<bestDist){ bestDist=d; best=candidates[i]; }
  }
  if(_spellCache.size>500) _spellCache.clear();
  _spellCache.set(word,best);
  return best;
}

// ---- Theme Search ----
var THEMES={
  'fitiavana':{label:'Fitiavana',keys:['fitiavana','tia','tiako','tianao','tia-namana']},
  'fanantenana':{label:'Fanantenana',keys:['fanantenana','manantena','tohana','antenaina']},
  'vavaka':{label:'Vavaka',keys:['vavaka','mivavaka','mangataka','angatahy','mifona']},
  'famonjiana':{label:'Famonjiana',keys:['famonjiana','voavonjy','mamonjy','vonjy','fanavotana']},
  'fandriampahalemana':{label:'Fiadanana',keys:['fandriampahalemana','fiadanana','miadana','mampiadana']},
  'fahendrena':{label:'Fahendrena',keys:['fahendrena','hendry','zoto','mahay']},
  'finoana':{label:'Finoana',keys:['finoana','mino','minoa','tsy mino']},
  'herim-po':{label:'Herim-po',keys:['herim-po','herina','sahy','mahery','aza matahotra']},
  'famelan-keloka':{label:'Famelan-keloka',keys:['famelan-keloka','mamela','melan-keloka','meloka']},
  'fahafatesana':{label:'Fahafatesana',keys:['fahafatesana','maty','faty','mahafaty']},
  'fitsanganana':{label:'Fitsanganana',keys:['fitsanganana','nitsangana','tsangana','velona','mitsangana']},
  'jesosy':{label:'Jesosy Kristy',keys:['jesosy','kristy','zanaka','andriamanitra','tompo','mpamonjy']},
  'fanahy masina':{label:'Fanahy Masina',keys:['fanahy masina','fanahy','masina','hery']},
  'sabata':{label:'Sabata',keys:['sabata','alakamisy','andro fahafito','andro fitsaharana']},
  'fahatongavan':{label:'Fahatongavany',keys:['fahatongavany','ho avy','andro']},
  'fitsarana':{label:'Fitsarana',keys:['fitsarana','tsara','mitsara','anjaran']},
  'batisa':{label:'Batisa',keys:['batisa','atao batisa','batisan','rano']},
  'fiangonana':{label:'Fiangonana',keys:['fiangonana','fivavahana','mpiandry','mpitandrina']},
  'fitoriana':{label:'Fitoriana',keys:['mitoria','mitory','vaovao mahafaly','mpitory']},
  'fianakaviana':{label:'Fianakaviana',keys:['ray','reny','zanaka','fianakaviana','vady','mpivady']},
  'asa':{label:'Asa',keys:['asa','miasa','mpiasa','tanana']},
  'fahavalo':{label:'Fahavalo',keys:['fahavalo','tia fahavalo','mamela fahavalo']},
  'fahamarinana':{label:'Fahamarinana',keys:['fahamarinana','marina','mahitsy','mahafoy','mino']},
  'fifaliana':{label:'Fifaliana',keys:['fifaliana','mifaly','hafaliananareo']},
  'fitiavanana':{label:'Fifankatiavana',keys:['mifankatia','mifanampy','mifanohana','fifankatiavana']},
  'fanetren-tena':{label:'Fanetren-tena',keys:['fanetren-tena','manetry','tsy mirehareha','malemy fanahy']},
  'faminaniana':{label:'Faminaniana',keys:['mpaminany','faminaniana','teny nampilazain','maminany']}
};

function searchByTheme(key,searchIndex){
  var theme=THEMES[key]; if(!theme) return [];
  var results=[];
  for(var i=0;i<searchIndex.length;i++){
    var entry=searchIndex[i];
    var tn=normalize(entry.text);
    var hits=0;
    for(var k=0;k<theme.keys.length;k++){
      if(tn.indexOf(theme.keys[k])!==-1) hits++;
    }
    if(hits>0) results.push({book:entry.book,bookId:entry.bookId,chapter:entry.chapter,verse:entry.verse,text:entry.text,score:hits,relevance:Math.min(1,hits/3)});
    if(results.length>=40) break;
  }
  results.sort(function(a,b){return b.score-a.score;});
  return results.slice(0,20);
}

// ---- Character Search ----
var CHARACTERS={
  'mosesy':{name:'Mosesy',keys:['mosesy','mose']},
  'abrahama':{name:'Abrahama',keys:['abrahama','abrama','abram']},
  'davida':{name:'Davida',keys:['davida','mpanjaka davida']},
  'solomona':{name:'Solomona',keys:['solomona']},
  'elija':{name:'Elija',keys:['elija','elia']},
  'isaia':{name:'Isaia',keys:['isaia']},
  'jeremia':{name:'Jeremia',keys:['jeremia']},
  'daniera':{name:'Daniera',keys:['daniera','daniyely']},
  'petera':{name:'Petera',keys:['petera','simona petera','kefa']},
  'paoly':{name:'Paoly',keys:['paoly','saoly']},
  'jaona':{name:'Jaona',keys:['jaona','mpianatra tia azy']},
  'maria':{name:'Maria',keys:['maria','renin\'i jesosy']},
  'josefa':{name:'Josefa',keys:['josefa']},
  'jakoba':{name:'Jakoba',keys:['jakoba','isiraely']},
  'noe':{name:'Noe',keys:['noe','tavin-drano','sambo-fiara']},
  'joba':{name:'Joba',keys:['joba','joba be']},
  'rota':{name:'Rota',keys:['rota']},
  'estera':{name:'Estera',keys:['estera']},
  'laza':{name:'Lazaro',keys:['lazaro','laza']}
};

function searchCharacter(q){
  var qn=normalize(q);
  for(var id in CHARACTERS){
    var char=CHARACTERS[id];
    for(var k=0;k<char.keys.length;k++){
      if(qn.indexOf(normalize(char.keys[k]))!==-1) return char;
    }
  }
  return null;
}

function getCharacterVerses(char,searchIndex){
  var results=[];
  for(var i=0;i<searchIndex.length;i++){
    var entry=searchIndex[i];
    var tn=normalize(entry.text);
    for(var k=0;k<char.keys.length;k++){
      if(tn.indexOf(normalize(char.keys[k]))!==-1){
        results.push({book:entry.book,bookId:entry.bookId,chapter:entry.chapter,verse:entry.verse,text:entry.text,score:1,relevance:0.8});
        if(results.length>=30) break;
      }
    }
    if(results.length>=30) break;
  }
  return results;
}

// ---- Abbreviations ----
var BOOK_ABBR={
  gen:'genesisy',eks:'eksodosy',lev:'levitikosy',nom:'nomery',deo:'deoteronomia',
  jos:'josoa',mpi:'mpitsara',rot:'rota','1sam':'1samoela','2sam':'2samoela',
  '1mpa':'1mpanjaka','2mpa':'2mpanjaka','1tan':'1tantara','2tan':'2tantara',
  ezr:'ezra',neh:'nehemia',est:'estera',job:'joba',sal:'salamo',oha:'ohabolana',
  mpt:'mpitoriteny',ton:'tononkira',isa:'isaia',jer:'jeremia',fit:'fitomaniana',
  eze:'ezekiela',dan:'daniela',hos:'hosea',joe:'joela',amo:'amosa',oba:'obadia',
  jon:'jona',mik:'mika',nah:'nahoma',hab:'habakoka',zef:'zefania',hag:'hagay',
  zak:'zakaria',mal:'malakia',mat:'matio',mar:'marka',lio:'lioka',jao:'jaona',
  asa:'asannyapostoly',rom:'romanina','1kor':'1korintianina','2kor':'2korintianina',
  gal:'galatianina',efe:'efesianina',fil:'filipianina',kol:'kolosianina',
  '1tes':'1tesalonianina','2tes':'2tesalonianina','1tim':'1timoty','2tim':'2timoty',
  tit:'titosy',flm:'filemona',heb:'hebreo',jak:'jakoba','1pet':'1petera','2pet':'2petera',
  '1jao':'1jaona','2jao':'2jaona','3jao':'3jaona',jod:'joda',apo:'apokalypsy'
};

var BOOK_ABBR_KEYS=Object.keys(BOOK_ABBR).sort(function(a,b){return b.length-a.length;});

// ---- Semantic Expansion ----
var SEMANTIC_MAP={
  'fitiavana':['tia','tiako','tianao','fifankatiavana','tian\'andriamanitra'],
  'fampahery':['mampahery','herim-po','fanantenana','mahery','antenaina'],
  'fivavahana':['vavaka','mivavaka','mangataka','tompo'],
  'famonjena':['mamonjy','voavonjy','famonjiana','mpamonjy'],
  'finoana':['mino','minoa','toky','mahatoky','fanantenana'],
  'fiadanana':['fandriampahalemana','fitsaharana','filaminana','milamina'],
  'fifaliana':['mifaly','hafaliampo','hafaliavana'],
  'sabata':['asabotsy','fitahiana','fitsaharana','masina'],
  'fahatongavana':['fahatongavan','tonga indray','maranata'],
  'batisa':['atao batisa','batisana','nisy batisa'],
  'famindram-po':['mamindra fo','mamela','mamela heloka','famelan-keloka'],
  'fahafatesana':['maty','mahafaty','fanahy','fanangana'],
  'fitsanganana':['nitsangana','mitsangana','tsy maty','velona'],
  'fanahy masina':['fanahy','fanahin\'andriamanitra'],
  'lalana':['didy','baiko','sitrapo','torolalana','lalan\'andriamanitra'],
  'fanantenana':['manantena','antenaina','tohana'],
  'herim-po':['mahery','sahy','hery','mampahery'],
  'fahasoavana':['soa','fahasoavana','tsara fanahy'],
  'fiainana':['velona','mandrakizay','fiainana mandrakizay','rano velona'],
  'fahafahana':['afaka','manafaka','fanafahana'],
  'fitsaharana':['mitsahatra','sabata','fialan-tsasatra'],
  'fanompoana':['manompo','mpanompo','fanompoana'],
  'fahadiovana':['madio','diovina','fahadiovana'],
  'fahari-tom-po':['mahari-po','fahari-tom-po','mijaly','manam-paharetana'],
  'fampihavanana':['mampihavana','mifankahavana','fampihavanana'],
  'fahatokiana':['matoky','atoky','mahatoky','fahatokiana'],
  'fahamarinana':['marina','mahitsy','fahamarinana','fitsarana'],
  'fankalazana':['mankalaza','fankalazana','dera','fiderana','hobio']
};

var TESTAMENT_BOOST={
  'matio':1.05,'marko':1.05,'lioka':1.05,'jaona':1.1,'asan':1.0,
  'romana':1.05,'1korintianina':1.05,'2korintianina':1.05,
  'efesianina':1.05,'filipianina':1.05,'kolosianina':1.05,
  'hebreo':1.05,'jakoba':1.05,'apokalypsy':1.0,
  'genesisy':1.03,'salamo':1.08,'ohabolana':1.06,'isaia':1.06
};

function semanticExpand(tokens){
  var expanded=[];
  var seen={};
  for(var i=0;i<tokens.length;i++){
    var tok=tokens[i];
    if(!seen[tok]){ seen[tok]=true; expanded.push(tok); }
    for(var key in SEMANTIC_MAP){
      var syns=SEMANTIC_MAP[key];
      if(tok===key){
        for(var s=0;s<syns.length;s++){
          if(!seen[syns[s]]){ seen[syns[s]]=true; expanded.push(syns[s]); }
        }
      }else{
        for(var s=0;s<syns.length;s++){
          if(tok===syns[s]&&!seen[key]){ seen[key]=true; expanded.push(key); break; }
        }
      }
    }
  }
  return expanded;
}

// ---- Parse Verse Reference ----
function parseVerseRef(q,allBooks){
  var qn=normalize(q);
  function ordToNum(s){
    var m=s.match(/faha[\s-]?(\d+)/i);
    return m?parseInt(m[1]):null;
  }
  var abbrPattern='^('+BOOK_ABBR_KEYS.map(function(k){return k.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}).join('|')+')(?![a-z])\\s*[:.,\\s]?(\\d+)?[:.,\\s]?(\\d*)?';
  var abbrRegex=new RegExp(abbrPattern,'i');
  var am=qn.match(abbrRegex);
  if(am){
    var ab=am[1].toLowerCase();
    var bi=BOOK_ABBR[ab];
    var bo=null;
    for(var i=0;i<allBooks.length;i++){
      if(allBooks[i].id===bi||allBooks[i].name.toLowerCase()===bi){ bo=allBooks[i]; break; }
    }
    if(bo){
      var c=am[2]?parseInt(am[2]):null;
      var v=am[3]?parseInt(am[3]):null;
      if(c){
        if(v){
          var t=bo.chapters[String(c)]?.[String(v)];
          if(t) return{type:'direct',book:bo,chapter:c,verse:v,text:t};
        }
        return{type:'chapter',book:bo,chapter:c};
      }
    }
  }
  for(var i=0;i<allBooks.length;i++){
    var book=allBooks[i];
    var bn=normalize(book.name),bi=normalize(book.id);
    if(qn.indexOf(bn)===-1&&qn.indexOf(bi)===-1) continue;
    var rest=qn.replace(bn,'').replace(bi,'').trim();
    var ch=null,v=null;
    var f1=rest.match(/(\d+)\s*[:.,,]\s*(\d+)/);
    if(f1){ ch=parseInt(f1[1]); v=parseInt(f1[2]); }
    if(!ch){ var f2=rest.match(/toko\s+(?:faha[\s-]?)?(\d+)\s+andininy\s+(?:faha[\s-]?)?(\d+)/i);
      if(f2){ ch=parseInt(f2[1]); v=parseInt(f2[2]); }
    }
    if(!ch){ var f3ch=rest.match(/toko\s+(faha[\s-]?\d+)/i); var f3v=rest.match(/andininy\s+(faha[\s-]?\d+)/i);
      if(f3ch) ch=ordToNum(f3ch[1]); if(f3v) v=ordToNum(f3v[1]);
    }
    if(!ch){ var f4=rest.match(/toko\s+(?:faha[\s-]?)?(\d+)/i); if(f4) ch=parseInt(f4[1]); }
    if(!ch){ var f5=rest.match(/(\d+)\s+(\d+)/); if(f5){ ch=parseInt(f5[1]); v=parseInt(f5[2]); }}
    if(!ch){ var f6=rest.match(/(\d+)/); if(f6) ch=parseInt(f6[1]); }
    if(!ch) continue;
    if(!book.chapters[String(ch)]) continue;
    if(v){
      var text=book.chapters[String(ch)]?.[String(v)];
      if(text) return{type:'direct',book:book,chapter:ch,verse:v,text:text};
    }
    return{type:'chapter',book:book,chapter:ch};
  }
  return null;
}

// ---- TF-IDF Scoring ----
function tfidfScore(queryWords,docVec){
  var score=0;
  for(var i=0;i<queryWords.length;i++){
    score+=docVec.get(queryWords[i])||0;
  }
  return score;
}

function hybridScore(entry,queryTokens,queryLemmas,docVec,verseLemmasEntry){
  var tn=normalize(entry.text);
  var tfidf=tfidfScore(queryLemmas,docVec);
  var exact=0;
  for(var i=0;i<queryTokens.length;i++){
    if(tn.indexOf(queryTokens[i])!==-1) exact+=0.3;
  }
  var lemma=0;
  for(var i=0;i<queryLemmas.length;i++){
    if(verseLemmasEntry.indexOf(queryLemmas[i])!==-1) lemma+=0.2;
  }
  var allPresent=queryTokens.every(function(w){return tn.indexOf(w)!==-1;});
  var boost=allPresent?0.5:0;
  return tfidf+exact+lemma+boost;
}

// ---- Fuzzy Score ----
function fuzzyScore(text,query){
  var tn=normalize(text),qn=normalize(query);
  if(tn.indexOf(qn)!==-1) return 1.0;
  var qWords=qn.split(' ').filter(function(w){return w.length>2;});
  if(!qWords.length) return 0;
  var matched=0;
  for(var i=0;i<qWords.length;i++){ if(tn.indexOf(qWords[i])!==-1) matched++; }
  var ratio=matched/qWords.length;
  var lastIdx=-1,ordered=0;
  for(var i=0;i<qWords.length;i++){
    var idx=tn.indexOf(qWords[i],lastIdx+1);
    if(idx>lastIdx){ ordered++; lastIdx=idx; }
  }
  return ratio+(qWords.length>1?ordered/qWords.length*0.2:0);
}

// ---- Main Engine ----
var engineState={
  searchIndex:null,
  allBooks:null,
  verseLemmas:null,
  tfidfIndex:null,
  invertedIndex:null,
  initialized:false
};

function initEngine(data){
  if(engineState.initialized) return true;
  var searchIndex=[];
  var allBooks=[];

  // SQLite dump format
  if(data.objects){
    var objects=data.objects||[];
    var books=null,verses=null;
    for(var i=0;i<objects.length;i++){
      var obj=objects[i];
      if(obj.name==='books'&&obj.rows) books=obj.rows;
      if(obj.name==='verses'&&obj.rows) verses=obj.rows;
    }
    if(books&&verses){
      var bookMap={};
      for(var i=0;i<books.length;i++){
        var r=books[i];
        if(r.length>=3){
          bookMap[r[1]]={short:r[2],long:r[3]||r[2]};
          allBooks.push({id:String(r[1]),name:r[2],chapters:{}});
        }
      }
      // Group verses by book/chapter for parseVerseRef compatibility
      for(var i=0;i<verses.length;i++){
        var v=verses[i];
        var bNum=v[0],ch=v[1],vs=v[2],txt=v[3];
        var bk=allBooks.find(function(b){return b.id===String(bNum);});
        if(!bk) continue;
        if(!bk.chapters[String(ch)]) bk.chapters[String(ch)]={};
        bk.chapters[String(ch)][String(vs)]=txt;
        searchIndex.push({book:bk.name,bookId:String(bNum),chapter:ch,verse:vs,text:txt});
      }
    }
  }

  // Nested testament format (baibolyMG_v2.html inline)
  if(data.testamenta_taloha||data.testamenta_vaovao){
    var testaments=(data.testamenta_taloha||[]).concat(data.testamenta_vaovao||[]);
    for(var t=0;t<testaments.length;t++){
      var book=testaments[t];
      var bookId=book.id||String(t+1);
      allBooks.push({id:bookId,name:book.name,chapters:book.chapters||{}});
      var chapters=book.chapters||{};
      var chKeys=Object.keys(chapters);
      for(var c=0;c<chKeys.length;c++){
        var chNum=parseInt(chKeys[c],10);
        var ch=chapters[chKeys[c]]||{};
        var vsKeys=Object.keys(ch);
        for(var v=0;v<vsKeys.length;v++){
          var vsNum=parseInt(vsKeys[v],10);
          searchIndex.push({book:book.name,bookId:bookId,chapter:chNum,verse:vsNum,text:ch[vsKeys[v]]});
        }
      }
    }
  }

  if(!searchIndex.length) return false;

  // Build indices
  var verseLemmas=searchIndex.map(function(entry){return tokenizeLemma(entry.text);});

  var N=searchIndex.length;
  var df=new Map();
  var wordDict=new Set();
  for(var i=0;i<verseLemmas.length;i++){
    var unique={};
    for(var j=0;j<verseLemmas[i].length;j++){
      var w=verseLemmas[i][j];
      if(!unique[w]){ unique[w]=true; df.set(w,(df.get(w)||0)+1); wordDict.add(w); }
    }
  }

  var docVectors=[];
  for(var i=0;i<verseLemmas.length;i++){
    var lemmas=verseLemmas[i];
    var freq=new Map();
    for(var j=0;j<lemmas.length;j++){
      freq.set(lemmas[j],(freq.get(lemmas[j])||0)+1);
    }
    var vec=new Map();
    for(var entry of freq){
      var w=entry[0],f=entry[1];
      var tf=f/lemmas.length;
      var idf=Math.log(N/(1+(df.get(w)||0)));
      vec.set(w,tf*idf);
    }
    docVectors.push(vec);
  }

  var invertedIndex={};
  for(var i=0;i<verseLemmas.length;i++){
    var seen={};
    for(var j=0;j<verseLemmas[i].length;j++){
      var l=verseLemmas[i][j];
      if(!seen[l]){ seen[l]=true; if(!invertedIndex[l]) invertedIndex[l]=[]; invertedIndex[l].push(i); }
    }
  }

  engineState.searchIndex=searchIndex;
  engineState.allBooks=allBooks;
  engineState.verseLemmas=verseLemmas;
  engineState.tfidfIndex={docVectors:docVectors,df:df,wordDict:wordDict,N:N};
  engineState.invertedIndex=invertedIndex;
  engineState.initialized=true;
  return true;
}

function searchBible(query,data){
  // Auto-init on first use
  if(!engineState.initialized){
    if(!data) data=window.BIBLE_DATA||window._BIBLE_DATA;
    if(!data) return null;
    if(!initEngine(data)) return null;
  }

  var q=normalize(query);
  if(!q) return null;

  var searchIndex=engineState.searchIndex;
  var allBooks=engineState.allBooks;
  var verseLemmas=engineState.verseLemmas;
  var tfidfIndex=engineState.tfidfIndex;
  var invertedIndex=engineState.invertedIndex;

  // 1. Try verse reference parsing
  var ref=parseVerseRef(query,allBooks);
  if(ref) return ref;

  // 2. Exact phrase search (quoted)
  var exactMatch=query.match(/"([^"]+)"/);
  if(exactMatch){
    var phrase=normalize(exactMatch[1]);
    var exactResults=[];
    for(var i=0;i<searchIndex.length;i++){
      var tn=normalize(searchIndex[i].text);
      if(tn.indexOf(phrase)!==-1){
        exactResults.push({book:searchIndex[i].book,bookId:searchIndex[i].bookId,chapter:searchIndex[i].chapter,verse:searchIndex[i].verse,text:searchIndex[i].text,relevance:1.0,matchType:'exact'});
      }
    }
    if(exactResults.length) return{type:'verses',results:exactResults.slice(0,30),exact:true};
  }

  // 3. Theme exact match
  for(var key in THEMES){
    if(q===key||q===normalize(THEMES[key].label)){
      var themeResults=searchByTheme(key,searchIndex);
      return{type:'theme',key:key,results:themeResults};
    }
  }

  // 4. Book exact match
  var bookExact=[];
  for(var i=0;i<allBooks.length;i++){
    if(normalize(allBooks[i].name)===q||normalize(allBooks[i].id)===q) bookExact.push(allBooks[i]);
  }
  if(bookExact.length>0) return{type:'books',books:bookExact};

  // 5. Book partial match (short queries)
  if(query.trim().length<=14){
    var bookPartial=[];
    for(var i=0;i<allBooks.length;i++){
      if(normalize(allBooks[i].name).indexOf(q)!==-1||normalize(allBooks[i].id).indexOf(q)!==-1){
        bookPartial.push(allBooks[i]);
      }
    }
    if(bookPartial.length>0) return{type:'books',books:bookPartial.slice(0,10)};
  }

  // 6. Fuzzy fallback for short queries
  var words=q.split(' ').filter(Boolean);
  var fuzzyResults=[];
  if(words.length<=3){
    for(var i=0;i<searchIndex.length;i++){
      var tn=normalize(searchIndex[i].text);
      var totalScore=0;
      for(var w=0;w<words.length;w++){
        if(words[w].length<3){ if(tn.indexOf(words[w])!==-1) totalScore+=1; continue; }
        if(tn.indexOf(words[w])!==-1){ totalScore+=1; continue; }
        // Character-level fuzzy match
        for(var ci=0;ci<=tn.length-words[w].length;ci++){
          var sub=tn.slice(ci,ci+words[w].length);
          var dist=0;
          for(var cj=0;cj<words[w].length;cj++) if(sub[cj]!==words[w][cj]) dist++;
          if(dist<=1){ totalScore+=0.8; break; }
        }
      }
      if(totalScore>0){
        fuzzyResults.push({book:searchIndex[i].book,bookId:searchIndex[i].bookId,chapter:searchIndex[i].chapter,verse:searchIndex[i].verse,text:searchIndex[i].text,relevance:Math.min(1,totalScore/words.length),matchType:'fuzzy'});
        if(fuzzyResults.length>=20) break;
      }
    }
  }

  // 7. TF-IDF hybrid search
  var rawTokens=tokenize(query);
  var wordDictArr=[];
  for(var w of tfidfIndex.wordDict) wordDictArr.push(w);
  var correctedTokens=rawTokens.map(function(w){return spellCorrect(w,tfidfIndex.wordDict);});
  var lemmaTokens=correctedTokens.map(lemmatize);
  var expandedTokens=semanticExpand(lemmaTokens);

  var scored=[];
  if(expandedTokens.length>0){
    var candidateSet=new Set();
    for(var i=0;i<expandedTokens.length;i++){
      var tok=expandedTokens[i];
      if(invertedIndex[tok]){
        for(var j=0;j<invertedIndex[tok].length;j++) candidateSet.add(invertedIndex[tok][j]);
      }
    }
    var candidates=candidateSet.size>0?Array.from(candidateSet):null;
    var iter=candidates||searchIndex.map(function(_,i){return i;});
    for(var ii=0;ii<iter.length;ii++){
      var i=iter[ii];
      var entry=searchIndex[i];
      var docVec=tfidfIndex.docVectors[i];
      var score=hybridScore(entry,correctedTokens,expandedTokens,docVec,verseLemmas[i]);
      for(var w=0;w<lemmaTokens.length;w++){
        if(normalize(entry.text).indexOf(lemmaTokens[w])!==-1) score+=0.15;
      }
      var bookBoost=TESTAMENT_BOOST[entry.bookId]||1.0;
      score*=bookBoost;
      if(score>0.01) scored.push({book:entry.book,bookId:entry.bookId,chapter:entry.chapter,verse:entry.verse,text:entry.text,score:score});
    }
  }

  // Merge results
  if(scored.length>0){
    scored.sort(function(a,b){return b.score-a.score;});
    var top=scored[0].score;
    var merged=scored.map(function(e){
      return{book:e.book,bookId:e.bookId,chapter:e.chapter,verse:e.verse,text:e.text,relevance:Math.min(1,e.score/top),matchType:'tfidf'};
    });
    return{type:'verses',results:merged.slice(0,60),fuzzy:true};
  }

  if(fuzzyResults.length>0){
    return{type:'verses',results:fuzzyResults,fuzzy:true};
  }

  // Last resort: individual word match
  var fallback=[];
  for(var i=0;i<searchIndex.length;i++){
    var tn=normalize(searchIndex[i].text);
    if(words.some(function(w){return w.length>3&&tn.indexOf(w)!==-1;})){
      fallback.push({book:searchIndex[i].book,bookId:searchIndex[i].bookId,chapter:searchIndex[i].chapter,verse:searchIndex[i].verse,text:searchIndex[i].text,relevance:0.3});
      if(fallback.length>=30) break;
    }
  }
  if(fallback.length) return{type:'verses',results:fallback,fuzzy:true};

  return{type:'verses',results:[]};
}

window.BibleSearchEngine={
  init:initEngine,
  search:function(query,data){ return searchBible(query,data); },
  isReady:function(){ return engineState.initialized; },
  normalize:normalize,
  lemmatize:lemmatize,
  tokenize:tokenize,
  getSearchIndex:function(){ return engineState.searchIndex; },
  getAllBooks:function(){ return engineState.allBooks; },
  searchByTheme:function(key){ return searchByTheme(key,engineState.searchIndex); },
  searchCharacter:searchCharacter,
  THEMES:THEMES,
  CHARACTERS:CHARACTERS
};

window.BibleSearchEngineReady=true;
})();
