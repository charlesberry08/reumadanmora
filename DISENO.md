# Lenguaje de diseño — Dr. Daniel Mora · Reumatología

Rediseño 2026-10-05 (CB.Design). Base clara, tinta navy, paleta de marca solo en bloques y acentos, composición bento.

## Paleta

Referencia entregada por Carlos (2026-10-05): cinco tonos de azul.

| Token | Valor | Uso |
|---|---|---|
| `--fondo` | `#f3f7fc` | Fondo de página |
| `--tarjeta` | `#ffffff` | Tiles |
| `--tinta` | `#121a45` | Texto principal (navy) |
| `--tinta-suave` | `#5a6487` | Texto secundario |
| `--borde` | `#e2e8f3` | Bordes |
| `--cielo` | `#7dd6f8` | Punta de las cadenas ligeras, gradiente claro |
| `--lavanda` | `#797ef6` | Base de las cadenas ligeras, acento |
| `--turquesa` | `#4adfdd` | Punta de las cadenas pesadas; etiquetas sobre el bloque saturado |
| `--azul` | `#1aa7ec` | Color de marca: puntos, iconos, inicio del gradiente |
| `--marino` | `#1e2f97` | Botón primario, fin del gradiente, tallo del isotipo |
| `--azul-tinta` | `#0b6fb0` | Enlaces y etiquetas sobre blanco (contraste AA) |
| `--lavanda-tinta` | `#5559d6` | Cifra destacada sobre blanco |
| `--celeste` | `#e9f6fd` | Bloque de tinte (máx. uno por sección) |
| `--grad-marca` | azul → `#2457c4` → marino (135°) | Bloque saturado (héroe y contacto), texto blanco |
| `--grad-suave` | cielo → lavanda | Iconos al pasar el cursor |

Tipografía: Manrope (400–800), títulos 800 con tracking −0.02em. Iconos Font Awesome 6.

## Logo

Isotipo "anticuerpo" **sin contenedor** (Carlos rechazó el recuadro el 2026-10-05). Inmunoglobulina en Y, vertical (Carlos pidió quitar la inclinación): dos cadenas pesadas con tallo recto, codo curvo y brazo, en gradiente marino → azul → turquesa de abajo hacia arriba; dos cadenas ligeras más cortas por fuera de cada brazo, flotando con un hueco, en gradiente lavanda → cielo. Remates redondos y un filo de luz blanco al 42 % en cada tubo para dar volumen. Archivos en `images/marca/`: `icono.svg` (color), `icono-blanco.svg` (monocromo para fondos saturados), `logo.svg` (isotipo + wordmark "Dr. Daniel Mora / REUMATOLOGÍA"), `icono-512.png` y `apple-touch-icon.png` (versión blanca sobre cuadrado azul → marino, solo para iconos de app) y `muestra.html` y `muestra-logo.jpg` (hoja de muestra). En el sitio las cadenas ligeras "respiran" (opacidad) y aceleran al pasar el cursor.

Reglas: nunca meter el isotipo en un recuadro; mantenerla vertical y conservar el hueco entre cadenas; sobre fondos saturados usar la versión blanca; no recolorear los gradientes.

## Bento

Retícula de 12 columnas (`.bento`), tiles con radio 20px (`.tile`) y spans `.c-3 … .c-12`, `.r-2`. A ≤980px la retícula pasa a 6 columnas y a ≤640px a una sola. Un bloque saturado (`.tile-marca`) y un bloque de tinte (`.tile-menta`) por sección como máximo.

## Imágenes

`images/web/` son las versiones optimizadas que usa el sitio (máx. 1800px). Las originales (4032px, 3–4 MB) y el PSD del retrato se conservan en `images/`. `og-consultorio.jpg` es la imagen para redes (1200×630).

## Movimiento

Aparición escalonada de los tiles (`--retraso` por posición en la retícula), cinta de padecimientos en desplazamiento continuo (se pausa al pasar el cursor), contador animado en la cifra del héroe, latido del nodo ámbar del logo, resplandor flotante en los bloques saturados, brillo en botones, acercamiento de fotos y onda en el botón de reproducir. Todo se desactiva con `prefers-reduced-motion`.

## Videos, podcast y redes

El contenido se captura en el bloque `CONFIGURACIÓN DE CONTENIDO` al inicio del script de `index.html`: `REDES` (URL y usuario por red), `VIDEOS` (id de YouTube, título y tema) y `PODCAST` (nombre, url, portada, descripción y episodios con id, número y título; el primero de la lista se muestra en grande). El podcast del doctor es **Articulación Sonora** (YouTube @articulacionsonora1860) y tiene su sección propia, separada de Videos. Los videos usan una fachada ligera: se muestra la portada y el iframe de YouTube (`youtube-nocookie`) solo se carga al dar clic. Sin id, el tile muestra "Próximamente"; sin URL de red, la tarjeta no enlaza y el icono del pie de página se oculta.

## Retrato del doctor

**Desde 2026-10-06 el héroe usa la foto a color del doctor recortada y montada sobre el degradado de marca** (`images/web/doctor-hero.jpg` y WebP 600/900/1200, 1200×1300; original en `images/doctor-color-original.jpg`). Se compone con PIL: máscara de sujeto de Vision (sin banda de luminancia, para no traer halo del fondo gris), lienzo con `--grad-marca` a 135° y resplandor turquesa, silueta fantasma del propio doctor al 26 % de opacidad en marino (eco de la composición que él mandó) y la figura anclada abajo. Tile `.retrato-foto` con oscurecido inferior fuerte y la ficha editorial encima. Lo que sigue describe el recorte en blanco y negro anterior, que se conserva en `images/web/doctor-bn*.webp` por si se vuelve a usar.

El héroe usa `images/web/doctor-bn.png`: el retrato **en blanco y negro** (Carlos descartó el duotono azul) recortado sin fondo. La máscara se obtiene con Vision de macOS (`VNGenerateForegroundInstanceMaskRequest`) y se refina en el borde del cabello con una banda de luminancia contra el fondo gris, para no perder mechones. La figura va **sin contenedor**, anclada abajo y contenida en la altura del héroe (altura 100 %; con más se metía bajo la barra de navegación y se cortaba el cabello), con sombra proyectada. Un oscurecido inferior neutro recortado a la silueta (`mask` con el mismo PNG) permite leer la ficha.

**Ficha editorial** (`.ficha`): etiqueta en Manrope mayúsculas con tracking amplio en cielo, nombre en **Fraunces** 500 a dos líneas con el "Dr." en itálica cielo, regla fina de 44px y cédulas en Manrope pequeña con separador en cielo. Fraunces solo se usa para este nombre.

## Espacios para imágenes

Once huecos repartidos en el sitio (3 en Sobre el doctor, 2 en ¿Qué es la reumatología?, 2 en Padecimientos, 1 en Síntomas, 2 en Consultorio, 1 en Contacto), como `<figure class="tile tile-foto tile-imagen …">`. Se llenan con atributos: `data-imagen` (ruta, ideal en `images/web/`, máx. 1800px), `data-alt` (texto alternativo) y opcionalmente `data-pie` / `data-pie2` (pie de foto). Sin `data-imagen` el tile muestra "Espacio para imagen" con la sugerencia de qué fotografiar (`data-sugerencia`). El primero ya tiene la foto a color del doctor (`doctor-color.jpg`).

## SEO y motores de IA (2026-10-06)

- `<head>`: título de 51 caracteres con la intención principal ("Reumatólogo en León, Gto."), descripción ≤160, canónico y hreflang `es-MX` con `www`, robots con `max-snippet/-image-preview/-video-preview`, meta geo (21.1504, -101.6878, MX-GUA), Open Graph y Twitter completos con dimensiones de imagen, preload del retrato y dns-prefetch a YouTube.
- Datos estructurados (un solo grafo JSON-LD con `@id`): WebSite, WebPage (con `speakable` para asistentes de voz/IA), ImageObject, BreadcrumbList, Physician+Person (cédulas como `hasCredential`, `alumniOf`, `knowsAbout`, `sameAs` a Instagram y YouTube, horario, geo, contactos), MedicalClinic (Médica Campestre, CP 37180), ItemList de MedicalCondition con `signOrSymptom`, FAQPage (8 preguntas tomadas del contenido visible), VideoObject (presentación, fecha 2022-01-04, 34 s), PodcastSeries + 5 PodcastEpisode.
- Semántica: un solo `h1`, `h2` por sección, `<main>`, alt de imágenes con entidad y lugar, `rel="noopener noreferrer"` en externos, dirección y cédulas en el pie.
- Archivos: `robots.txt` (permite GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc. y bloquea archivos internos), `sitemap.xml` (con imágenes y video), `llms.txt` (ficha para motores de IA con datos verificables y cómo citar), `.htaccess` (301 a https+www, compresión, caché, cabeceras).
- Al publicar: enviar el sitemap en Google Search Console y Bing Webmaster, crear/reclamar el Perfil de Negocio de Google con la misma dirección y horario, y verificar los datos con la prueba de resultados enriquecidos de Google.

## Rendimiento y estructura (2026-10-06, segunda ronda SEO)

- **Fuentes propias** en `fonts/` (Manrope y Fraunces variables, subconjunto latin, `font-display: swap`, precargadas). Ya no se carga Google Fonts.
- **Iconos sin Font Awesome**: `images/marca/iconos.svg` es un sprite con los 33 iconos usados (Font Awesome Free, CC BY 4.0). El marcado sigue siendo `<i class="fa-solid fa-nombre">` y `js/comun.js` lo convierte en `<svg class="ico-svg"><use href="…#nombre">`. Para usar un icono nuevo: bajar su SVG de Font Awesome y agregar el `<symbol>` al sprite.
- **Imágenes WebP responsivas** en `images/web/*-600/-1200/-1800.webp` y `*-full.webp` (retratos con transparencia). Los `<img>` llevan `srcset`/`sizes`; los espacios de imagen cargan `-full.webp` y caen al original si no existe. Para una foto nueva: dejar el JPG en `images/web/` y generar sus WebP (script en el historial o PIL).
- **`js/comun.js`**: iconos, menú, aparición, contador, índice de la guía, espacios de imagen y fachada de YouTube, compartido por todas las páginas. `index.html` solo conserva la configuración (REDES, VIDEOS, PODCAST) y `window.renderPagina`.
- **Páginas de padecimientos** (`artritis-reumatoide.html`, `lupus.html`, `sindrome-de-sjogren.html`, `espondiloartritis.html`, `vasculitis.html`): se generan con `python3 herramientas/generar-padecimientos.py` a partir de `herramientas/padecimientos.py` (texto en tono llano; el doctor debe revisarlo). Cada una lleva MedicalWebPage + MedicalCondition + FAQPage + migas, `lastReviewed` con la fecha de generación, y enlaza a las demás.
- **Preguntas frecuentes visibles** (`#preguntas`, N.º 04) alineadas una a una con el FAQPage del JSON-LD de la portada.
- **Accesibilidad**: enlace "Ir al contenido", `<main id="contenido">`, foco visible, números decorativos con contraste ≥ 4.5:1, `aria-current` en migas.
- **404.html** propia (noindex) con enlaces útiles; `.htaccess` la sirve como ErrorDocument.

## Estructura del sitio (2026-10-06, acordada con Carlos)

Objetivo del doctor: "que la gente me encuentre en internet". Cuatro páginas, cada una para una intención de búsqueda, más cinco páginas por padecimiento:

| Página | Qué contiene | Búsqueda a la que responde |
|---|---|---|
| `index.html` | Héroe con retrato, datos rápidos, cinta, perfil editorial del doctor (#sobre-mi), tres accesos, videos (#videos), podcast (#podcast), contacto corto | "reumatólogo en León", "Dr. Daniel Mora" |
| `padecimientos.html` | ¿Qué es la reumatología? (#reumatologia) + fichas de padecimientos; de aquí cuelgan `artritis-reumatoide`, `lupus`, `sindrome-de-sjogren`, `espondiloartritis`, `vasculitis` | "qué atiende un reumatólogo", cada enfermedad + León |
| `cuando-acudir.html` | Guía de señales por tipo con índice fijo + preguntas frecuentes (#preguntas) | "cuándo ir al reumatólogo", "síntomas de…" |
| `contacto.html` | Fotos del consultorio (#consultorio), cómo llegar, horarios, WhatsApp, mapa y redes (#redes) | "consultorio", "cita", "Médica Campestre" |

Menú: El doctor · Padecimientos · ¿Cuándo acudir? · Consultorio y contacto + botón Agendar. El menú móvil y el pie añaden ¿Qué es la reumatología?, Preguntas frecuentes, Videos y podcast y Aviso de privacidad.

- `herramientas/agrupar-paginas.py` hizo la agrupación una vez (no volver a correrlo). Las páginas se editan directo; las de padecimientos se regeneran con `generar-padecimientos.py`, que toma barra y pie de `index.html`.
- `.htaccess` redirige con 301 las rutas que existieron brevemente (sobre-mi, reumatologia, sintomas, preguntas, videos, podcast, consultorio).
- `js/contenido.js`: redes, videos y podcast. `js/comun.js`: comportamiento común.

## Precarga de marca

Cortina clara con el isotipo dibujándose trazo a trazo (cadenas pesadas y luego ligeras, con los gradientes de marca), el nombre que sube y "REUMATOLOGÍA" que se abre; una barra de progreso fina abajo. Dura 3.2 s como mínimo y 4.8 s como máximo, se retira cuando la página terminó de cargar, y **solo se muestra una vez por visita** (bandera en `sessionStorage`; un script en `<head>` añade `html.sin-precarga` para que las páginas siguientes no la muestren ni parpadeen). Con `prefers-reduced-motion` no aparece. Marcado `#precarga` al inicio del `<body>` de cada página (lo incluye también el generador de padecimientos); estilos en la sección "Precarga de marca" de `styles.css`; lógica en `js/comun.js`.

## Móvil y tableta (auditoría 2026-10-06)

Se auditaron las once páginas a 375, 768 y 1024 px con un script que busca desbordes horizontales, elementos fuera del viewport, zonas táctiles menores a 40 px y textos menores a 11.5 px. Ajustes: rótulos con tamaño mínimo legible, enlaces de texto con área táctil ≥ 40 px (pie, migas, teléfonos, "leer más", índice de la guía, acordeón), tiles de dato, redes y episodios del podcast a dos por fila en teléfonos (una por fila por debajo de 340 px), índice de la guía a dos columnas en tableta, fichas de padecimientos a dos por fila en tableta, títulos del héroe y de página reducidos en teléfonos. La cinta de padecimientos es el único elemento que sale del viewport, por diseño.

## Menú móvil

Panel lateral (`#mobile-drawer`) con el sistema del sitio: cabecera con isotipo y wordmark bajo doble filete, cuatro páginas principales numeradas en Fraunces itálica con filetes (la página actual en marino y azul), grupo "También" con iconos para las secciones secundarias, bloque saturado con horario, botón de WhatsApp y teléfono, y redes al pie. Los elementos entran escalonados. El panel y el velo se mueven al `body` al cargar (la barra tiene backdrop-filter) y el bloqueo de scroll se aplica en `html`. Si cambia el menú, editar el `<aside id="mobile-drawer">` en cada página (o en index.html y regenerar las de padecimientos).
