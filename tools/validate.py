#!/usr/bin/env python3
"""SEO/link sanity check for the generated site."""
import os,re,json,sys,glob
from html.parser import HTMLParser
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages=[f for f in glob.glob(ROOT+'/**/*.html',recursive=True) if '/.git/' not in f]
def exists(u):
    u=u.split('#')[0].split('?')[0]
    if not u or u.startswith(('http','mailto:','tel:','data:')):return True
    p=ROOT+u
    return os.path.isfile(p) or os.path.isfile(os.path.join(p,'index.html'))
bad=0;titles={}
for f in sorted(pages):
    h=open(f).read();rel=f[len(ROOT):]
    def err(m):
        global bad;bad+=1;print('ERR',rel,m)
    t=re.search(r'<title>(.*?)</title>',h);d=re.search(r'name="description" content="(.*?)"',h)
    if not t:err('no title')
    else:
        titles.setdefault(t.group(1),[]).append(rel)
        if len(t.group(1))>75:err(f'title long {len(t.group(1))}')
    if not d:err('no desc')
    elif len(d.group(1))>165:err(f'desc long {len(d.group(1))}')
    if len(re.findall(r'<h1[ >]',h))!=1:err('h1 count %d'%len(re.findall(r'<h1[ >]',h)))
    if 'rel="canonical"' not in h:err('no canonical')
    if rel!='/404.html' and 'hreflang="es"' not in h:err('no hreflang')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
        try:json.loads(j)
        except Exception as e:err('bad jsonld')
    for u in re.findall(r'(?:href|src)="([^"]+)"',h):
        if not exists(u):err('broken '+u)
    for m in re.findall(r'<img[^>]*>',h):
        if ' alt=' not in m:err('img no alt')
for t,v in titles.items():
    if len(v)>1:print('WARN duplicate title',t,v);bad+=1
sm=open(ROOT+'/sitemap.xml').read()
for u in re.findall(r'<loc>https://unitedcleaning.us(.*?)</loc>',sm):
    if not exists(u):print('ERR sitemap',u);bad+=1
print(len(pages),'pages checked;','OK' if not bad else f'{bad} problems')
sys.exit(1 if bad else 0)
