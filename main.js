(function(){
var b=document.querySelector('.burger'),m=document.querySelector('nav.menu');
if(b)b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach(function(el){io.observe(el)})}else document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')});
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
