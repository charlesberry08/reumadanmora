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

Isotipo "articulación": dos barras blancas con remate redondo que forman un ángulo abierto (como una rodilla o un dedo flexionado) y un nodo ámbar con anillo blanco en el vértice, sobre un cuadrado con radio 25 % relleno del gradiente de marca. Archivos en `images/marca/`: `icono.svg` (isotipo), `logo.svg` (isotipo + wordmark "Dr. Daniel Mora / REUMATOLOGÍA"), `icono-512.png`. Favicon y apple-touch-icon generados del mismo SVG.

Reglas: no cambiar el color del nodo, no cerrar el ángulo, no usar el isotipo sin el gradiente sobre fondos claros.

## Bento

Retícula de 12 columnas (`.bento`), tiles con radio 20px (`.tile`) y spans `.c-3 … .c-12`, `.r-2`. A ≤980px la retícula pasa a 6 columnas y a ≤640px a una sola. Un bloque saturado (`.tile-marca`) y un bloque de tinte (`.tile-menta`) por sección como máximo.

## Imágenes

`images/web/` son las versiones optimizadas que usa el sitio (máx. 1800px). Las originales (4032px, 3–4 MB) y el PSD del retrato se conservan en `images/`. `og-consultorio.jpg` es la imagen para redes (1200×630).
