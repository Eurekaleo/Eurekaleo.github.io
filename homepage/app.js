document.documentElement.classList.replace('no-js','js');
const menu=document.querySelector('.menu-toggle');
const nav=document.querySelector('#primary-nav');
function closeMenu(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open navigation');}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';nav.classList.toggle('open',open);menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close navigation':'Open navigation');});
nav.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu();});
document.addEventListener('click',event=>{if(!event.target.closest('.masthead'))closeMenu();});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&nav.classList.contains('open')){closeMenu();menu.focus();}});
matchMedia('(min-width:761px)').addEventListener('change',event=>{if(event.matches)closeMenu();});

const dialog=document.querySelector('#figure-dialog');
let trigger;
document.querySelectorAll('[data-figure]').forEach(link=>link.addEventListener('click',event=>{
  if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||typeof dialog.showModal!=='function')return;
  event.preventDefault();trigger=link;
  const image=document.querySelector('#expanded-figure');image.src=link.href;image.alt=link.dataset.title;
  document.querySelector('#figure-caption').textContent=link.dataset.title;
  document.querySelector('#original-figure').href=link.href;
  dialog.showModal();document.querySelector('#close-figure').focus();
}));
document.querySelector('#close-figure').addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>trigger?.focus({preventScroll:true}));
dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();});

function revealHash(){
  let target;try{target=document.getElementById(decodeURIComponent(location.hash.slice(1)));}catch{return;}
  if(!target)return;
  const details=target.closest('details');
  if(details&&!details.open){details.open=true;requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));}
}
window.addEventListener('hashchange',revealHash);revealHash();
const sections=[...document.querySelectorAll('main>section[id]')];
let pending=false;
function updateNavigation(){
  let current=sections[0].id;
  for(const section of sections){if(section.getBoundingClientRect().top<=140)current=section.id;}
  if(window.scrollY+window.innerHeight>=document.documentElement.scrollHeight-3)current=sections.at(-1).id;
  nav.querySelectorAll('a').forEach(link=>{if(link.hash==='#'+current)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});
  pending=false;
}
window.addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(updateNavigation);}},{passive:true});
window.addEventListener('resize',updateNavigation);
updateNavigation();
