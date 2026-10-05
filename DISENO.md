# Lenguaje de diseño — Dr. Daniel Mora · Reumatología

Rediseño 2026-10-05 (CB.Design). Base clara, tinta navy, paleta de marca solo en bloques y acentos, composición bento.

## Paleta

| Token | Valor | Uso |
|---|---|---|
| `--fondo` | `#f4f7f8` | Fondo de página |
| `--tarjeta` | `#ffffff` | Tiles |
| `--tinta` | `#0f1f2e` | Texto principal (navy) |
| `--tinta-suave` | `#56687a` | Texto secundario |
| `--borde` | `#e2e9ec` | Bordes |
| `--salvia` | `#5fa896` | Color de marca, tomado de la pared del consultorio |
| `--salvia-tinta` | `#2f7f70` | Enlaces y etiquetas sobre blanco (contraste AA) |
| `--petroleo` | `#0f4c5c` | Botón primario, fin del gradiente |
| `--petroleo-oscuro` | `#0a3542` | Hover, títulos dentro de tintes |
| `--menta` | `#e3f1ed` | Bloque de tinte (máx. uno por sección) |
| `--ambar` | `#e2a85f` | Acento cálido: nodo del logo, cifra destacada |
| `--grad-marca` | salvia → `#2a7a7c` → petróleo (135°) | Bloque saturado (héroe y contacto), texto blanco |

Tipografía: Manrope (400–800), títulos 800 con tracking −0.02em. Iconos Font Awesome 6.

## Logo

Isotipo "anticuerpo" (referencia: inmunoglobulina en Y, elegida por Carlos el 2026-10-05). Dos cadenas pesadas blancas que suben desde el tallo y se abren en Y, y dos cadenas ligeras ámbar paralelas por fuera de cada brazo; remates redondos, sobre un cuadrado con radio 25 % relleno del gradiente de marca. Archivos en `images/marca/`: `icono.svg` (isotipo), `logo.svg` (isotipo + wordmark "Dr. Daniel Mora / REUMATOLOGÍA"), `icono-512.png`. Favicon y apple-touch-icon generados del mismo SVG. En el sitio las cadenas ligeras "respiran" (opacidad) y aceleran al pasar el cursor.

Reglas: las cadenas ligeras siempre en ámbar y por fuera; no cerrar los brazos ni separar los tallos; no usar el isotipo sin el gradiente sobre fondos claros.

## Bento

Retícula de 12 columnas (`.bento`), tiles con radio 20px (`.tile`) y spans `.c-3 … .c-12`, `.r-2`. A ≤980px la retícula pasa a 6 columnas y a ≤640px a una sola. Un bloque saturado (`.tile-marca`) y un bloque de tinte (`.tile-menta`) por sección como máximo.

## Imágenes

`images/web/` son las versiones optimizadas que usa el sitio (máx. 1800px). Las originales (4032px, 3–4 MB) y el PSD del retrato se conservan en `images/`. `og-consultorio.jpg` es la imagen para redes (1200×630).

## Movimiento

Aparición escalonada de los tiles (`--retraso` por posición en la retícula), cinta de padecimientos en desplazamiento continuo (se pausa al pasar el cursor), contador animado en la cifra del héroe, latido del nodo ámbar del logo, resplandor flotante en los bloques saturados, brillo en botones, acercamiento de fotos y onda en el botón de reproducir. Todo se desactiva con `prefers-reduced-motion`.

## Videos y redes

El contenido se captura en el bloque `CONFIGURACIÓN DE CONTENIDO` al inicio del script de `index.html`: `REDES` (URL y usuario por red) y `VIDEOS` (id de YouTube, título y tema). Los videos usan una fachada ligera: se muestra la portada y el iframe de YouTube (`youtube-nocookie`) solo se carga al dar clic. Sin id, el tile muestra "Próximamente"; sin URL de red, la tarjeta no enlaza y el icono del pie de página se oculta.
