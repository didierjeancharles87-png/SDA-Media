/* ═══ SDA PROJECTOR — Mode Simple + Mode Étendre ═══
 * Bouton flottant "AFFICHER" avec menu de sélection de mode :
 *   • Mode Simple   → projector.html directement sur le 2ème écran
 *   • Mode Étendre  → presenter.html (contrôle) + projector.html (2ème écran)
 * Usage : <script src="projector.js"></script> avant la fermeture du body.
 *
 * Communication: stocke le dernier message dans _lastMsg.
 * projector.html et presenter.html pollent window.opener.SDAProjector.pull()
 * toutes les 800ms pour récupérer le contenu.
 */
(function(){
  var CHANNEL='sda_projector';
  var LS_KEY='sda_projector_ls';
  var MODE_KEY='sda_proj_mode';
  var projectorUrl='projector.html?v=7';
  var presenterUrl='presenter.html?v=7';
  var popup=null;
  var mode=localStorage.getItem(MODE_KEY)||'extend';
  var bc=null;
  try{bc=new BroadcastChannel(CHANNEL)}catch(e){bc=null}

  /* ═══ DERNIER MESSAGE (pull mechanism) ═══ */
  var _lastMsg=null;
  var _lastMsgId=0;

  function send(msg){
    msg=msg||{};msg._t=Date.now();
    var prev=_lastMsg;
    if(prev&&prev.type===msg.type&&prev.payload&&msg.payload){
      var a=prev.payload,b=msg.payload;
      if(a.title===b.title&&a.body===b.body&&a.html===b.html&&a.subtitle===b.subtitle&&a.bg===b.bg&&a.contentType===b.contentType&&a.split===b.split){
        msg._id=prev._id;
      }else{
        msg._id=++_lastMsgId;
      }
    }else{
      msg._id=++_lastMsgId;
    }
    _lastMsg=msg;
    try{localStorage.setItem(LS_KEY,JSON.stringify(msg))}catch(e){}
    if(popup&&!popup.closed){
      try{popup.postMessage({type:'sda_proj',data:msg},'*')}catch(e){}
      try{if(typeof popup.renderProjector==='function')popup.renderProjector(msg)}catch(e){}
    }
  }

  function openPopup(url,title){
    if(popup&&!popup.closed){popup.focus();return popup}
    var w=Math.round(screen.width*(url===presenterUrl?0.55:0.6));
    var h=Math.round(screen.height*(url===presenterUrl?0.85:0.8));
    var left=url===presenterUrl?0:screen.width-w;
    var top=0;
    try{
      popup=window.open(url,title,'width='+w+',height='+h+',left='+left+',top='+top+',menubar=no,toolbar=no,location=no,status=no');
    }catch(e){popup=null}
    if(!popup) popup=window.open(url,'_blank');
    updateBtn();
    setTimeout(function(){try{capture()}catch(e){}},500);
    return popup;
  }

  window.SDAProjector={
    send:send,
    open:function(){
      var url=mode==='extend'?presenterUrl:projectorUrl;
      return openPopup(url,'sda_projector');
    },
    openSimple:function(){
      mode='simple';localStorage.setItem(MODE_KEY,'simple');
      return openPopup(projectorUrl,'sda_projector');
    },
    openExtend:function(){
      mode='extend';localStorage.setItem(MODE_KEY,'extend');
      return openPopup(presenterUrl,'sda_projector');
    },
    setMode:function(m){
      mode=m;localStorage.setItem(MODE_KEY,m);
    },
    getMode:function(){return mode},
    show:function(opts){
      opts=opts||{};
      send({type:'content',payload:{
        title:opts.title||'',
        subtitle:opts.subtitle||'',
        body:opts.body||'',
        html:opts.html||'',
        split:!!opts.split,
        bg:opts.bg||'',
        signature:opts.signature,
        contentType:opts.contentType||''
      }});
    },
    clear:function(){send({type:'clear'})},
    showSlide:function(html){
      send({type:'content',payload:{type:'slide',html:html||''}});
    },
    capture:capture,
    isOpen:function(){return popup&&!popup.closed},
    get:function(){return null},
    pull:function(){
      if(_lastMsg) return _lastMsg;
      return null;
    },
    toggle:function(){
      if(window.SDAProjector.isOpen()){
        if(popup)popup.close();popup=null;
      }else{
        window.SDAProjector.open();
      }
      updateBtn();
    }
  };

  // ── Capture générique du contenu visible ──
  function textOf(el){ if(!el)return ''; return (el.innerText||el.textContent||'').replace(/\s+/g,' ').trim(); }
  var _clearTimer=null;
  var _lastContentType='';
  function capture(){
    if(!window.SDAProjector.isOpen())return;
    function vis(el){ if(!el)return false; if(el.offsetParent!==null)return true; var r=el.getBoundingClientRect(); return r.width>0&&r.height>0; }

    if(_clearTimer){clearTimeout(_clearTimer);_clearTimer=null}

    var active=document.querySelector('.slideshow.open .slide.active')||document.querySelector('.slideshow.open .slide.active');
    if(active){
      var clone=active.cloneNode(true);
      clone.classList.remove('exit');
      clone.classList.remove('enter-fade','enter-zoomIn','enter-zoomOut','enter-slideLeft','enter-slideRight','enter-blur','enter-rotate','enter-flip');
      clone.style.position='absolute';clone.style.opacity='1';
      window.SDAProjector.showSlide(clone.outerHTML);
      _lastContentType='slide';
      return;
    }
    if(document.querySelector('.slideshow.open'))return;

    var vt=document.querySelector('.verse-text-view');
    if(vis(vt)){
      var ref=textOf(vt.querySelector('.verse-ref'))||textOf(document.querySelector('.chapter-reader-title'));
      var body=textOf(vt.querySelector('.verse-text'))||textOf(vt.querySelector('.verse-display'));
      window.SDAProjector.show({title:ref,body:body,split:true,contentType:'verse'});
      _lastContentType='verse';
      return;
    }
    var cr=document.querySelector('.chapter-reader');
    if(vis(cr)){
      var title=textOf(cr.querySelector('.chapter-reader-title'));
      var verses=cr.querySelectorAll('.chapter-reader-verse');
      var txt='';
      verses.forEach(function(v){ txt+=v.innerText.trim()+'\n\n'; });
      window.SDAProjector.show({title:title,body:txt.trim(),split:true,contentType:'chapter'});
      _lastContentType='chapter';
      return;
    }

    var fv=document.querySelector('.slide-view')||document.querySelector('.slide-body');
    if(vis(fv)){
      var fref=textOf(document.querySelector('.slide-ref'))||textOf(document.querySelector('.slide-header'));
      var fbody='';
      var couplets=document.querySelectorAll('.slide-couplet-text');
      if(couplets.length){
        couplets.forEach(function(c){ fbody+=(c.innerText||'').trim()+'\n\n'; });
      } else {
        fbody=textOf(fv);
      }
      var hbg='';
      var activeCouplet=document.querySelector('.slide-couplet.has-img .slide-img');
      if(activeCouplet&&activeCouplet.src){hbg=activeCouplet.src}
      window.SDAProjector.show({title:fref,body:fbody.trim(),split:true,contentType:'hymn',bg:hbg});
      _lastContentType='hymn';
      return;
    }

    var sabGlass=document.querySelector('.glass-card');
    if(sabGlass&&vis(sabGlass)){
      var sabPayload={split:false,contentType:'program'};
      if(sabGlass.classList.contains('is-cover')){
        sabPayload.title=textOf(sabGlass.querySelector('.cover-title'))||'';
        sabPayload.subtitle=textOf(sabGlass.querySelector('.cover-sub'))||'';
        sabPayload.body='';
      }else if(sabGlass.classList.contains('is-section')){
        sabPayload.title=textOf(sabGlass.querySelector('.cover-title'))||'';
        sabPayload.subtitle=textOf(sabGlass.querySelector('.cover-sub'))||'';
        sabPayload.body='';
      }else if(sabGlass.classList.contains('is-end')){
        sabPayload.title=textOf(sabGlass.querySelector('.cover-title'))||'';
        sabPayload.subtitle=textOf(sabGlass.querySelector('.cover-sub'))||'';
        sabPayload.body='';
      }else{
        var sabLabel=textOf(sabGlass.querySelector('.eyebrow'))||'';
        var sabHeadline=textOf(sabGlass.querySelector('.headline'))||'';
        sabPayload.title=sabLabel;
        sabPayload.body=sabHeadline;
        sabPayload.split=true;
      }
      window.SDAProjector.show(sabPayload);
      _lastContentType='program';
      return;
    }

    var card=document.querySelector('.card-expanded');
    if(vis(card)){
      window.SDAProjector.show({title:textOf(card.querySelector('h1,h2,h3,.card-title')),body:textOf(card.querySelector('.text')),split:true,contentType:'card'});
      _lastContentType='card';
      return;
    }

    var items=document.querySelector('.items');
    if(vis(items)){
      var rows=items.querySelectorAll('.item-row');
      var out='';
      rows.forEach(function(r){
        var t=textOf(r.querySelector('.item-type'));
        var x=textOf(r.querySelector('.item-input'))||textOf(r);
        out+=(t?('\u3010 '+t+' \u3011\n'):'')+x.trim()+'\n\n';
      });
      window.SDAProjector.show({title:'FILAZANA',body:out.trim(),split:true,contentType:'announcement'});
      _lastContentType='announcement';
      return;
    }

    var ov=document.querySelector('.overlay');
    if(vis(ov)){
      var mq=document.querySelector('.marquee-wrap');
      window.SDAProjector.show({title:'',body:mq?mq.innerText.trim():'',split:false,contentType:'marquee'});
      _lastContentType='marquee';
      return;
    }

    if(_lastContentType){
      _clearTimer=setTimeout(function(){
        window.SDAProjector.clear();
        _lastContentType='';
        _clearTimer=null;
      },2000);
    }
  }

  // ── Menu de mode ──
  var menuEl=null;
  function showModeMenu(e){
    e&&e.preventDefault&&e.preventDefault();
    hideModeMenu();
    menuEl=document.createElement('div');
    menuEl.id='sdaProjMenu';
    menuEl.innerHTML=
      '<div class="spm-title">MODE PROJECTION</div>'+
      '<div class="spm-item'+(mode==='simple'?' active':'')+'" data-m="simple">'+
        '<span class="spm-icon">\uD83D\uDCFA</span><div><b>Mode Simple</b><span>Projecteur seul sur le 2\u00E8me \u00E9cran</span></div>'+
      '</div>'+
      '<div class="spm-item'+(mode==='extend'?' active':'')+'" data-m="extend">'+
        '<span class="spm-icon">\uD83D\uDCFD</span><div><b>Mode \u00C9tendre</b><span>Contr\u00F4le + Projecteur (2 \u00E9crans)</span></div>'+
      '</div>';
    document.body.appendChild(menuEl);

    var s=document.createElement('style');
    s.id='sdaProjMenuCss';
    s.textContent=
      '#sdaProjMenu{position:fixed;z-index:100000;right:14px;bottom:74px;'+
      'min-width:260px;background:rgba(12,18,36,.92);border:1px solid rgba(255,255,255,.14);'+
      'border-radius:16px;backdrop-filter:blur(32px) saturate(180%);-webkit-backdrop-filter:blur(32px) saturate(180%);'+
      'box-shadow:0 20px 60px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.05) inset;'+
      'padding:8px;animation:spmIn .25s cubic-bezier(.34,1.56,.64,1)}'+
      '@keyframes spmIn{from{opacity:0;transform:translateY(12px) scale(.95)}to{opacity:1;transform:none}}'+
      '#sdaProjMenu .spm-title{font-size:9px;font-weight:800;letter-spacing:2px;text-transform:uppercase;'+
      'color:rgba(255,255,255,.3);padding:8px 12px 6px}'+
      '#sdaProjMenu .spm-item{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:12px;'+
      'cursor:pointer;transition:all .2s;border:1px solid transparent}'+
      '#sdaProjMenu .spm-item:hover{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.1)}'+
      '#sdaProjMenu .spm-item.active{background:rgba(10,132,255,.15);border-color:rgba(10,132,255,.3)}'+
      '#sdaProjMenu .spm-icon{font-size:22px;width:36px;height:36px;display:flex;align-items:center;'+
      'justify-content:center;border-radius:10px;background:rgba(255,255,255,.06);flex-shrink:0}'+
      '#sdaProjMenu .spm-item div{display:flex;flex-direction:column;gap:1px}'+
      '#sdaProjMenu .spm-item b{font-size:13px;font-weight:700;color:rgba(255,255,255,.92)}'+
      '#sdaProjMenu .spm-item span{font-size:10px;color:rgba(255,255,255,.4);letter-spacing:.3px}'+
      '@media(max-width:500px){#sdaProjMenu{right:10px;bottom:64px;min-width:220px}}';
    document.head.appendChild(s);

    var items=menuEl.querySelectorAll('.spm-item');
    for(var i=0;i<items.length;i++){
      items[i].addEventListener('click',function(){
        var m=this.getAttribute('data-m');
        mode=m;localStorage.setItem(MODE_KEY,m);
        hideModeMenu();
        if(window.SDAProjector.isOpen()){
          if(popup)popup.close();popup=null;
        }
        window.SDAProjector.open();
        updateBtn();
      });
    }
    setTimeout(function(){document.addEventListener('click',hideModeMenuOnClick)},10);
  }
  function hideModeMenu(){
    if(menuEl){menuEl.remove();menuEl=null}
    var css=document.getElementById('sdaProjMenuCss');if(css)css.remove();
    document.removeEventListener('click',hideModeMenuOnClick);
  }
  function hideModeMenuOnClick(e){
    if(menuEl&&!menuEl.contains(e.target)){
      var btn=document.getElementById('sdaProjBtn');
      if(btn&&btn.contains(e.target))return;
      hideModeMenu();
    }
  }

  function updateBtn(){
    var b=document.getElementById('sdaProjBtn');
    if(!b)return;
    if(window.SDAProjector.isOpen()){
      b.classList.add('active');
      b.innerHTML='&#x2716; FERMER';
      b.title='Projecteur actif \u2014 Cliquer pour arr\u00EAt\u00E9r';
    }else{
      b.classList.remove('active');
      b.innerHTML='&#x1F4FD; ';
      b.title='. sur le projecteur \u2014 Mode '+mode;
    }
  }

  function buildBtn(){
    if(document.getElementById('sdaProjBtn'))return;
    var b=document.createElement('button');
    b.id='sdaProjBtn';
    b.innerHTML='&#x1F4FD; ';
    b.title=' sur le projecteur \u2014 Cliquer pour ouvrir \u00B7 Clic droit: choisir le mode';
    b.addEventListener('click',function(e){
      if(menuEl){hideModeMenu();return}
      if(e.shiftKey||e.ctrlKey||e.metaKey){
        showModeMenu(e);return;
      }
      window.SDAProjector.toggle();
    });
    b.addEventListener('contextmenu',function(e){e.preventDefault();showModeMenu(e)});
    document.body.appendChild(b);
    var s=document.createElement('style');
    s.textContent=
      '#sdaProjBtn{position:fixed;z-index:99999;right:14px;bottom:14px;'+
      'height:48px;padding:0 20px;border-radius:999px;'+
      'border:1px solid rgba(255,255,255,.22);cursor:pointer;font-size:14px;font-weight:700;'+
      'letter-spacing:1.5px;'+
      'background:linear-gradient(135deg,rgba(10,132,255,.65),rgba(90,200,250,.45));'+
      'color:#fff;backdrop-filter:blur(20px) saturate(180%);'+
      '-webkit-backdrop-filter:blur(20px) saturate(180%);'+
      'box-shadow:0 6px 28px rgba(10,132,255,.45),inset 0 1px 0 rgba(255,255,255,.25);'+
      'transition:transform .25s cubic-bezier(.34,1.56,.64,1),background .3s,box-shadow .3s;'+
      'display:flex;align-items:center;justify-content:center;gap:8px;line-height:1;'+
      'text-transform:uppercase;white-space:nowrap;}'+
      '#sdaProjBtn:hover{transform:scale(1.06);background:linear-gradient(135deg,rgba(10,132,255,.85),rgba(90,200,250,.65));'+
      'box-shadow:0 12px 40px rgba(10,132,255,.55),inset 0 1px 0 rgba(255,255,255,.3);}'+
      '#sdaProjBtn:active{transform:scale(.94)}'+
      '#sdaProjBtn.active{background:linear-gradient(135deg,rgba(52,199,89,.7),rgba(48,209,88,.5));'+
      'border-color:rgba(52,199,89,.6);'+
      'box-shadow:0 0 32px rgba(52,199,89,.5),inset 0 1px 0 rgba(255,255,255,.2);}'+
      '@media(max-width:500px){#sdaProjBtn{height:42px;padding:0 14px;font-size:12px;right:10px;bottom:10px;}}';
    document.head.appendChild(s);
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',buildBtn);
  } else { buildBtn(); }

  setInterval(function(){ if(popup&&popup.closed){popup=null;updateBtn();} },1000);
  setInterval(function(){ try{capture()}catch(e){} },500);

  /* ── Hook sabata_hariva navigation ── */
  function hookSabataHariva(){
    var orig=window.__sabataGoTo;
    if(typeof orig==='function'&&!orig._hooked){
      window.__sabataGoTo=function(i){orig.call(null,i);setTimeout(function(){try{capture()}catch(e){}},420)};
      window.__sabataGoTo._hooked=true;
    }
    var origNext=window.__sabataNext;
    if(typeof origNext==='function'&&!origNext._hooked){
      window.__sabataNext=function(){origNext.call(null);setTimeout(function(){try{capture()}catch(e){}},420)};
      window.__sabataNext._hooked=true;
    }
  }
  hookSabataHariva();
  setInterval(hookSabataHariva,2000);
})();
