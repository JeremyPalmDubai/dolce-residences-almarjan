"""Static integrity checks: all pages, local assets, anchors, translations and SEO."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];D=R/'docs';P=json.loads((R/'content/project.json').read_text());C=json.loads((R/'content/locales.json').read_text())
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.nodes=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
pages={f:Page(f.read_text()) for f in D.rglob('*.html')};errors=[]
def check(v,msg):
 if not v:errors.append(msg)
for file,page in pages.items():
 text=file.read_text();rel=file.relative_to(D).as_posix()
 if file.name=='404.html':continue
 nodes=page.nodes;lang=next(a['lang'] for t,a in nodes if t=='html');check(lang in P['languages'],rel+' language')
 check(sum(t=='h1' for t,a in nodes)==1,rel+' H1')
 canonical=[a['href'] for t,a in nodes if t=='link' and a.get('rel')=='canonical'];check(len(canonical)==1 and canonical[0].startswith(P['domain']),rel+' canonical')
 alternates=[a for t,a in nodes if t=='link' and a.get('rel')=='alternate'];check(len(alternates)==7,rel+' hreflang count');check(set(a['hreflang'] for a in alternates)==set(P['languages']+['x-default']),rel+' hreflang languages')
 expected=rel.removesuffix('index.html') if rel!='index.html' else 'en/'
 check(canonical==[P['domain']+'/'+expected],rel+' exact canonical')
 for a in alternates:
  target=D/a['href'].replace(P['domain']+'/','')/'index.html';check(target.exists(),rel+' hreflang target')
  if target in pages:check(any(ta.get('href')==canonical[0] for tt,ta in pages[target].nodes if tt=='link' and ta.get('rel')=='alternate'),rel+' reciprocal hreflang')
 check(any(t=='iframe' and 'tally.so/embed/kdVP5j' in a.get('src','') and a.get('title') for t,a in nodes),rel+' Tally')
 for tag,a in nodes:
  for attr in ['href','src']:
   if attr not in a:continue
   url=urlsplit(a[attr])
   if url.scheme or url.netloc:continue
   target=(file.parent/unquote(url.path)).resolve() if url.path else file
   if target.is_dir():target=target/'index.html'
   check(target.exists(),rel+' missing '+a[attr])
   if url.fragment and target in pages:check(any(ta.get('id')==url.fragment for tt,ta in pages[target].nodes),rel+' anchor '+a[attr])
  if tag=='img':check(all(a.get(k) for k in ['width','height','alt']),rel+' image metadata')
 for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text):json.loads(s)
 check(not re.search(r'the.views|ardee|2EQxVj|50/50|616',text,re.I),rel+' source residue')
 check(len(re.findall(r'<meta name="description"',text))==1,rel+' description')
for lang,c in C.items():check(set(c)==set(C['en']),lang+' translation keys')
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}
smap=ET.parse(D/'sitemap.xml'); urls=[x.text for x in smap.findall('.//s:loc',ns)];check(len(urls)==42 and len(set(urls))==42,'sitemap entries')
for u in urls:check((D/u.replace(P['domain']+'/','')/'index.html').exists(),'sitemap '+u)
for x in ET.parse(D/'sitemap-images.xml').findall('.//i:loc',ns):check((D/x.text.replace(P['domain']+'/','')).exists(),'image sitemap '+x.text)
check(P['booking_percent']+P['handover_percent']==100,'percentages');check(round(P['starting_price_aed']*.3)==420000,'booking');check(round(P['starting_price_aed']*.7)==980000,'handover')
if errors:raise SystemExit('\n'.join(errors))
print('PASS: 42 localized pages + root; local links/assets/anchors, reciprocal hreflang, canonical URLs, JSON-LD, Tally, translation key parity, both sitemaps, 30/70 amounts, source residue scan.')
