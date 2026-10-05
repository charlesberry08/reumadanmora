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

## Videos y redes

El contenido se captura en el bloque `CONFIGURACIÓN DE CONTENIDO` al inicio del script de `index.html`: `REDES` (URL y usuario por red) y `VIDEOS` (id de YouTube, título y tema). Los videos usan una fachada ligera: se muestra la portada y el iframe de YouTube (`youtube-nocookie`) solo se carga al dar clic. Sin id, el tile muestra "Próximamente"; sin URL de red, la tarjeta no enlaza y el icono del pie de página se oculta.
