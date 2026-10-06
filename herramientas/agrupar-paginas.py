#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agrupa el sitio en 4 páginas (index, padecimientos, cuando-acudir, contacto) + 5 de padecimientos. Se corre una vez."""
import re, json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE='https://www.reumadanmora.com/'
CTA_MARCA='<h3>¿Dudas? Mejor pregunta</h3>'
def leer(f): return open(f,encoding='utf-8').read()
def seccion_de(archivo):
    s=leer(archivo); a=s.index('<!-- ============'); 
    b=s.find('<section class="seccion">\n  <div class="container bento">\n    <div class="tile tile-tinte tile-aviso c-12 reveal">\n      <div>\n        '+CTA_MARCA)
    if b<0: b=s.index('</main>')
    return s[a:b]
idx=leer('index.html')
head=idx[idx.index('<head>'):idx.index('</head>')+7]
nav=re.search(r'<nav class="topbar".*?</nav>',idx,re.S).group(0)
footer=re.search(r'<footer>.*?</footer>',idx,re.S).group(0)
hero=idx[idx.index('<!-- ============ HERO ============ -->'):idx.index('<!-- ============ CINTA ============ -->')]
cinta=idx[idx.index('<!-- ============ CINTA ============ -->'):idx.index('<!-- ============ EXPLORA ============ -->')]
contacto_home=idx[idx.index('<!-- ============ CONTACTO ============ -->'):idx.index('</main>')]
S={k:seccion_de(f) for k,f in [('sobre','sobre-mi.html'),('reuma','reumatologia.html'),('pad','padecimientos.html'),('guia','sintomas.html'),('videos','videos.html'),('podcast','podcast.html'),('consultorio','consultorio.html'),('contacto','contacto.html'),('faq','preguntas.html')]}
# contacto.html traía contacto+redes juntos
ld_idx=json.loads(re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',idx,re.S).group(1))
def nodo(archivo,tipo):
    g=json.loads(re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',leer(archivo),re.S).group(1))['@graph']
    return [n for n in g if (n['@type'] if isinstance(n['@type'],str) else '/'.join(n['@type']))==tipo]
website=nodo('index.html','WebSite')[0]; imagen=nodo('index.html','ImageObject')[0]
physician=nodo('index.html','Physician/Person')[0]; clinica=nodo('index.html','MedicalClinic')[0]
itemlist=nodo('padecimientos.html','ItemList')[0]; faq=nodo('preguntas.html','FAQPage')[0]
video=nodo('videos.html','VideoObject')[0]; serie=nodo('podcast.html','PodcastSeries')[0]; episodios=nodo('podcast.html','PodcastEpisode')
physician_min={"@type":"Physician","@id":BASE+"#physician","name":physician['name'],"url":BASE,"medicalSpecialty":"Rheumatology","telephone":physician['telephone'],"address":physician['address'],"sameAs":physician['sameAs']}

# ---------- mapa de enlaces ----------
MAPA=[('sobre-mi.html','index.html#sobre-mi'),('reumatologia.html','padecimientos.html#reumatologia'),('sintomas.html','cuando-acudir.html'),('preguntas.html','cuando-acudir.html#preguntas'),('videos.html','index.html#videos'),('podcast.html','index.html#podcast'),('consultorio.html','contacto.html#consultorio'),('contacto.html#redes','contacto.html#redes')]
def enlazar(html, propia):
    for viejo,nuevo in MAPA:
        html=html.replace(f'href="{viejo}"',f'href="{nuevo}"')
    # misma página: dejar solo el ancla
    html=re.sub(r'href="'+re.escape(propia)+r'#([\w-]+)"',r'href="#\1"',html)
    html=html.replace(f'href="{propia}"','href="#top"' if propia=='index.html' else f'href="{propia}"')
    return html

# ---------- barra y pie nuevos ----------
nav_nuevo=re.sub(r'<ul class="nav-links">.*?</ul>','''<ul class="nav-links">
      <li><a href="index.html#sobre-mi" class="nav-link">El doctor</a></li>
      <li><a href="padecimientos.html" class="nav-link">Padecimientos</a></li>
      <li><a href="cuando-acudir.html" class="nav-link">¿Cuándo acudir?</a></li>
      <li><a href="contacto.html" class="nav-link">Consultorio y contacto</a></li>
    </ul>''',nav,flags=re.S)
nav_nuevo=re.sub(r'<ul class="drawer-links">.*?</ul>','''<ul class="drawer-links">
      <li><a href="index.html#sobre-mi" class="drawer-link">El doctor</a></li>
      <li><a href="padecimientos.html" class="drawer-link">Padecimientos</a></li>
      <li><a href="padecimientos.html#reumatologia" class="drawer-link">¿Qué es la reumatología?</a></li>
      <li><a href="cuando-acudir.html" class="drawer-link">¿Cuándo acudir?</a></li>
      <li><a href="cuando-acudir.html#preguntas" class="drawer-link">Preguntas frecuentes</a></li>
      <li><a href="index.html#videos" class="drawer-link">Videos y podcast</a></li>
      <li><a href="contacto.html" class="drawer-link">Consultorio y contacto</a></li>
      <li><a href="aviso-de-privacidad.html" class="drawer-link">Aviso de privacidad</a></li>
    </ul>''',nav_nuevo,flags=re.S)
footer_nuevo=re.sub(r'<ul class="footer-links">.*?</ul>','''<ul class="footer-links">
      <li><a href="index.html#sobre-mi">El doctor</a></li>
      <li><a href="padecimientos.html">Padecimientos</a></li>
      <li><a href="padecimientos.html#reumatologia">¿Qué es la reumatología?</a></li>
      <li><a href="cuando-acudir.html">¿Cuándo acudir?</a></li>
      <li><a href="cuando-acudir.html#preguntas">Preguntas frecuentes</a></li>
      <li><a href="contacto.html">Consultorio y contacto</a></li>
      <li><a href="aviso-de-privacidad.html">Aviso de privacidad</a></li>
    </ul>''',footer,flags=re.S)

def head_pagina(archivo,titulo,desc,grafo,og_type='website',preload_hero=False):
    url=BASE+archivo if archivo!='index.html' else BASE
    hd=head
    hd=re.sub(r'<title>.*?</title>',f'<title>{titulo}</title>',hd)
    hd=re.sub(r'<meta name="description" content="[^"]*" />',f'<meta name="description" content="{desc}" />',hd)
    for pat in ['<link rel="canonical" href="{0}" />','<link rel="alternate" hreflang="es-MX" href="{0}" />','<link rel="alternate" hreflang="x-default" href="{0}" />','<meta property="og:url" content="{0}" />']:
        hd=hd.replace(pat.format(BASE),pat.format(url))
    hd=hd.replace('<meta property="og:type" content="website" />',f'<meta property="og:type" content="{og_type}" />')
    hd=re.sub(r'<meta property="og:title" content="[^"]*" />',f'<meta property="og:title" content="{titulo}" />',hd)
    hd=re.sub(r'<meta property="og:description" content="[^"]*" />',f'<meta property="og:description" content="{desc}" />',hd)
    hd=re.sub(r'<meta name="twitter:title" content="[^"]*" />',f'<meta name="twitter:title" content="{titulo}" />',hd)
    hd=re.sub(r'<meta name="twitter:description" content="[^"]*" />',f'<meta name="twitter:description" content="{desc}" />',hd)
    if not preload_hero: hd=hd.replace('  <link rel="preload" as="image" href="images/web/doctor-bn-full.webp" type="image/webp" fetchpriority="high" />\n','')
    hd=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">\n'+json.dumps(grafo,ensure_ascii=False,indent=2)+'\n  </script>',hd,flags=re.S)
    return hd
def grafo(archivo,nombre,desc,extra,miga=None):
    url=BASE+archivo if archivo!='index.html' else BASE
    migas=[{"@type":"ListItem","position":1,"name":"Inicio","item":BASE}]+([{"@type":"ListItem","position":2,"name":miga,"item":url}] if miga else [])
    return {"@context":"https://schema.org","@graph":[website,{"@type":"WebPage","@id":url+"#webpage","url":url,"name":nombre,"description":desc,"inLanguage":"es-MX","isPartOf":{"@id":BASE+"#website"},"about":{"@id":BASE+"#physician"},"breadcrumb":{"@id":url+"#migas"},"primaryImageOfPage":{"@id":BASE+"#imagen"}},imagen,{"@type":"BreadcrumbList","@id":url+"#migas","itemListElement":migas}]+extra}
CTA='''<section class="seccion">
  <div class="container bento">
    <div class="tile tile-tinte tile-aviso c-12 reveal">
      <div>
        <h3>¿Dudas? Mejor pregunta</h3>
        <p>Escríbenos por WhatsApp y te orientamos. Si hace falta valoración, agendamos en el momento.</p>
      </div>
      <div class="acciones">
        <a href="https://wa.me/524774011085?text=Hola%20doctor,%20quisiera%20agendar%20una%20cita" class="btn btn-primario" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i> Agendar por WhatsApp</a>
        <a href="contacto.html" class="btn btn-contorno"><i class="fa-solid fa-location-dot" aria-hidden="true"></i> Consultorio y horarios</a>
      </div>
    </div>
  </div>
</section>
'''
def escribir(archivo,titulo,desc,miga,cuerpo,extra,cta=True,clase='pag',preload=False):
    hd=head_pagina(archivo,titulo,desc,grafo(archivo,titulo,desc,extra,miga),preload_hero=preload)
    migas=f'<div class="container"><nav class="migas" aria-label="Ruta"><a href="index.html">Inicio</a><i class="fa-solid fa-play" aria-hidden="true"></i><span aria-current="page">{miga}</span></nav></div>\n' if miga else ''
    html=f'''<!DOCTYPE html>
<html lang="es-MX">
{hd}
<body id="top" data-raiz=""{(' class="'+clase+'"') if clase else ''}>
<a class="saltar" href="#contenido">Ir al contenido</a>
{enlazar(nav_nuevo,archivo)}

<main id="contenido">
{migas}{enlazar(cuerpo,archivo)}{enlazar(CTA,archivo) if cta else ''}</main>

{enlazar(footer_nuevo,archivo)}
</body>
</html>
'''
    open(archivo,'w',encoding='utf-8').write(html); print('escrita',archivo)

# ---------- INICIO: héroe, cinta, el doctor, accesos, videos, podcast, contacto ----------
accesos='''<!-- ============ ACCESOS ============ -->
<section class="seccion" id="explora">
  <div class="container">
    <div class="seccion-cabecera reveal">
      <span class="etiqueta">Por dónde empezar</span>
      <h2>Tres páginas, tres preguntas</h2>
    </div>
    <div class="bento">
      <a class="tile explora c-4 reveal" href="padecimientos.html">
        <span class="ico"><i class="fa-solid fa-hand-dots" aria-hidden="true"></i></span>
        <span class="explora-titulo">¿Qué atiende un reumatólogo?</span>
        <span class="explora-texto">Qué es la reumatología sin palabras raras, y los padecimientos uno por uno: artritis reumatoide, lupus, Sjögren, espondiloartritis, vasculitis y más.</span>
        <span class="explora-ir">Ver padecimientos <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></span>
      </a>
      <a class="tile explora c-4 reveal" href="cuando-acudir.html">
        <span class="ico"><i class="fa-solid fa-list-check" aria-hidden="true"></i></span>
        <span class="explora-titulo">¿Tengo que ir?</span>
        <span class="explora-texto">Las señales por tipo y las preguntas de siempre. Si reconoces una, ya sabes a quién escribirle.</span>
        <span class="explora-ir">Ver la guía <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></span>
      </a>
      <a class="tile explora c-4 reveal" href="contacto.html">
        <span class="ico"><i class="fa-solid fa-location-dot" aria-hidden="true"></i></span>
        <span class="explora-titulo">¿Dónde y cuándo?</span>
        <span class="explora-texto">Médica Campestre, cómo llegar, horarios, WhatsApp y redes. Y fotos, para que no te pierdas.</span>
        <span class="explora-ir">Consultorio y contacto <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></span>
      </a>
    </div>
  </div>
</section>

'''
home=hero+cinta+S['sobre']+accesos+S['videos']+S['podcast']+contacto_home
desc_home=re.search(r'<meta name="description" content="([^"]*)" />',head).group(1)
escribir('index.html','Reumatólogo en León, Gto. | Dr. Daniel Mora Saucedo',desc_home,None,home,[physician,clinica,video,serie]+episodios,cta=False,clase='',preload=True)

# ---------- PADECIMIENTOS: qué es la reumatología + fichas ----------
pad=S['reuma'].replace('<span class="ed-cabecera-num">N.º 02</span>','<span class="ed-cabecera-num">N.º 01</span>')+S['pad']
escribir('padecimientos.html','Padecimientos reumáticos que atiende el Dr. Daniel Mora en León, Gto.','Qué es la reumatología explicado en lenguaje llano, y los padecimientos que atiende el Dr. Daniel Mora en León: artritis reumatoide, lupus, Sjögren, espondiloartritis, vasculitis, gota y más.','Padecimientos',pad,[itemlist,physician_min])

# ---------- CUÁNDO ACUDIR: guía + preguntas ----------
ca=S['guia'].replace('<span class="ed-cabecera-num">N.º 03</span>','<span class="ed-cabecera-num">N.º 01</span>')+S['faq'].replace('<span class="ed-cabecera-num">N.º 04</span>','<span class="ed-cabecera-num">N.º 02</span>')
faq['url']=BASE+'cuando-acudir.html#preguntas'
escribir('cuando-acudir.html','¿Cuándo acudir con un reumatólogo? Señales y preguntas frecuentes | Dr. Daniel Mora, León','Guía de señales por tipo (articulares, sistémicas, cutáneas, oculares y más) y respuestas a las dudas de siempre. Si reconoces alguna, agenda valoración con el Dr. Daniel Mora en León, Gto.','¿Cuándo acudir?',ca,[faq,physician_min])

# ---------- CONSULTORIO Y CONTACTO ----------
cc=S['consultorio']+S['contacto']
escribir('contacto.html','Consultorio y contacto | Dr. Daniel Mora, reumatólogo en Médica Campestre, León','Agenda por WhatsApp al 477 401 1085 o llama al 477 717 3939. Torre Médica Campestre I, Calle Manantial 114, consultorio 107, León, Gto. Horarios, mapa, fotos y redes.','Consultorio y contacto',cc,[clinica,physician],cta=False)

# ---------- borrar páginas agrupadas ----------
for f in ['sobre-mi.html','reumatologia.html','sintomas.html','videos.html','podcast.html','consultorio.html','preguntas.html']:
    os.remove(f); print('eliminada',f)
