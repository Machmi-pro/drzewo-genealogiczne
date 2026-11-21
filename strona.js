(function(){
  // Menu hamburger: wysuwana szuflada z kaflami
  var bg=document.getElementById('burger'),dr=document.getElementById('drawer'),sc=document.getElementById('scrim');
  function menu(open){dr.hidden=!open;sc.hidden=!open;bg.setAttribute('aria-expanded',open);document.body.style.overflow=open?'hidden':'';if(open)dr.querySelector('a,button').focus();else bg.focus();}
  if(bg){bg.addEventListener('click',function(){menu(dr.hidden);});
    document.getElementById('dclose').addEventListener('click',function(){menu(false);});
    sc.addEventListener('click',function(){menu(false);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!dr.hidden)menu(false);});}

  // Tytuł w nagłówku: dopasuj szerokość do linii z nazwiskami pod spodem
  var bt=document.querySelector('.brand .bt'),bs=document.querySelector('.brand small');
  function fit(){if(!bt||!bs)return;bt.style.fontSize='20px';var w=bt.getBoundingClientRect().width,t=bs.getBoundingClientRect().width;if(w>0&&t>0)bt.style.fontSize=(20*t/w).toFixed(2)+'px';}
  fit();window.addEventListener('resize',fit);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);

  // Powiększanie zdjęć i skanów
  var d=document.getElementById('lightbox');
  if(d){
    document.querySelectorAll('button.zoom').forEach(function(b){
      b.addEventListener('click',function(){
        var img=b.querySelector('img'),box=document.getElementById('lb-img');
        if(img){box.innerHTML='';box.className='foto';var c=img.cloneNode();c.removeAttribute('loading');c.removeAttribute('class');box.appendChild(c);}
        else{box.className='ph';box.innerHTML=b.querySelector('.ph').innerHTML;}
        document.getElementById('lb-cap').textContent=b.dataset.cap||'';
        document.getElementById('lb-src').textContent=b.dataset.src||'';
        if(d.showModal)d.showModal();
      });
    });
    document.getElementById('lb-close').addEventListener('click',function(){d.close();});
    d.addEventListener('click',function(e){if(e.target===d)d.close();});
  }
  document.querySelectorAll('a.todo').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();});});
})();
