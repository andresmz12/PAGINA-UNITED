(function(){
var b=document.querySelector('.burger'),m=document.querySelector('nav.menu');
if(b)b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach(function(el){io.observe(el)})}else document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')});
var sl=document.querySelector('.slider');
if(sl){var ss=[].slice.call(sl.querySelectorAll('.slide')),ds=[].slice.call(sl.querySelectorAll('.dots button')),i=0,t,hov=false,red=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function go(n){i=(n+ss.length)%ss.length;ss.forEach(function(s,k){s.classList.toggle('on',k===i);s.setAttribute('aria-hidden',k!==i)});ds.forEach(function(d,k){d.setAttribute('aria-current',k===i)})}
function auto(){clearInterval(t);if(!red)t=setInterval(function(){if(!hov)go(i+1)},6500)}
sl.querySelector('.prev').onclick=function(){go(i-1);auto()};sl.querySelector('.next').onclick=function(){go(i+1);auto()};
ds.forEach(function(d,k){d.onclick=function(){go(k);auto()}});
sl.addEventListener('mouseenter',function(){hov=true});sl.addEventListener('mouseleave',function(){hov=false});
sl.addEventListener('focusin',function(){hov=true});sl.addEventListener('focusout',function(){hov=false});
sl.addEventListener('keydown',function(e){if(e.key==='ArrowLeft'){go(i-1);auto()}if(e.key==='ArrowRight'){go(i+1);auto()}});
go(0);auto()}
var sp=new URLSearchParams(location.search).get('service');
if(sp){document.querySelectorAll('select[name="Service Needed"] option').forEach(function(o){if(o.dataset.slug===sp)o.selected=true})}
var v=document.querySelector('video');if(v){v.muted=true;var p=v.play();if(p&&p.catch)p.catch(function(){})}
var f=document.querySelector('form.q');
if(f)f.addEventListener('submit',function(e){e.preventDefault();
if(f.querySelector('.hp input').value)return;
var btn=f.querySelector('button'),err=f.querySelector('.err'),lbl=btn.textContent;
btn.disabled=true;btn.textContent=f.dataset.sending;err.hidden=true;
fetch('https://formsubmit.co/ajax/Info@unitedcleaning.us',{method:'POST',headers:{Accept:'application/json'},body:new FormData(f)})
.then(function(r){if(!r.ok)throw 0;f.hidden=true;document.querySelector('.ok').hidden=false;document.querySelector('.ok').scrollIntoView({behavior:'smooth',block:'center'})})
.catch(function(){btn.disabled=false;btn.textContent=lbl;err.hidden=false})});
})();
