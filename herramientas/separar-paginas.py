#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Separa la portada de una sola página en páginas independientes (se corre una vez; después se edita cada página)."""
import re, json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE='https://www.reumadanmora.com/'
h=open('index.html',encoding='utf-8').read()

def bloque(marca, siguiente):
    a=h.index(f'<!-- ============ {marca} ============ -->'); b=h.index(f'<!-- ============ {siguiente} ============ -->')
    return h[a:b]
secciones={
 'sobre': bloque('SOBRE MÍ','QUÉ ES LA REUMATOLOGÍA'),
 'reuma': bloque('QUÉ ES LA REUMATOLOGÍA','PADECIMIENTOS'),
 'padecimientos': bloque('PADECIMIENTOS','SÍNTOMAS (guía editorial)'),
 'sintomas': bloque('SÍNTOMAS (guía editorial)','VIDEOS'),
 'videos': bloque('VIDEOS','PODCAST'),
 'podcast': bloque('PODCAST','CONSULTORIO'),
 'consultorio': bloque('CONSULTORIO','REDES'),
 'redes': bloque('REDES','CONTACTO'),
 'contacto': bloque('CONTACTO','PREGUNTAS FRECUENTES'),
 'preguntas': h[h.index('<!-- ============ PREGUNTAS FRECUENTES ============ -->'):h.index('</main>')],
}
hero=h[h.index('<!-- ============ HERO ============ -->'):h.index('<!-- ============ CINTA ============ -->')]
cinta=h[h.index('<!-- ============ CINTA ============ -->'):h.index('<!-- ============ SOBRE MÍ ============ -->')]
nav=re.search(r'<nav class="topbar".*?</nav>',h,re.S).group(0)
footer=re.search(r'<footer>.*?</footer>',h,re.S).group(0)
head=h[h.index('<head>'):h.index('</head>')+7]
ld=json.loads(re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',h,re.S).group(1))
script=re.search(r'<script>\n  // =====.*?</script>',h,re.S).group(0)

# ---------- js/contenido.js: configuración + render ----------
cuerpo=script[len('<script>\n'):-len('</script>')]
open('js/contenido.js','w',encoding='utf-8').write('/* Contenido configurable del sitio (redes, videos, podcast) y render de esas secciones */\n'+cuerpo)

# ---------- mapa de anclas a páginas ----------
MAPA={'#top':'index.html','#sobre-mi':'sobre-mi.html','#reumatologia':'reumatologia.html','#padecimientos':'padecimientos.html','#sintomas':'sintomas.html','#videos':'videos.html','#podcast':'podcast.html','#consultorio':'consultorio.html','#redes':'contacto.html#redes','#contacto':'contacto.html','#preguntas':'preguntas.html'}
def enlazar(html, propia=None):
    for anc,pag in MAPA.items():
        if propia and pag.split('#')[0]==propia and '#' not in pag[1:]:
            html=html.replace(f'href="{anc}"',f'href="{anc}"')  # misma página: se queda el ancla
        else:
            html=html.replace(f'href="{anc}"',f'href="{pag}"')
    return html

# nav/footer con páginas y menú ajustado
nav=enlazar(nav); footer=enlazar(footer)
nav=nav.replace('<li><a href="videos.html" class="nav-link">Videos</a></li>','<li><a href="videos.html" class="nav-link">Videos</a></li>')
nav=nav.replace('<li><a href="sobre-mi.html" class="drawer-link">Sobre mí</a></li>','<li><a href="sobre-mi.html" class="drawer-link">Sobre mí</a></li>\n      <li><a href="reumatologia.html" class="drawer-link">¿Qué es la reumatología?</a></li>')
footer=footer.replace('<li><a href="sobre-mi.html">Sobre mí</a></li>','<li><a href="sobre-mi.html">Sobre mí</a></li>\n      <li><a href="reumatologia.html">¿Qué es la reumatología?</a></li>')

# ---------- head por página ----------
def head_pagina(archivo, titulo, desc, grafo, og_type='website'):
    url=BASE+archivo if archivo!='index.html' else BASE
    hd=head
    hd=re.sub(r'<title>.*?</title>',f'<title>{titulo}</title>',hd)
    hd=re.sub(r'<meta name="description" content="[^"]*" />',f'<meta name="description" content="{desc}" />',hd)
    hd=hd.replace('<link rel="canonical" href="https://www.reumadanmora.com/" />',f'<link rel="canonical" href="{url}" />')
    hd=hd.replace('<link rel="alternate" hreflang="es-MX" href="https://www.reumadanmora.com/" />',f'<link rel="alternate" hreflang="es-MX" href="{url}" />')
    hd=hd.replace('<link rel="alternate" hreflang="x-default" href="https://www.reumadanmora.com/" />',f'<link rel="alternate" hreflang="x-default" href="{url}" />')
    hd=hd.replace('<meta property="og:url" content="https://www.reumadanmora.com/" />',f'<meta property="og:url" content="{url}" />')
    hd=hd.replace('<meta property="og:type" content="website" />',f'<meta property="og:type" content="{og_type}" />')
    hd=re.sub(r'<meta property="og:title" content="[^"]*" />',f'<meta property="og:title" content="{titulo}" />',hd)
    hd=re.sub(r'<meta property="og:description" content="[^"]*" />',f'<meta property="og:description" content="{desc}" />',hd)
    hd=re.sub(r'<meta name="twitter:title" content="[^"]*" />',f'<meta name="twitter:title" content="{titulo}" />',hd)
    hd=re.sub(r'<meta name="twitter:description" content="[^"]*" />',f'<meta name="twitter:description" content="{desc}" />',hd)
    if archivo!='index.html':
        hd=hd.replace('  <link rel="preload" as="image" href="images/web/doctor-bn-full.webp" type="image/webp" fetchpriority="high" />\n','')
    hd=hd.replace('<script src="js/comun.js?v=2" defer></script>','<script src="js/contenido.js?v=1" defer></script>\n  <script src="js/comun.js?v=2" defer></script>')
    hd=re.sub(r'<script type="application/ld\+json">.*?</script>','<script type="application/ld+json">\n'+json.dumps(grafo,ensure_ascii=False,indent=2)+'\n  </script>',hd,flags=re.S)
    return hd

nodos={ (n['@type'] if isinstance(n['@type'],str) else '/'.join(n['@type'])): n for n in ld['@graph'] }
physician=nodos['Physician/Person']; clinica=nodos['MedicalClinic']; website=nodos['WebSite']; imagen=nodos['ImageObject']
physician_min={"@type":"Physician","@id":BASE+"#physician","name":physician['name'],"url":BASE,"medicalSpecialty":"Rheumatology","telephone":physician['telephone'],"address":physician['address'],"sameAs":physician['sameAs']}
def grafo(archivo, nombre, desc, extra, migas_nombre=None):
    url=BASE+archivo if archivo!='index.html' else BASE
    migas=[{"@type":"ListItem","position":1,"name":"Inicio","item":BASE}]
    if migas_nombre: migas.append({"@type":"ListItem","position":2,"name":migas_nombre,"item":url})
    g=[website,{"@type":"WebPage","@id":url+"#webpage","url":url,"name":nombre,"description":desc,"inLanguage":"es-MX","isPartOf":{"@id":BASE+"#website"},"about":{"@id":BASE+"#physician"},"breadcrumb":{"@id":url+"#migas"},"primaryImageOfPage":{"@id":BASE+"#imagen"}},
       {"@type":"BreadcrumbList","@id":url+"#migas","itemListElement":migas}]+extra
    return {"@context":"https://schema.org","@graph":g}

def cta_final():
    return '''<section class="seccion">
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
def migas_html(nombre):
    return f'''<div class="container"><nav class="migas" aria-label="Ruta"><a href="index.html">Inicio</a><i class="fa-solid fa-play" aria-hidden="true"></i><span aria-current="page">{nombre}</span></nav></div>
'''
def pagina(archivo, titulo, desc, nombre_miga, cuerpo, extra_nodos, cta=True):
    hd=head_pagina(archivo,titulo,desc,grafo(archivo,titulo,desc,extra_nodos,nombre_miga))
    cuerpo=enlazar(cuerpo, archivo)
    html=f'''<!DOCTYPE html>
<html lang="es-MX">
{hd}
<body id="top" data-raiz="" class="pag">
<a class="saltar" href="#contenido">Ir al contenido</a>
{nav}

<main id="contenido">
{migas_html(nombre_miga)}{cuerpo}{cta_final() if cta else ''}</main>

{footer}
</body>
</html>
'''
    open(archivo,'w',encoding='utf-8').write(html); print('página', archivo)

# ---------- páginas ----------
pagina('sobre-mi.html','Dr. Daniel Mora Saucedo, reumatólogo en León | Perfil y formación','Perfil del Dr. Gildardo Daniel Mora Saucedo, reumatólogo certificado en León, Gto.: formación en la UdeG y el Centro Médico Nacional de Occidente, cédulas y forma de trabajar.','Sobre el doctor',secciones['sobre'],[physician])
pagina('reumatologia.html','¿Qué es la reumatología? Explicado sin palabras raras | Dr. Daniel Mora','Qué atiende un reumatólogo, en qué se diferencia del traumatólogo, qué es "tener reumas" y qué pasa en la consulta. Explicado en lenguaje llano por el Dr. Daniel Mora, León, Gto.','¿Qué es la reumatología?',secciones['reuma'],[physician_min])
pagina('padecimientos.html','Padecimientos reumáticos que atiende el Dr. Daniel Mora en León, Gto.','Artritis reumatoide, lupus, Sjögren, espondiloartritis, vasculitis, gota, fibromialgia y más. Señales de cada uno y cuándo acudir con el reumatólogo en León, Guanajuato.','Padecimientos',secciones['padecimientos'],[nodos['ItemList'],physician_min])
pagina('sintomas.html','¿Cuándo acudir con un reumatólogo? Señales por tipo | Dr. Daniel Mora, León','Guía de signos clínicos por tipo: articulares, sistémicos, musculares, cutáneos, oculares y hemato-inmunológicos. Si reconoces alguno, agenda valoración con el Dr. Daniel Mora en León, Gto.','¿Cuándo acudir?',secciones['sintomas'],[physician_min])
pagina('videos.html','Videos del Dr. Daniel Mora, reumatólogo en León | El doctor explica','Videos breves del Dr. Daniel Mora sobre enfermedades reumáticas y la consulta de reumatología en Médica Campestre, León, Guanajuato.','Videos',secciones['videos'],[nodos['VideoObject'],physician_min])
pagina('podcast.html','Articulación Sonora, el podcast del Dr. Daniel Mora | Reumatología en lenguaje claro','Episodios de Articulación Sonora, podcast de divulgación sobre enfermedades reumáticas producido por el Dr. Daniel Mora, reumatólogo en León, Gto.','Podcast',secciones['podcast'],[nodos['PodcastSeries']]+[n for n in ld['@graph'] if n.get('@type')=='PodcastEpisode']+[physician_min])
pagina('consultorio.html','Consultorio del Dr. Daniel Mora en Médica Campestre, León | Cómo llegar','Consultorio de reumatología en Torre Médica Campestre I, Calle Manantial 114, consultorio 107, León, Gto. Fotos, ubicación y horario del Dr. Daniel Mora.','Consultorio',secciones['consultorio'],[clinica,physician_min])
pagina('contacto.html','Agenda tu cita con el Dr. Daniel Mora, reumatólogo en León | Contacto','Agenda por WhatsApp al 477 401 1085 o llama al 477 717 3939. Médica Campestre, León, Gto. Lunes, miércoles y viernes de 10 a 13 y de 18 a 20 h. Redes del doctor.','Contacto',secciones['contacto']+secciones['redes'],[clinica,physician],cta=False)
pagina('preguntas.html','Preguntas frecuentes sobre reumatología y la consulta | Dr. Daniel Mora, León','Respuestas claras: qué es la reumatología, reumatólogo o traumatólogo, qué llevar a la consulta, cuándo acudir, horario y cómo agendar con el Dr. Daniel Mora en León, Gto.','Preguntas frecuentes',secciones['preguntas'],[nodos['FAQPage'],physician_min])

# ---------- portada ----------
explora=[
 ('sobre-mi.html','fa-solid fa-certificate','Sobre el doctor','Formación, cédulas y cómo trabaja. Sin discursos.'),
 ('reumatologia.html','fa-solid fa-circle-info','¿Qué es la reumatología?','Explicado sin palabras raras, para que lo entienda cualquiera.'),
 ('padecimientos.html','fa-solid fa-hand-dots','Padecimientos','Artritis reumatoide, lupus, Sjögren, espondiloartritis, vasculitis y más.'),
 ('sintomas.html','fa-solid fa-list-check','¿Cuándo acudir?','Las señales por tipo. Si reconoces una, ya sabes a quién llamar.'),
 ('videos.html','fa-solid fa-play','Videos','El doctor explica, en corto.'),
 ('podcast.html','fa-solid fa-headphones','Podcast','Articulación Sonora: reumatología para escuchar en el camino.'),
 ('consultorio.html','fa-solid fa-location-dot','Consultorio','Médica Campestre, cómo llegar y cómo se ve por dentro.'),
 ('preguntas.html','fa-solid fa-clipboard-check','Preguntas frecuentes','Las dudas de siempre, sin vueltas.'),
]
cards=''.join(f'''      <a class="tile explora c-3 reveal" href="{u}">
        <span class="ico"><i class="{ic}" aria-hidden="true"></i></span>
        <span class="explora-titulo">{t}</span>
        <span class="explora-texto">{d}</span>
        <span class="explora-ir">Ver <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></span>
      </a>
''' for u,ic,t,d in explora)
contacto_home=secciones['contacto'].replace('<section class="seccion contacto" id="contacto">','<section class="seccion contacto" id="contacto">').replace('''      <div class="tile tile-mapa c-7 reveal">''','''      <div class="tile tile-mapa c-7 reveal" hidden>''')
# en portada: contacto sin mapa ni espacio de imagen (eso vive en contacto.html)
contacto_home=re.sub(r'      <div class="tile tile-mapa c-7 reveal" hidden>.*?</div>\n      <figure class="tile tile-foto tile-imagen c-5 reveal"[^>]*></figure>\n','',contacto_home,flags=re.S)
home=f'''{hero}{cinta}
<!-- ============ EXPLORA ============ -->
<section class="seccion" id="explora">
  <div class="container">
    <div class="seccion-cabecera reveal">
      <span class="etiqueta">Explora el sitio</span>
      <h2>Todo lo que necesitas saber, en su lugar</h2>
      <p>Cada tema tiene su página. Entra directo a lo que te interesa.</p>
    </div>
    <div class="bento">
{cards}    </div>
  </div>
</section>

{contacto_home}'''
home=enlazar(home,'index.html')
grafo_home={"@context":"https://schema.org","@graph":[website,nodos['WebPage'],imagen,nodos['BreadcrumbList'],physician,clinica]}
grafo_home['@graph'][1].pop('hasPart',None)
hd=head_pagina('index.html','Reumatólogo en León, Gto. | Dr. Daniel Mora Saucedo',re.search(r'<meta name="description" content="([^"]*)" />',head).group(1),grafo_home)
html=f'''<!DOCTYPE html>
<html lang="es-MX">
{hd}
<body id="top" data-raiz="">
<a class="saltar" href="#contenido">Ir al contenido</a>
{nav}

<main id="contenido">
{home}</main>

{footer}
</body>
</html>
'''
open('index.html','w',encoding='utf-8').write(html); print('portada reescrita')
