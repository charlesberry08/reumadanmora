#!/usr/bin/env python3
"""Genera las imágenes Open Graph (1200×630) de cada página a partir de
herramientas/og/plantilla.html, renderizada con Chrome sin ventana a 2×.

Uso: con el dev-server corriendo en :4328,
    python3 herramientas/generar-og.py            # genera images/og/*.jpg y actualiza las etiquetas
"""
import os, re, subprocess, sys, tempfile, urllib.parse, glob
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'herramientas'))
from padecimientos import PADECIMIENTOS

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SERVIDOR = 'http://localhost:4328/herramientas/og/plantilla.html'
BASE = 'https://www.reumadanmora.com/'
SALIDA = os.path.join(RAIZ, 'images', 'og')

PAGINAS = [
    dict(slug='inicio', archivo='index.html', tipo='inicio',
         eyebrow='Reumatólogo en León, Gto.', titulo='<em>Dr.</em> Daniel Mora',
         sub='Diagnóstico temprano, oportuno y tratamiento integral de enfermedades reumáticas y autoinmunes.',
         alt='Dr. Daniel Mora, reumatólogo en León, Guanajuato'),
    dict(slug='padecimientos', archivo='padecimientos.html',
         eyebrow='Padecimientos que atiende', titulo='Enfermedades reumáticas y <em>autoinmunes</em>',
         sub='Artritis reumatoide, lupus, enfermedad de Sjögren, espondiloartritis, vasculitis, etc.',
         alt='Padecimientos reumáticos que atiende el Dr. Daniel Mora en León'),
    dict(slug='cuando-acudir', archivo='cuando-acudir.html',
         eyebrow='Guía para el paciente', titulo='¿Cuándo acudir con un <em>reumatólogo</em>?',
         sub='Señales por tipo y respuestas a las dudas de siempre.',
         alt='Cuándo acudir con un reumatólogo: guía del Dr. Daniel Mora'),
    dict(slug='contacto', archivo='contacto.html',
         eyebrow='Consultorio y citas', titulo='Un espacio tranquilo en <em>Médica Campestre</em>',
         sub='Calle Manantial 114, consultorio 107. Lunes, miércoles y viernes. Citas por WhatsApp.',
         alt='Consultorio del Dr. Daniel Mora en Médica Campestre, León'),
    dict(slug='aviso-de-privacidad', archivo='aviso-de-privacidad.html',
         eyebrow='Protección de datos', titulo='Aviso de <em>privacidad</em>',
         sub='Qué datos usamos, para qué y cómo ejercer tus derechos ARCO.',
         alt='Aviso de privacidad del consultorio del Dr. Daniel Mora'),
    dict(slug='404', archivo='404.html',
         eyebrow='Página no encontrada', titulo='Esta página se fue a <em>consulta</em>',
         sub='', alt='Dr. Daniel Mora, reumatólogo en León'),
]
for p in PADECIMIENTOS:
    nombre = p['nombre']
    # Cursiva en la última palabra del nombre para seguir el estilo editorial
    partes = nombre.rsplit(' ', 1)
    titulo = f'{partes[0]} <em>{partes[1]}</em>' if len(partes) == 2 else nombre
    PAGINAS.append(dict(slug=p['slug'], archivo=f"{p['slug']}.html",
                        eyebrow='Señales, diagnóstico y tratamiento', titulo=titulo,
                        sub=p.get('sub') or '', alt=f'{nombre}: atención con el Dr. Daniel Mora, reumatólogo en León'))


def renderizar(pag, destino):
    q = urllib.parse.urlencode({k: pag.get(k, '') for k in ('eyebrow', 'titulo', 'sub', 'tipo') if pag.get(k)})
    with tempfile.TemporaryDirectory() as perfil:
        png = os.path.join(perfil, 'captura.png')
        subprocess.run([CHROME, '--headless=new', '--no-first-run', '--disable-gpu', f'--user-data-dir={perfil}',
                        '--hide-scrollbars', '--window-size=1200,630', '--force-device-scale-factor=2',
                        '--virtual-time-budget=4000', f'--screenshot={png}', f'{SERVIDOR}?{q}'],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        im = Image.open(png).convert('RGB').resize((1200, 630), Image.LANCZOS)
        im.save(destino, 'JPEG', quality=86, optimize=True, progressive=True)


def actualizar_etiquetas(pag):
    ruta = os.path.join(RAIZ, pag['archivo'])
    s = open(ruta, encoding='utf-8').read()
    url = f"{BASE}images/og/{pag['slug']}.jpg"
    s = re.sub(r'(property="og:image(?::secure_url)?" content=")[^"]*', lambda m: m.group(1) + url, s)
    s = re.sub(r'(name="twitter:image" content=")[^"]*', lambda m: m.group(1) + url, s)
    s = re.sub(r'(property="og:image:alt" content=")[^"]*', lambda m: m.group(1) + pag['alt'], s)
    s = re.sub(r'(name="twitter:image:alt" content=")[^"]*', lambda m: m.group(1) + pag['alt'], s)
    open(ruta, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True)
    solo = sys.argv[1:]  # slugs opcionales
    for pag in PAGINAS:
        if solo and pag['slug'] not in solo:
            continue
        destino = os.path.join(SALIDA, f"{pag['slug']}.jpg")
        renderizar(pag, destino)
        if os.path.exists(os.path.join(RAIZ, pag['archivo'])):
            actualizar_etiquetas(pag)
        print(f"og/{pag['slug']}.jpg  {os.path.getsize(destino)//1024} KB")
