#!/usr/bin/env python3
"""Generates the static site. Edit site.config.json / content.py, then run: python3 tools/build.py"""
import os, json, sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sys.path.insert(0,HERE)
from content import SERVICES
C=json.load(open(os.path.join(HERE,'site.config.json')))
BASE=C['domain']; PH=C['phone_display']; TEL=C['phone_tel']; EM=C['email']; WA=C['whatsapp']
K=C['colors']
open(f'{ROOT}/theme.css','w').write(f":root{{--navy:{K['navy']};--navy2:{K['navy2']};--ink:#1d2836;--muted:#5d6a78;--line:#e1e6ec;--bg:#f4f7fa;--teal:{K['teal']};--teal-d:{K['teal_dark']};--accent:{K['accent']};--accent-d:{K['accent_dark']};--cyan:{K['cyan']};--green:{K['green']};--blue:{K['blue']};--r:14px}}\n")

import hashlib
def _v(f): return hashlib.md5(open(os.path.join(ROOT,f),'rb').read()).hexdigest()[:8]
VER={f:_v(f) for f in ('styles.css','main.js')}
def write(path,html):
    d=os.path.join(ROOT,path.strip('/'));os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w').write(html)

# ---- URL helpers
def u(lang,kind,sv=None):
    if lang=='en':
        return {'home':'/','services':'/services/','about':'/about/','contact':'/contact/','sv':f'/services/{sv["en"]}/' if sv else ''}[kind]
    return {'home':'/es/','services':'/es/servicios/','about':'/es/nosotros/','contact':'/es/contacto/','sv':f'/es/servicios/{sv["es"]}/' if sv else ''}[kind]
def L(lang,i): return i[0] if lang=='en' else i[1]

T={'en':dict(home='Home',services='Services',about='About',contact='Contact',quote='Get a Free Quote',foot='Commercial and residential cleaning across Missouri, Kansas & Southern Illinois.',co='COMPANY',ct='CONTACT',avail='Available 24/7',area=C['areas_en'],rights='© 2026 United Cleaning Services. All rights reserved.',call='Call',q_s='Free Quote',other='ES',olabel='Español',svc='SERVICES',wa='Chat on WhatsApp'),
   'es':dict(home='Inicio',services='Servicios',about='Nosotros',contact='Contacto',quote='Cotización Gratis',foot='Limpieza comercial y residencial en Missouri, Kansas y el sur de Illinois.',co='EMPRESA',ct='CONTACTO',avail='Disponible 24/7',area=C['areas_es'],rights='© 2026 United Cleaning Services. Todos los derechos reservados.',call='Llamar',q_s='Cotizar',other='EN',olabel='English',svc='SERVICIOS',wa='Escríbanos por WhatsApp')}

def ic(n):
    p={'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>','shield':'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>','star':'<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>'}[n]
    return f'<svg class="i" viewBox="0 0 24 24" aria-hidden="true">{p}</svg>'

WA_SVG='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.900-.2-.3A8.200 8.200 0 1112 20.200zm4.500-6.100c-.2-.1-1.500-.7-1.700-.8s-.4-.1-.6.100-.6.800-.8 1-.3.200-.6.100a6.700 6.700 0 01-3.300-2.900c-.2-.4.200-.4.700-1.300.1-.2 0-.3 0-.5l-.8-1.800c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.300 3 3 0 00-.9 2.200c0 1.300.9 2.600 1 2.800.1.200 1.800 2.800 4.400 3.900 1.600.7 2.300.7 3.100.6.500-.1 1.500-.6 1.700-1.200s.2-1.100.2-1.200-.2-.2-.5-.3z"/></svg>'

THEMEV=hashlib.md5(open(f'{ROOT}/theme.css','rb').read()).hexdigest()[:8]
FLAGS={
'es':'<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#c60b1e"/><rect y="5" width="30" height="10" fill="#ffc400"/></svg>',
'en':'<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#fff"/>'+''.join(f'<rect y="{y*20/7.0:.2f}" width="30" height="{20/13.0:.2f}" fill="#b22234"/>' for y in [0,1.9,3.8,5.7,7.6,9.5,11.4] if False)+''.join(f'<rect y="{k*20/13:.2f}" width="30" height="{20/13:.2f}" fill="#b22234"/>' for k in range(0,13,2))+'<rect width="13" height="10.77" fill="#3c3b6e"/></svg>'}
def page(lang,path,alt,title,desc,body,ld_extra='',ogimg='/assets/office-team.jpg'):
    t=T[lang]; url=BASE+path
    sv_links=''.join(f'<li><a href="{u(lang,"sv",s)}">{L(lang,s["n"])}</a></li>' for s in SERVICES)
    def cls(p): return ' class="on"' if (path==p or (p not in('/','/es/') and path.startswith(p))) else ''
    nav=(f'<a href="{u(lang,"home")}"{cls(u(lang,"home"))}>{t["home"]}</a>'
         f'<div class="dd"><a href="{u(lang,"services")}"{cls(u(lang,"services"))}>{t["services"]}</a><ul class="ddm">{sv_links}</ul></div>'
         f'<a href="{u(lang,"about")}"{cls(u(lang,"about"))}>{t["about"]}</a><a href="{u(lang,"contact")}"{cls(u(lang,"contact"))}>{t["contact"]}</a>')
    flat=''.join(f'<a href="{h}">{n}</a>' for h,n in [(u(lang,'home'),t['home']),(u(lang,'services'),t['services']),(u(lang,'about'),t['about']),(u(lang,'contact'),t['contact'])])
    en_p,es_p=(path,alt) if lang=='en' else (alt,path)
    hl=f'<link rel="alternate" hreflang="en" href="{BASE}{en_p}"><link rel="alternate" hreflang="es" href="{BASE}{es_p}"><link rel="alternate" hreflang="x-default" href="{BASE}{en_p}">'
    ld=json.dumps({"@context":"https://schema.org","@type":"CleaningService","name":C['name'],"image":BASE+"/assets/logo.jpg","url":BASE+"/","telephone":TEL,"email":EM,"areaServed":["Missouri","Kansas","Southern Illinois"],"openingHours":"Mo-Su 00:00-24:00","priceRange":"$$"})
    q=u(lang,'contact'); home=u(lang,'home')
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">{hl}
<link rel="icon" type="image/png" href="/assets/favicon.png"><meta name="theme-color" content="{K['navy']}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{C['name']}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}{ogimg}"><meta property="og:locale" content="{'en_US' if lang=='en' else 'es_US'}"><meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/theme.css?v={THEMEV}"><link rel="stylesheet" href="/styles.css?v={VER["styles.css"]}">
<script type="application/ld+json">{ld}</script>{ld_extra}
</head>
<body>
<header class="top"><div class="wrap nav">
<a class="brand" href="{home}"><img src="/assets/logo.jpg" alt="{C['name']} logo" width="44" height="44"><span>UNITED<small>CLEANING SERVICES</small></span></a>
<nav class="menu" id="menu" aria-label="Main">{nav}<a class="lang" href="{alt}" hreflang="{'es' if lang=='en' else 'en'}" title="{t['olabel']}" aria-label="{t['olabel']}">{FLAGS['es' if lang=='en' else 'en']}</a></nav>
<div class="nav-cta"><a class="tel" href="tel:{TEL}">{PH}</a><a class="btn btn-g" href="{q}">{t['quote']}</a><button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button></div>
</div></header>
<main>{body}</main>
<footer class="f"><div class="wrap">
<div class="fg">
<div><a class="brand" href="{home}"><img src="/assets/logo.jpg" alt="" width="40" height="40"><span>UNITED<small>CLEANING SERVICES</small></span></a><p>{t['foot']}</p></div>
<div><h4>{t['co']}</h4>{flat}</div>
<div><h4>{t['svc']}</h4>{''.join(f'<a href="{u(lang,"sv",s)}">{L(lang,s["n"])}</a>' for s in SERVICES)}</div>
<div><h4>{t['ct']}</h4><a href="tel:{TEL}">{PH}</a><a href="mailto:{EM}">{EM}</a><span>{t['avail']}</span><span>{t['area']}</span></div>
</div>
<div class="fb"><span>{t['rights']}</span><a href="{alt}" style="color:#7f93a8;display:flex;align-items:center;gap:8px"><span class="flag">{FLAGS['es' if lang=='en' else 'en']}</span>{t['olabel']}</a></div>
</div></footer>
<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="{t['wa']}">{WA_SVG}</a>
<div class="mbar"><a class="c" href="tel:{TEL}">{t['call']}</a><a class="q" href="{q}">{t['q_s']}</a></div>
<script src="/main.js?v={VER["main.js"]}" defer></script>
</body></html>'''

# ---- shared blocks
def tx(en,es,lang): return en if lang=='en' else es
def steps(lang):
    S=[('Tell us about your space','Share your property type, size, and schedule through our quick form or a phone call.','Cuéntenos sobre su espacio','Comparta el tipo de propiedad, tamaño y horario por formulario o llamada.'),
       ('Get your free quote','Within one business day you receive a customized plan and a clear price.','Reciba su cotización gratis','En un día hábil recibe un plan y precio claros.'),
       ('We clean, you relax','A trained, vetted crew arrives on schedule and cleans to a consistent standard.','Nosotros limpiamos','Un equipo capacitado y verificado llega puntual y limpia con un estándar consistente.'),
       ('Guaranteed results',"Not satisfied? We come back and make it right.",'Resultados garantizados','¿No está satisfecho? Regresamos y lo corregimos.')]
    return ''.join(f'<div class="step rv"><h3>{tx(a,c,lang)}</h3><p>{tx(b,d,lang)}</p></div>' for a,b,c,d in S)
def cta(lang,h_en,h_es,p_en,p_es):
    return f'<section class="cta"><div class="wrap rv"><h2>{tx(h_en,h_es,lang)}</h2><p>{tx(p_en,p_es,lang)}</p><a class="btn" href="{u(lang,"contact")}">{T[lang]["quote"]}</a></div></section>'
def svc_cards(lang):
    return ''.join(f'<a class="card rv" href="{u(lang,"sv",s)}"><h3>{L(lang,s["n"])}</h3><p>{L(lang,s["s"])}</p><span class="go">{tx("Learn more","Conocer más",lang)} →</span></a>' for s in SERVICES)
def faq_html(items): return ''.join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
def faq_ld(items): return '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]},ensure_ascii=False)+'</script>'

GENFAQ={'en':[("How fast can I get a quote?","We send a customized quote within one business day of your request. For urgent needs, call us any time — we're available 24/7."),("Do you clean at night or on weekends?","Yes. Our crews work around your schedule, including nights, weekends, and holidays."),("Are your cleaners background-checked?","Every team member is background-checked and trained to our cleaning standards before being assigned to a job."),("What if I'm not happy with a cleaning?","Tell us and we return to make it right. Satisfaction is guaranteed."),("Do you offer one-time and recurring cleaning?","Yes. We offer recurring daily, weekly, or nightly service as well as one-time cleanings."),("Which areas do you serve?","We serve businesses and homes across Missouri, Kansas, and Southern Illinois.")],
'es':[("¿Qué tan rápido recibo una cotización?","Enviamos una cotización personalizada en un día hábil. Para urgencias, llámenos a cualquier hora — estamos disponibles 24/7."),("¿Limpian de noche o en fines de semana?","Sí. Nuestros equipos trabajan según su horario, incluyendo noches, fines de semana y días festivos."),("¿Su personal tiene verificación de antecedentes?","Cada miembro del equipo pasa una verificación de antecedentes y es capacitado según nuestros estándares antes de ser asignado."),("¿Y si no quedo satisfecho con una limpieza?","Avísenos y regresamos para corregirlo. La satisfacción está garantizada."),("¿Ofrecen limpieza única y recurrente?","Sí. Ofrecemos servicio recurrente diario, semanal o nocturno, además de limpiezas únicas."),("¿Qué áreas atienden?","Atendemos empresas y hogares en Missouri, Kansas y el sur de Illinois.")]}

def slider(lang):
    S=[dict(h=tx('Professional cleaning for businesses and homes across Missouri, Kansas & Southern Illinois.','Limpieza profesional para empresas y hogares en Missouri, Kansas y el sur de Illinois.',lang),
            p=tx('Trained, vetted staff available 24/7 — backed by a satisfaction guarantee.','Personal capacitado y verificado, disponible 24/7 — respaldado por una garantía de satisfacción.',lang),
            b1=(T[lang]['quote'],u(lang,'contact')),b2=(tx('Our services','Nuestros servicios',lang),u(lang,'services')),vid=True,img='office-team'),
       dict(h=tx('Cleaning that keeps your operation running.','Limpieza que mantiene su operación en marcha.',lang),
            p=tx('Offices, industrial sites, retail, healthcare, and schools — scheduled around your hours, including nights and weekends.','Oficinas, plantas, tiendas, clínicas y escuelas — programada según su horario, incluyendo noches y fines de semana.',lang),
            b1=(tx('Commercial services','Servicios comerciales',lang),u(lang,'sv',SERVICES[0])),b2=(T[lang]['quote'],u(lang,'contact')),img='glove-detail'),
       dict(h=tx('Residential cleaning you can trust in your home.','Limpieza residencial en la que puede confiar en su hogar.',lang),
            p=tx('Recurring or one-time visits by the same vetted professionals who care for commercial properties.','Visitas recurrentes o únicas por los mismos profesionales verificados que atienden propiedades comerciales.',lang),
            b1=(tx('Residential cleaning','Limpieza residencial',lang),u(lang,'sv',SERVICES[6])),b2=(T[lang]['quote'],u(lang,'contact')),img='residential-vacuum')]
    out=''
    for k,s in enumerate(S):
        tag='h1' if k==0 else 'h2 class="h"'; close='h1' if k==0 else 'h2'
        media='<video class="bg" autoplay muted loop playsinline preload="auto" poster="/assets/office-team.jpg"><source src="/assets/hero-video.mp4" type="video/mp4"></video>' if s.get('vid') else f'<img class="bg" src="/assets/{s["img"]}.jpg" alt="" {"loading=lazy" if k else ""}>'
        out+=f'<div class="slide{" on" if k==0 else ""}" aria-roledescription="slide" aria-label="{k+1} / 3">{media}<div class="wrap"><div class="in-t"><{tag}>{s["h"]}</{close}><p class="sub">{s["p"]}</p><div class="btns"><a class="btn btn-g" href="{s["b1"][1]}">{s["b1"][0]}</a><a class="btn btn-o" href="{s["b2"][1]}">{s["b2"][0]}</a></div></div></div></div>'
    dots=''.join(f'<button aria-label="Slide {k+1}" aria-current="{"true" if k==0 else "false"}"></button>' for k in range(3))
    return f'<section class="slider" aria-roledescription="carousel" aria-label="{tx("Highlights","Destacados",lang)}">{out}<div class="sctl"><div class="wrap"><button class="arr prev" aria-label="Previous">‹</button><div class="dots">{dots}</div><button class="arr next" aria-label="Next">›</button></div></div></section>'

def stats(lang):
    S=[('24/7',tx('Availability, including holidays','Disponibilidad, incluso en festivos',lang)),('3',tx('Regions served: MO, KS & S. IL','Regiones: MO, KS y sur de IL',lang)),('8',tx('Specialized service lines','Líneas de servicio especializadas',lang)),('1',tx('Business day to receive your quote','Día hábil para recibir su cotización',lang))]
    return '<section class="stats"><div class="wrap">'+''.join(f'<div class="stat rv"><b>{a}</b><span>{b}</span></div>' for a,b in S)+'</div></section>'

def home(lang):
    es=lang=='es'
    gf=GENFAQ[lang]
    body=f'''{slider(lang)}{stats(lang)}
<section class="sec"><div class="wrap"><p class="eyebrow">{tx("What we do","Qué hacemos",lang)}</p><h2>{tx("Services for every kind of space","Servicios para todo tipo de espacio",lang)}</h2><p class="lead">{tx("From corporate offices to family homes, our crews adjust to the demands of each property type.","Desde oficinas corporativas hasta hogares, nuestros equipos se adaptan a cada propiedad.",lang)}</p><div class="grid">{svc_cards(lang)}</div><a class="more" href="{u(lang,"services")}">{tx("See all services","Ver todos los servicios",lang)} →</a></div></section>
<section class="sec dark"><div class="wrap"><p class="eyebrow">{tx("How it works","Cómo funciona",lang)}</p><h2>{tx("Simple from first call to final walkthrough","Simple, de la primera llamada al resultado final",lang)}</h2><p class="lead">{tx("No guesswork — just a clear process and a team you can count on.","Sin sorpresas: un proceso claro y un equipo en el que puede confiar.",lang)}</p><div class="steps">{steps(lang)}</div></div></section>
<section class="sec"><div class="wrap split"><div class="rv"><p class="eyebrow">{tx("About us","Nosotros",lang)}</p><h2>{tx("A cleaning company built for consistency","Una empresa de limpieza construida para la consistencia",lang)}</h2>
<p>{tx("United Cleaning Services cleans offices, industrial facilities, retail stores, schools, healthcare spaces, and homes. Our teams are trained to a consistent standard and vetted before working in any space we clean.","United Cleaning Services limpia oficinas, instalaciones industriales, tiendas, escuelas, centros de salud y hogares. Nuestros equipos son capacitados bajo un estándar consistente y verificados antes de trabajar en cualquier espacio.",lang)}</p>
<ul class="list"><li>{tx("Every technician background-checked","Cada técnico con verificación de antecedentes",lang)}</li><li>{tx("One consistent cleaning standard","Un estándar de limpieza consistente",lang)}</li><li>{tx("Satisfaction guarantee on every job","Garantía de satisfacción en cada trabajo",lang)}</li></ul>
<a class="btn btn-p" href="{u(lang,"about")}">{tx("Learn more about us","Conozca más sobre nosotros",lang)}</a></div>
<img class="rv" src="/assets/office-team.jpg" alt="{tx("United Cleaning Services team at work in a corporate lobby","Equipo de United Cleaning Services trabajando en un lobby corporativo",lang)}" loading="lazy" width="1400" height="788"></div></section>
<section class="sec alt"><div class="wrap faq"><p class="eyebrow">FAQ</p><h2>{tx("Questions, answered","Preguntas frecuentes",lang)}</h2><p class="lead">{tx("Can't find what you need? Call us any time.","¿No encuentra lo que busca? Llámenos a cualquier hora.",lang)}</p>{faq_html(gf)}</div></section>
{cta(lang,"Request a free quote","Solicite una cotización gratis","Tell us about your space and we'll send a customized quote within one business day.","Cuéntenos sobre su espacio y le enviamos una cotización personalizada en un día hábil.")}'''
    return body,faq_ld(gf)

def phead(lang,eyebrow,h1,sub='',crumbs=''):
    return f'<section class="phead"><div class="wrap">{crumbs}<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1>{f"<p class=sub>{sub}</p>" if sub else ""}</div></section>'

def sv_page(lang,s):
    i=0 if lang=='en' else 1
    name=s['n'][i]; faq=s['f'][i]
    crumbs=f'<p class="crumb"><a href="{u(lang,"home")}">{T[lang]["home"]}</a> / <a href="{u(lang,"services")}">{T[lang]["services"]}</a> / {name}</p>'
    others=''.join(f'<a href="{u(lang,"sv",o)}">{o["n"][i]}</a>' for o in SERVICES if o is not s)
    qlink=u(lang,'contact')+'?service='+s['en']
    body=f'''{phead(lang,tx("Our services","Nuestros servicios",lang),name,s['s'][i],crumbs)}
<section class="sec"><div class="wrap sv-g"><div>
<p style="font-size:18px;color:var(--muted);margin-top:0">{s['intro'][i]}</p>
<h2 style="font-size:26px;margin-top:34px">{tx("What's included","Qué incluye",lang)}</h2>
<ul class="list">{''.join(f'<li>{b}</li>' for b in s['b'][i])}</ul>
<h2 style="font-size:26px;margin:40px 0 18px">{tx("Questions about this service","Preguntas sobre este servicio",lang)}</h2>{faq_html(faq)}
</div>
<aside class="side"><h3>{tx("Get a free quote","Pida su cotización gratis",lang)}</h3><p>{tx("Tell us about your space. We reply within one business day.","Cuéntenos sobre su espacio. Respondemos en un día hábil.",lang)}</p><a class="btn btn-g" href="{qlink}">{T[lang]['quote']}</a><p style="margin:16px 0 0;text-align:center">{tx("or call","o llame",lang)} <a href="tel:{TEL}"><strong>{PH}</strong></a></p></aside></div></section>
<section class="sec alt"><div class="wrap"><h2 style="font-size:26px">{tx("Other services","Otros servicios",lang)}</h2><div class="other">{others}</div></div></section>
<section class="sec dark"><div class="wrap"><p class="eyebrow">{tx("How it works","Cómo funciona",lang)}</p><h2>{tx("Our process","Nuestro proceso",lang)}</h2><div class="steps" style="margin-top:34px">{steps(lang)}</div></div></section>
{cta(lang,"Ready to get started?","¿Listo para empezar?","A free quote is one short form away.","Una cotización gratis está a un formulario de distancia.")}'''
    return body,faq_ld(faq)

def services_index(lang):
    return f'''{phead(lang,tx("Our services","Nuestros servicios",lang),tx("Cleaning services for every property type","Servicios de limpieza para todo tipo de propiedad",lang),tx("We adjust our crews, schedule, and equipment to match the demands of the space — from corporate offices to family homes.","Ajustamos equipos, horarios y equipo de trabajo a las necesidades de cada espacio — desde oficinas corporativas hasta hogares.",lang))}
<section class="sec"><div class="wrap"><div class="grid">{svc_cards(lang)}</div></div></section>
<section class="sec dark"><div class="wrap"><p class="eyebrow">{tx("How it works","Cómo funciona",lang)}</p><h2>{tx("Our process","Nuestro proceso",lang)}</h2><div class="steps" style="margin-top:34px">{steps(lang)}</div></div></section>
{cta(lang,"Not sure which service you need?","¿No sabe qué servicio necesita?","Tell us about your space and we'll recommend a plan and send a free quote.","Cuéntenos sobre su espacio y le recomendamos un plan con cotización gratis.")}'''

TR={'en':[('clock','24/7 Availability','Crews ready around the clock, including nights, weekends, and holidays.'),('shield','Trained & Vetted Staff','Every team member is background-checked and trained to our standards before stepping on site.'),('star','Satisfaction Guaranteed',"If a cleaning doesn't meet your standards, we return to make it right.")],
'es':[('clock','Disponibilidad 24/7','Equipos listos a toda hora, incluyendo noches, fines de semana y días festivos.'),('shield','Personal Capacitado y Verificado','Cada miembro pasa una verificación de antecedentes y es capacitado según nuestros estándares.'),('star','Satisfacción Garantizada','Si una limpieza no cumple con sus estándares, regresamos para corregirlo.')]}
def about(lang):
    return f'''{phead(lang,tx("About us","Nosotros",lang),tx("A cleaning company built for consistency","Una empresa de limpieza construida para la consistencia",lang))}
<section class="sec"><div class="wrap split"><img class="rv" src="/assets/office-team.jpg" alt="{tx("United Cleaning Services team at work in a corporate lobby","Equipo de United Cleaning Services trabajando en un lobby corporativo",lang)}" width="1400" height="788">
<div class="rv"><p style="font-size:17px">{tx("United Cleaning Services provides commercial and residential cleaning across Missouri, Kansas &amp; Southern Illinois. We work with offices, industrial facilities, retail stores, healthcare spaces, schools, and homes — adjusting our approach to the demands of each type of property.","United Cleaning Services ofrece limpieza comercial y residencial en Missouri, Kansas y el sur de Illinois. Trabajamos con oficinas, instalaciones industriales, tiendas, centros de salud, escuelas y hogares, adaptando nuestro enfoque a cada tipo de propiedad.",lang)}</p>
<p style="font-size:17px">{tx("Every technician is background-checked and trained to a consistent cleaning standard before being assigned to a job. Crews are available around the clock, and if a cleaning doesn't meet your standards, we return to make it right.","Cada técnico pasa una verificación de antecedentes y es capacitado bajo un estándar consistente antes de ser asignado. Los equipos están disponibles a toda hora y, si una limpieza no cumple sus estándares, regresamos para corregirla.",lang)}</p></div></div></section>
<section class="sec alt"><div class="wrap"><p class="eyebrow">{tx("Our promise","Nuestra promesa",lang)}</p><h2>{tx("What we stand for","Lo que nos define",lang)}</h2><p class="lead">{tx("Three commitments behind every job.","Tres compromisos en cada trabajo.",lang)}</p><div class="grid">{''.join(f'<div class="card rv"><h3>{n}</h3><p>{d}</p></div>' for _,n,d in TR[lang])}</div></div></section>
<section class="sec"><div class="wrap split"><div class="rv"><p class="eyebrow">{tx("Where we work","Dónde trabajamos",lang)}</p><h2>{tx("Serving businesses and homes across Missouri, Kansas &amp; Southern Illinois.","Atendemos empresas y hogares en Missouri, Kansas y el sur de Illinois.",lang)}</h2><a class="btn btn-p" href="{u(lang,"services")}">{tx("Explore our services","Ver nuestros servicios",lang)}</a></div>
<img class="rv tall" src="/assets/residential-vacuum.jpg" alt="" loading="lazy" width="1200" height="900"></div></section>
{cta(lang,"Ready to get started?","¿Listo para empezar?","A free quote is one short form away.","Una cotización gratis está a un formulario de distancia.")}'''

def form(lang):
    es=lang=='es'
    g=lambda a,b:b if es else a
    opts=''.join(f'<option value="{s["n"][0]}" data-slug="{s["en"]}">{L(lang,s["n"])}</option>' for s in SERVICES)+f'<option value="Other">{g("Other","Otro")}</option>'
    return f'''<form class="q" data-sending="{g("Sending…","Enviando…")}">
<input type="hidden" name="_subject" value="New quote request — {C['name']}{' (ES)' if es else ''}"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
<div class="hp" aria-hidden="true"><input type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
<div class="row"><label>{g("Full Name*","Nombre completo*")}<input type="text" name="Name" required autocomplete="name"></label><label>{g("Email*","Correo electrónico*")}<input type="email" name="Email" required autocomplete="email"></label></div>
<div class="row"><label>{g("Phone*","Teléfono*")}<input type="tel" name="Phone" required autocomplete="tel"></label><label>{g("Company (optional)","Empresa (opcional)")}<input type="text" name="Company" autocomplete="organization"></label></div>
<div><label style="margin-bottom:7px">{g("Property Type","Tipo de propiedad")}</label><div class="radios"><label><input type="radio" name="Property Type" value="Commercial" checked> {g("Commercial","Comercial")}</label><label><input type="radio" name="Property Type" value="Residential"> {g("Residential","Residencial")}</label></div></div>
<label>{g("Service Needed","Servicio necesitado")}<select name="Service Needed">{opts}</select></label>
<label>{g("Message","Mensaje")}<textarea rows="4" name="Message" placeholder="{g("Tell us about your space, schedule, or any special requirements","Cuéntenos sobre su espacio, horario o requisitos especiales")}"></textarea></label>
<p class="err" hidden>{g("Something went wrong sending your request. Please call us at "+PH+".","Algo salió mal. Llámenos al "+PH+".")}</p>
<button class="btn btn-g" type="submit" style="justify-content:center">{g("Request Quote","Solicitar cotización")}</button>
</form>
<div class="ok" hidden><h3>{g("Thank you","Gracias")}</h3><p>{g("We've received your request. A member of our team will contact you within one business day.","Hemos recibido su solicitud. Un miembro de nuestro equipo se pondrá en contacto en un día hábil.")}</p></div>'''
def info(lang):
    es=lang=='es'
    return f'''<div class="info"><div class="card"><h4>{'LLÁMENOS' if es else 'CALL US'}</h4><a href="tel:{TEL}">{PH}</a></div>
<div class="card"><h4>WHATSAPP</h4><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{PH}</a></div>
<div class="card"><h4>{'ESCRÍBANOS' if es else 'EMAIL US'}</h4><a href="mailto:{EM}" style="font-size:15px">{EM}</a></div>
<div class="card"><h4>{'HORARIO' if es else 'HOURS'}</h4><p>{T[lang]['avail']}</p><h4 style="margin-top:14px">{'ÁREA DE SERVICIO' if es else 'SERVICE AREA'}</h4><p style="font-size:15px">{T[lang]['area'].replace('&','&amp;')}</p></div></div>'''
def contact(lang):
    return f'''{phead(lang,tx("Contact us","Contacto",lang),tx("Get a free quote","Solicite una cotización gratis",lang),tx("Tell us about your space and we'll send a customized quote within one business day.","Cuéntenos sobre su espacio y le enviamos una cotización personalizada en un día hábil.",lang))}
<section class="sec"><div class="wrap cgrid"><div>{form(lang)}</div>{info(lang)}</div></section>'''

# ---- generate
pairs=[]
def emit(lang,path,alt,title,desc,body,ld='',img='/assets/office-team.jpg'):
    write(path,page(lang,path,alt,title,desc,body,ld,img)); pairs.append((path,alt,lang))

for lang in('en','es'):
    other='es' if lang=='en' else 'en'
    b,ld=home(lang)
    emit(lang,u(lang,'home'),u(other,'home'),
        'United Cleaning Services | Commercial & Residential Cleaning in Missouri, Kansas & Southern Illinois' if lang=='en' else 'United Cleaning Services | Limpieza Comercial y Residencial en Missouri, Kansas y el Sur de Illinois',
        'United Cleaning Services provides commercial and residential cleaning across Missouri, Kansas & Southern Illinois with trained, vetted staff available 24/7. Get a free quote today.' if lang=='en' else 'Limpieza comercial y residencial en Missouri, Kansas y el sur de Illinois con personal capacitado y verificado, disponible 24/7. Solicite una cotización gratis.',b,ld)
    emit(lang,u(lang,'services'),u(other,'services'),
        'Cleaning Services | Office, Industrial, Retail & More — United Cleaning Services' if lang=='en' else 'Servicios de Limpieza | Oficinas, Industrial, Tiendas y Más — United Cleaning Services',
        'Commercial and residential cleaning services: office, industrial, retail, healthcare, post-construction, schools, residential, and floor & carpet care.' if lang=='en' else 'Servicios de limpieza comercial y residencial: oficinas, industrial, tiendas, clínicas, post-construcción, escuelas, residencial y pisos y alfombras.',services_index(lang))
    emit(lang,u(lang,'about'),u(other,'about'),'About Us | United Cleaning Services' if lang=='en' else 'Nosotros | United Cleaning Services',
        'United Cleaning Services cleans offices, industrial facilities, retail stores, schools, healthcare spaces, and homes with trained, vetted staff.' if lang=='en' else 'United Cleaning Services limpia oficinas, instalaciones industriales, tiendas, escuelas, centros de salud y hogares con personal capacitado y verificado.',about(lang),img='/assets/office-team.jpg')
    emit(lang,u(lang,'contact'),u(other,'contact'),'Contact Us | Get a Free Cleaning Quote — United Cleaning Services' if lang=='en' else 'Contacto | Cotización Gratis de Limpieza — United Cleaning Services',
        f'Request a free quote for commercial or residential cleaning. Call {PH} or fill out our form — available 24/7.' if lang=='en' else f'Solicite una cotización gratis de limpieza comercial o residencial. Llame al {PH} o use nuestro formulario — disponible 24/7.',contact(lang))
    for s in SERVICES:
        b,ld=sv_page(lang,s); i=0 if lang=='en' else 1
        emit(lang,u(lang,'sv',s),u(other,'sv',s),f'{s["n"][i]} | United Cleaning Services',s['s'][i]+(' Free quote within one business day.' if lang=='en' else ' Cotización gratis en un día hábil.'),b,ld)

sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
for p,a,lang in pairs:
    en,es=(p,a) if lang=='en' else (a,p)
    sm+=f'<url><loc>{BASE}{p}</loc><xhtml:link rel="alternate" hreflang="en" href="{BASE}{en}"/><xhtml:link rel="alternate" hreflang="es" href="{BASE}{es}"/><priority>{1.0 if p in("/","/es/") else 0.7}</priority></url>\n'
open(f'{ROOT}/sitemap.xml','w').write(sm+'</urlset>\n')
print(len(pairs),'pages')
