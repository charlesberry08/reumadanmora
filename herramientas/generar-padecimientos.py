#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera las páginas de padecimientos a partir de padecimientos.py, reutilizando la barra y el pie de index.html.
Uso: python3 herramientas/generar-padecimientos.py  (desde la raíz del proyecto)"""
import json, re, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from padecimientos import PADECIMIENTOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
BASE = 'https://www.reumadanmora.com/'
HOY = datetime.date.today().isoformat()
index = open('index.html', encoding='utf-8').read()
nav = re.search(r'<nav class="topbar".*?</nav>', index, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', index, re.S).group(0)
# enlaces de la portada -> index.html#...
nav = nav.replace('href="#top"', 'href="index.html"').replace('href="#', 'href="index.html#')
footer = footer.replace('href="#top"', 'href="index.html"').replace('href="#', 'href="index.html#')
# ids de gradiente únicos por página se mantienen (gm-nav/gm-foot); el pie no debe repetir el listado de redes dinámico
footer = footer.replace('<ul class="footer-redes" id="footer-redes"></ul>', '')
version = re.search(r'styles\.css\?v=([\w]+)', index).group(1)

def pagina(p):
    otros = [q for q in PADECIMIENTOS if q['slug'] != p['slug']]
    en_corto = ''.join(f'''      <div class="tile reuma-dato c-4 reveal">
        <span class="reuma-num">{i+1:02d}</span>
        <h3>{t}</h3>
        <p>{d}</p>
      </div>
''' for i, (t, d) in enumerate(p['en_corto']))
    senales = ''.join(f'          <li>{s}</li>\n' for s in p['senales'])
    tuparte = ''.join(f'          <li><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>{s}</span></li>\n' for s in p['tu_parte'])
    faq = ''.join(f'''        <details class="faq-item"{' open' if i == 0 else ''}>
          <summary><span class="faq-num">{i+1:02d}</span><span class="faq-q">{q}</span><i class="fa-solid fa-circle-info" aria-hidden="true"></i></summary>
          <div class="faq-a"><p>{a}</p></div>
        </details>
''' for i, (q, a) in enumerate(p['faq']))
    otros_html = ''.join(f'          <a href="{q["slug"]}.html"><i class="{q["icono"]}" aria-hidden="true"></i> {q["nombre"]}</a>\n' for q in otros)
    url = f'{BASE}{p["slug"]}.html'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "MedicalWebPage", "@id": url + "#webpage", "url": url, "name": p['titulo'], "description": p['descripcion'], "inLanguage": "es-MX",
         "isPartOf": {"@id": BASE + "#website"}, "about": {"@id": url + "#condicion"}, "mainEntity": {"@id": url + "#condicion"},
         "audience": {"@type": "MedicalAudience", "audienceType": "Patient"}, "lastReviewed": HOY, "reviewedBy": {"@id": BASE + "#physician"},
         "author": {"@id": BASE + "#physician"}, "breadcrumb": {"@id": url + "#migas"}, "dateModified": HOY,
         "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".pag-hero h1", ".pag-hero .lead"]}},
        {"@type": "MedicalCondition", "@id": url + "#condicion", "name": p['nombre'], "url": url, "description": p['lead'],
         "signOrSymptom": [{"@type": "MedicalSignOrSymptom", "name": s} for s in p['senales']],
         "possibleTreatment": {"@type": "MedicalTherapy", "name": f"Tratamiento de {p['nombre'].lower()}", "description": p['tratamiento']},
         "typicalTest": {"@type": "MedicalTest", "name": f"Diagnóstico de {p['nombre'].lower()}", "description": p['diagnostico']},
         "relevantSpecialty": "Rheumatology"},
        {"@type": "BreadcrumbList", "@id": url + "#migas", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Padecimientos", "item": BASE + "padecimientos.html"},
            {"@type": "ListItem", "position": 3, "name": p['nombre'], "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]},
        {"@type": "Physician", "@id": BASE + "#physician", "name": "Dr. Gildardo Daniel Mora Saucedo", "url": BASE, "medicalSpecialty": "Rheumatology",
         "telephone": "+52-477-717-3939", "address": {"@type": "PostalAddress", "streetAddress": "Calle Manantial 114, Consultorio 107, Médica Campestre", "addressLocality": "León", "addressRegion": "Guanajuato", "postalCode": "37180", "addressCountry": "MX"}}
    ]}
    return f'''<!DOCTYPE html>
<html lang="es-MX">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="format-detection" content="telephone=no" />
  <meta name="theme-color" content="#1e2f97" />
  <title>{p['titulo']}</title>
  <meta name="description" content="{p['descripcion']}" />
  <meta name="author" content="Dr. Gildardo Daniel Mora Saucedo" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large" />
  <link rel="canonical" href="{url}" />
  <link rel="alternate" hreflang="es-MX" href="{url}" />
  <link rel="alternate" hreflang="x-default" href="{url}" />
  <link rel="preload" as="font" href="fonts/manrope-variable.woff2" type="font/woff2" crossorigin />
  <link rel="preload" as="font" href="fonts/fraunces-variable.woff2" type="font/woff2" crossorigin />
  <script>try{{if(sessionStorage.getItem('precarga'))document.documentElement.classList.add('sin-precarga')}}catch(e){{}}</script>
  <link rel="stylesheet" href="fonts/fuentes.css?v=1" />
  <link rel="stylesheet" href="css/styles.css?v={version}" />
  <script src="js/contenido.js?v=2" defer></script>
  <script src="js/comun.js?v=8" defer></script>
  <link rel="icon" href="images/marca/icono.svg" type="image/svg+xml" />
  <link rel="alternate icon" href="images/favicon.png" type="image/png" />
  <link rel="apple-touch-icon" href="images/apple-touch-icon.png" />
  <meta property="og:type" content="article" />
  <meta property="og:locale" content="es_MX" />
  <meta property="og:site_name" content="Dr. Daniel Mora · Reumatología" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{p['titulo']}" />
  <meta property="og:description" content="{p['descripcion']}" />
  <meta property="og:image" content="{BASE}images/og-consultorio.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{p['titulo']}" />
  <meta name="twitter:description" content="{p['descripcion']}" />
  <meta name="twitter:image" content="{BASE}images/og-consultorio.jpg" />
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body class="pag" data-raiz="">
<a class="saltar" href="#contenido">Ir al contenido</a>
<div id="precarga" aria-hidden="true">
  <div class="precarga-logo">
    <svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="gp-pre" gradientUnits="userSpaceOnUse" x1="50" y1="92" x2="50" y2="22"><stop offset="0" stop-color="#1e2f97"/><stop offset=".55" stop-color="#1aa7ec"/><stop offset="1" stop-color="#4adfdd"/></linearGradient>
        <linearGradient id="gl-pre" gradientUnits="userSpaceOnUse" x1="50" y1="62" x2="50" y2="26"><stop offset="0" stop-color="#797ef6"/><stop offset="1" stop-color="#7dd6f8"/></linearGradient>
      </defs>
      <path class="p1" d="M43 92 V62 C43 54 40 49 35 42 L23 24" stroke="url(#gp-pre)"/>
      <path class="p2" d="M57 92 V62 C57 54 60 49 65 42 L77 24" stroke="url(#gp-pre)"/>
      <path class="l1" d="M30.5 59 L12.5 30" stroke="url(#gl-pre)"/>
      <path class="l2" d="M69.5 59 L87.5 30" stroke="url(#gl-pre)"/>
    </svg>
    <div class="precarga-texto">
      <span class="precarga-nombre">Dr. Daniel Mora</span>
      <span class="precarga-sub">Reumatología</span>
    </div>
  </div>
  <div class="precarga-barra"></div>
</div>
{nav}

<main id="contenido">
<header class="hero">
  <div class="container">
    <nav class="migas" aria-label="Ruta">
      <a href="index.html">Inicio</a><i class="fa-solid fa-play" aria-hidden="true"></i>
      <a href="padecimientos.html">Padecimientos</a><i class="fa-solid fa-play" aria-hidden="true"></i>
      <span aria-current="page">{p['nombre']}</span>
    </nav>
  </div>
  <div class="container bento" style="margin-top:16px">
    <div class="tile tile-marca pag-hero c-7 r-2 reveal">
      <span class="ico"><i class="{p['icono']}" aria-hidden="true"></i></span>
      <span class="etiqueta">Padecimiento · Reumatología en León, Gto.</span>
      <h1>{p['h1']}</h1>
      <p class="pag-sub">{p['sub']}</p>
      <p class="lead">{p['lead']}</p>
      <div class="acciones">
        <a href="https://wa.me/524774011085?text=Hola%20doctor,%20quisiera%20agendar%20una%20cita%20por%20{p['nombre'].replace(' ', '%20')}" class="btn btn-blanco" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i> Agendar valoración</a>
        <a href="#senales" class="btn btn-fantasma"><i class="fa-solid fa-list-check" aria-hidden="true"></i> Ver las señales</a>
      </div>
    </div>
    <figure class="tile tile-foto tile-imagen c-5 r-2 reveal" data-imagen="" data-alt="" data-sugerencia="Imagen relacionada con {p['nombre'].lower()}: articulación afectada, exploración o paciente en consulta"></figure>
  </div>
</header>

<section class="seccion">
  <div class="container">
    <div class="ed-cabecera ed-cabecera-seccion reveal">
      <span>En corto</span>
      <span class="ed-cabecera-num">N.º 01</span>
      <span>Tres cosas que conviene saber</span>
    </div>
    <div class="bento">
{en_corto}    </div>
  </div>
</section>

<section class="seccion" id="senales">
  <div class="container">
    <div class="ed-cabecera ed-cabecera-seccion reveal">
      <span>Señales, diagnóstico y tratamiento</span>
      <span class="ed-cabecera-num">N.º 02</span>
      <span>Lo que hace el reumatólogo</span>
    </div>
    <div class="bento">
      <div class="tile pag-bloque c-6 reveal">
        <span class="etiqueta">Señales frecuentes</span>
        <h2>¿Cómo se siente?</h2>
        <ul class="pag-senales">
{senales}        </ul>
      </div>
      <div class="tile pag-bloque c-6 reveal">
        <span class="etiqueta">Diagnóstico</span>
        <h2>¿Cómo se confirma?</h2>
        <p>{p['diagnostico']}</p>
        <span class="etiqueta" style="margin-top:8px">Tratamiento</span>
        <h2>¿Cómo se trata?</h2>
        <p>{p['tratamiento']}</p>
      </div>
      <div class="tile tile-tinte pag-bloque c-7 reveal">
        <span class="etiqueta">Tu parte</span>
        <h2>Lo que sí depende de ti</h2>
        <ul class="pag-tuparte">
{tuparte}        </ul>
      </div>
      <div class="tile pad-cta c-5 reveal">
        <h3>¿Te suena? Agenda una valoración</h3>
        <p>Trae tus estudios previos y la lista de lo que tomas. Si aún no tienes estudios, el doctor te indica cuáles hacer.</p>
        <a href="https://wa.me/524774011085?text=Hola%20doctor,%20quisiera%20agendar%20una%20cita" class="btn btn-primario" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i> Agendar por WhatsApp</a>
        <p class="pag-nota-medica">Información de divulgación general; no sustituye la valoración médica. Contenido elaborado para el consultorio del Dr. Gildardo Daniel Mora Saucedo, reumatólogo (céd. esp. 10508486).</p>
      </div>
    </div>
  </div>
</section>

<section class="seccion" id="preguntas">
  <div class="container">
    <div class="ed-cabecera ed-cabecera-seccion reveal">
      <span>Preguntas frecuentes</span>
      <span class="ed-cabecera-num">N.º 03</span>
      <span>Sobre {p['nombre'].lower() if p['slug'] != 'sindrome-de-sjogren' else 'el síndrome de Sjögren'}</span>
    </div>
    <div class="bento">
      <div class="tile faq-lista c-8 reveal">
{faq}      </div>
      <div class="tile pag-bloque c-4 reveal">
        <span class="etiqueta">Otros padecimientos</span>
        <h3>También te puede interesar</h3>
        <div class="pag-otros">
{otros_html}          <a href="padecimientos.html"><i class="fa-solid fa-list-check" aria-hidden="true"></i> Todos los padecimientos</a>
        </div>
        <p class="pag-revision">Última revisión del contenido: {HOY}.</p>
      </div>
    </div>
  </div>
</section>
</main>

{footer}
</body>
</html>
'''

for p in PADECIMIENTOS:
    open(f'{p["slug"]}.html', 'w', encoding='utf-8').write(pagina(p))
    print('generado', p['slug'] + '.html')
