"""Dependency-free multilingual static site generator. Run with Python 3.9+."""
from pathlib import Path
import json, shutil, html, re, os
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'content/project.json').read_text()); C=json.loads((ROOT/'content/locales.json').read_text()); A=json.loads((ROOT/'content/assets.json').read_text())
OUT=ROOT/'docs'; OUT.mkdir(exist_ok=True);shutil.copytree(ROOT/'public',OUT,dirs_exist_ok=True)
DOMAIN=P['domain'];langs=P['languages'];unitkeys=P['units'];routes=['','residences/studio/','residences/1br/','residences/2br/','residences/3br/','payment-plan/','privacy/']
e=html.escape

def route(lang,key=''):return f'{lang}/{key}'
def number(n,lang):
 s=f'{round(n):,}'
 return s if lang=='en' else s.replace(',', ' ' if lang in ['fr','pt'] else '.')
def money(n,lang):return number(n,lang)+' AED'
def usd(n,lang):return '≈ '+number(n/P['aed_per_usd'],lang)+' USD'
def render(lang,key='',root_alias=False):
 t=C[lang]; current=route(lang,key); depth=0 if root_alias else len(current.strip('/').split('/'));base='../'*depth
 link=lambda path:base+path
 home=link(route(lang));pay=link(route(lang,'payment-plan/')); privacy=link(route(lang,'privacy/'));canonical=DOMAIN+'/'+current
 unit=unitkeys.index(key.split('/')[1]) if key.startswith('residences/') else None
 ishome=key=='';isprivacy=key=='privacy/';ispay=key=='payment-plan/'
 title=(P['name']+' | '+t['nav'][0]+' · Al Marjan Island') if ishome else (t['unitNames'][unit] if unit is not None else t['paymentPage'] if ispay else t['privacyTitle'])+' | '+P['name']
 description=t['homeMeta'] if ishome else t['unitMeta'].format(unit=t['unitNames'][unit]) if unit is not None else t['paymentMeta'] if ispay else t['privacyTitle']+' — '+P['name']
 def pic(name,caption,hero=False):
  a=A[name];src=link(f'assets/{name}.webp');small=link(f'assets/{name}-800.webp')
  img=f'<img src="{src}" srcset="{small} 800w, {src} {a["width"]}w" sizes="{("100vw" if hero else "(max-width: 700px) 100vw, 60vw")}" width="{a["width"]}" height="{a["height"]}" alt="{e(caption)}" '+('fetchpriority="high"' if hero else 'loading="lazy" decoding="async"')+'>'
  wrap=f'<span class="watermarked">{img}<span class="image-watermark" aria-hidden="true">dolce-residences-almarjan.com</span></span>'
  return wrap if hero else f'<figure class="project-figure">{wrap}<figcaption class="caption">{e(caption)}</figcaption></figure>'
 def cta(label=None,cls='dark'):return f'<a class="button {cls}" href="#enquire">{e(label or t["cta"])} <span aria-hidden="true">↗</span></a>'
 def priceblock():return f'<div class="start-price"><span class="eyebrow">{t["from"]}</span><strong>{money(P["starting_price_aed"],lang)}</strong><span>{usd(P["starting_price_aed"],lang)} · {t["estimate"]}</span></div>'
 def units(exclude=None):
  rows=''
  for i,u in enumerate(unitkeys):
   if i==exclude:continue
   rows+=f'<a class="residence-row" href="{link(route(lang,"residences/"+u+"/"))}"><span class="row-number">0{i+1}</span><span><h3>{t["unitNames"][i]}</h3><p>{t["onRequest"]}</p></span><span class="row-cta">{t["viewUnit"]} <b aria-hidden="true">↗</b></span></a>'
  return f'<div class="residence-list">{rows}</div>'
 def payment(calculator=False):
  amount=P['starting_price_aed']; a=round(amount*P['booking_percent']/100);b=amount-a
  text=f'<div class="payment-head"><div><p class="eyebrow">{t["nav"][2]}</p><h2>{t["paymentTitle"]}</h2><p class="lead">{t["paymentIntro"]}</p></div><div class="plan-number">30<span>/</span>70</div></div><p class="eyebrow">{t["example"]} · {money(amount,lang)}</p>'
  if calculator:text+=f'<div class="calculator"><h3>{t["calcTitle"]}</h3><label for="property-price">{t["calcLabel"]}</label><input id="property-price" type="number" min="1400000" max="1000000000" step="1" value="1400000" aria-describedby="calc-help calc-error"><p class="small" id="calc-help">{t["calcHelp"]}</p><p id="calc-error" role="alert" data-message="{e(t["calcError"])}"></p></div>'
  text+=f'<div class="payment-results" aria-live="polite"><div class="timeline"><article class="milestone"><strong>30%</strong><h3>{t["booking"]}</h3><div class="unit-amount"><strong data-payment="booking">{money(a,lang)}</strong><span data-usd="booking">{usd(a,lang)}</span></div></article><article class="milestone"><strong>70%</strong><h3>{t["handover"]}</h3><div class="unit-amount"><strong data-payment="handover">{money(b,lang)}</strong><span data-usd="handover">{usd(b,lang)}</span></div></article></div>'
  if calculator:text+=f'<div class="totals"><p>{t["total"]}<strong data-payment="total">{money(amount,lang)}</strong></p><p>{t["before"]}<strong data-payment="before">{money(a,lang)}</strong></p><p>{t["after"]}<strong>0 AED</strong></p></div>'
  text+=f'</div><p class="small">{t["paymentNote"]}</p><p class="small muted">{t["exchange"]}</p>'
  if not calculator:text+=f'<a class="text-link" href="{pay}">{t["paymentDetail"]} ↗</a>'
  return '<section class="wrap payment" id="payment">'+text+'</section>'
 alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{DOMAIN}/{route(l,key)}">' for l in langs)+f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{route("en",key)}">'
 schema=[{'@context':'https://schema.org','@type':'WebPage','name':title,'description':description,'url':canonical,'inLanguage':lang,'isPartOf':{'@type':'WebSite','name':P['name'],'url':DOMAIN+'/en/'}}]
 if not ishome:schema.append({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':t['home'],'item':DOMAIN+'/'+route(lang)},{'@type':'ListItem','position':2,'name':title,'item':canonical}]})
 body=f'<a class="skip-link" href="#main">{t["skip"]}</a><header><a class="brand" href="{home}" aria-label="{e(P["name"])}">DOLCE<span>RESIDENCES BY WYNDHAM</span></a><nav aria-label="{e(t["home"])}"><a href="{home}#residences">{t["nav"][0]}</a><a href="{home}#island">{t["nav"][1]}</a><a href="{pay}">{t["nav"][2]}</a><details class="language-picker"><summary aria-label="{e(t["language"])}">{lang.upper()}</summary><div class="language-menu">'+''.join(f'<a href="{link(route(l,key))}" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{C[l]["language"]}</a>' for l in langs)+f'</div></details>{cta(t["nav"][3],"light")}</nav></header><main id="main">'
 heroimg='dolce-hero' if ishome else 'project-front' if unit is not None else 'project-evening'
 herocaption=t['renderCaption']
 heading=t['hero'] if ishome else t['unitNames'][unit] if unit is not None else t['paymentPage'] if ispay else t['privacyTitle']
 intro=t['intro'] if ishome else t['unitIntro'].format(unit=t['unitNames'][unit]) if unit is not None else t['paymentIntro'] if ispay else P['name']
 body+=f'<section class="hero {"home-hero" if ishome else "inner-hero"}">{pic(heroimg,herocaption,True)}<div class="hero-content"><h1><span class="hero-kicker">{e(P["name"])} · AL MARJAN ISLAND</span>{heading}</h1><p class="intro">{intro}</p>{cta(cls="light") if not isprivacy else ""}</div>'
 if ishome:body+=f'<div class="hero-bottom"><div><span>{t["from"]}</span><strong>{money(P["starting_price_aed"],lang)}</strong><small>{usd(P["starting_price_aed"],lang)}</small></div><div><span>{t["nav"][2]}</span><strong>30 / 70</strong><small>{t["booking"]} / {t["handover"]}</small></div><div><span>{t["locationLabel"]}</span><strong>Q4 2028*</strong><small>{t["completion"]}</small></div></div>'
 body+=f'</section><p class="hero-caption">{herocaption}</p>'
 if ishome:
  body+=f'<section class="wrap project-section"><div class="split"><div><p class="eyebrow">01 / DOLCE</p><h2>{t["projectTitle"]}</h2><p class="lead">{t["projectText"]}</p><p class="muted">{t["projectNote"]}</p></div>{pic("project-front",t["renderCaption"])}</div><div class="stats"><div><strong>93*</strong><span>{t["residencesCount"]}</span></div><div><strong>04</strong><span>{t["typesCount"]}</span></div><div><strong>HRA08</strong><span>{t["locationLabel"]}</span></div></div></section>'
  body+=f'<section class="wrap island-section" id="island"><div class="split">{pic("al-marjan-island",t["heroCaption"])}<div><p class="eyebrow">02 / AL MARJAN ISLAND</p><h2>{t["islandTitle"]}</h2><p class="lead">{t["islandText"]}</p><p class="small muted">{t["islandNote"]}</p></div></div><div class="destination-panorama">{pic("al-marjan-hero",t["heroCaption"])}</div></section>'
  body+=f'<section class="wrap night" id="residences"><p class="eyebrow">03 / {t["nav"][0]}</p><div class="split"><div><h2>{t["residencesTitle"]}</h2><p>{t["residencesText"]}</p></div>{priceblock()}</div>{units()}<p class="small res-note">{t["priceNote"]}</p><p class="small res-note">{t["exchange"]}</p></section>'
  body+=f'<section class="wrap experiences"><div class="experience-row">{pic("project-corner",t["renderCaption"])}<div><p class="eyebrow">04 / DOLCE</p><h2>{t["architectureTitle"]}</h2><p>{t["architectureText"]}</p></div></div><div class="experience-row">{pic("project-pool",t["renderCaption"])}<div><h2>{t["poolTitle"]}</h2><p>{t["poolText"]}</p></div></div></section>'
 if unit is not None:
  vals=[t['unitShort'][unit]]+[t['onRequest']]*3
  body+=f'<section class="wrap unit-overview"><p class="eyebrow">DOLCE / {t["unitShort"][unit]}</p><div class="split"><div><h2>{t["unitHeading"]}</h2><p class="lead">{t["unitDescriptions"][unit]}</p></div>{priceblock()}</div><p class="small">{t["priceNote"]}</p><dl class="unit-facts">'+''.join(f'<div><dt>{x}</dt><dd>{v}</dd></div>' for x,v in zip(t['factsLabels'],vals))+f'</dl><p class="small">{t["projectNote"]}</p></section><section class="wrap unit-plan"><div class="split">{pic("plot-plan",t["planCaption"])}<div><h2>{t["plansTitle"]}</h2><p>{t["plansText"]}</p>{cta(t["requestPlan"])}</div></div></section>'
 if ishome or unit is not None:
  body+=f'<section class="wrap"><div class="heading-row"><h2>{t["interiorsTitle"]}</h2><p>{t["interiorsText"]}</p></div><div class="interior-gallery">{pic("interior-mood",t["moodCaption"])}{pic("bedroom-mood",t["moodCaption"])}{pic("lobby-mood",t["moodCaption"])}</div></section>'
  body+=payment()
 if ispay:
  body+=payment(True)+f'<section class="wrap accent"><div class="split"><div><h2>{t["fees"]}</h2><p>{t["feesText"]}</p></div><div><h3>{t["unitPaymentNote"]}</h3><p>{t["priceNote"]}</p></div></div>{units()}</section>'
 if isprivacy:
  body+=f'<section class="wrap legal-content"><h2>{t["privacyTitle"]}</h2><p>{t["privacyText"]}</p><p>{t["privacyNote"]}</p><h3>{t["source"]}</h3><p>{t["sourceText"]}</p><p>{t["legal"]}</p></section>'
 else:
  body+=f'<section class="wrap accent"><div class="faq-grid"><h2>{t["faqTitle"]}</h2><div>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in t['faq'])+'</div></div></section>'
 if unit is not None:body+=f'<section class="wrap"><h2>{t["otherUnits"]}</h2>{units(unit)}</section>'
 tally=f'https://tally.so/embed/{P["tally_id"]}?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&page_language={lang}'
 body+=f'<section class="wrap contact" id="enquire"><div class="split"><div><p class="eyebrow">DOLCE RESIDENCES BY WYNDHAM</p><h2>{t["contactTitle"]}</h2><p>{t["contactText"]}</p><ul class="benefit-list">'+''.join(f'<li>{x}</li>' for x in t['contactList'])+f'</ul></div><div class="form-shell"><iframe src="{e(tally)}" data-tally-src="{e(tally)}" loading="lazy" width="100%" height="540" title="{e(t["formTitle"])}"></iframe><p class="form-fallback"><a href="https://tally.so/r/{P["tally_id"]}" target="_blank" rel="noopener">{t["formFallback"]} ↗</a></p><p class="small muted">{t["formNotice"]} <a href="{privacy}">{t["privacy"]}</a></p></div></div></section></main>'
 body+=f'<footer><div class="footer-top"><div><a class="brand" href="{home}">DOLCE<span>RESIDENCES BY WYNDHAM</span></a><p>Al Marjan Island<br>Ras Al Khaimah · UAE</p></div><div class="footer-links"><a href="{home}">{t["home"]}</a><a href="{pay}">{t["paymentPage"]}</a><a href="{privacy}">{t["privacy"]}</a></div><div class="footer-links">'+''.join(f'<a href="{link(route(lang,"residences/"+u+"/"))}">{t["unitNames"][i]}</a>' for i,u in enumerate(unitkeys))+'</div></div><div class="languages">'+''.join(f'<a href="{link(route(l,key))}" lang="{l}">{C[l]["language"]}</a>' for l in langs)+f'</div><p class="legal">{t["legal"]}</p><p class="small">© 2026 · dolce-residences-almarjan.com</p></footer><a class="button sticky" href="#enquire">{t["cta"]} ↗</a>'
 return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description)}"><link rel="canonical" href="{canonical}">{alternates}<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{canonical}"><meta property="og:locale" content="{t["locale"].replace("-","_")}"><meta name="theme-color" content="#082f3c"><link rel="icon" href="{link("assets/favicon.svg")}" type="image/svg+xml"><link rel="stylesheet" href="{link("assets/style.css")}"><link rel="stylesheet" href="{link("assets/dolce.css")}"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script defer src="{link("assets/app.js")}"></script><script defer src="{link("assets/calculator.js")}"></script></head><body data-locale="{t["locale"]}" data-aed-usd="{P["aed_per_usd"]}" data-booking="{P["booking_percent"]}">{body}</body></html>'

for lang in langs:
 for key in routes:
  target=OUT/route(lang,key)/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(render(lang,key))
(OUT/'index.html').write_text(render('en',root_alias=True))
(OUT/'.nojekyll').write_text('')
(OUT/'404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | Dolce Residences by Wyndham</title><body style="font:20px sans-serif;padding:10vw;background:#f5f7f5;color:#102f38"><h1>Page not found</h1><p>Dolce Residences by Wyndham</p><a id="back-home" href="'+DOMAIN+'/en/">Return to the residences</a><script>document.getElementById("back-home").href=(location.hostname.endsWith("github.io")?"/dolce-residences-almarjan":"")+"/en/";</script></body></html>')
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9');ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml');ET.register_namespace('image','http://www.google.com/schemas/sitemap-image/1.1')
ns='http://www.sitemaps.org/schemas/sitemap/0.9'; sitemap=ET.Element('{'+ns+'}urlset'); ims=ET.Element('{'+ns+'}urlset')
for lang in langs:
 for key in routes:
  url=ET.SubElement(sitemap,'{'+ns+'}url');ET.SubElement(url,'{'+ns+'}loc').text=DOMAIN+'/'+route(lang,key)
  for alt in langs+['x-default']:ET.SubElement(url,'{http://www.w3.org/1999/xhtml}link',{'rel':'alternate','hreflang':alt,'href':DOMAIN+'/'+route('en' if alt=='x-default' else alt,key)})
  if key=='':
   ur=ET.SubElement(ims,'{'+ns+'}url');ET.SubElement(ur,'{'+ns+'}loc').text=DOMAIN+'/'+route(lang)
   for name in ['dolce-hero','al-marjan-hero','al-marjan-island','project-front','project-corner','project-pool','interior-mood','bedroom-mood','lobby-mood']:
    im=ET.SubElement(ur,'{http://www.google.com/schemas/sitemap-image/1.1}image');ET.SubElement(im,'{http://www.google.com/schemas/sitemap-image/1.1}loc').text=DOMAIN+f'/assets/{name}.webp'
ET.ElementTree(sitemap).write(OUT/'sitemap.xml',encoding='utf-8',xml_declaration=True);ET.ElementTree(ims).write(OUT/'sitemap-images.xml',encoding='utf-8',xml_declaration=True)
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\nSitemap: {DOMAIN}/sitemap-images.xml\n')
print(f'Built {len(langs)*len(routes)} localized pages + English root and 404 in {OUT}')
