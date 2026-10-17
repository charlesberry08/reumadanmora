#!/usr/bin/env python3
"""Genera subtítulos .ass (estilo reel: frases cortas, palabra activa resaltada) a partir de las
transcripciones de mlx-whisper (JSON con word_timestamps) de cada clip, desplazadas al tiempo del reel.

Uso: subtitulos.py salida.ass clip1.json:INICIO1 clip2.json:INICIO2 ...
  INICIO = segundo en el que ese clip empieza dentro del reel (lo imprime armar-reel.sh como "inicios").
Quemar: ffmpeg -i reel.mp4 -vf "ass=salida.ass:fontsdir=<carpeta con Manrope-ExtraBold.ttf>" -c:a copy out.mp4
"""
import json, re, sys

ANCHO, ALTO = 1080, 1920
MAX_CHARS = 22          # por línea
MAX_LINEAS = 2
MAX_PALABRAS = 6        # por frase en pantalla
PAUSA_CORTE = 0.6       # un silencio mayor cierra la frase
MARGEN_INF = 760        # px desde abajo → la frase queda arriba de la zona de la pleca (y≈1160)
COLOR_TEXTO = '&H00FFFFFF'    # blanco (formato ASS: &HAABBGGRR)
COLOR_ACTIVA = '&H00F8D67D'   # celeste de marca #7dd6f8
COLOR_BORDE = '&H00452F1E'    # marino oscuro #1e2f45… (BGR de #1e2f97 → &H00972F1E)
COLOR_BORDE = '&H00972F1E'
COLOR_SOMBRA = '&H80000000'

CABECERA = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {ANCHO}
PlayResY: {ALTO}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Reel,Manrope ExtraBold,78,{COLOR_TEXTO},{COLOR_ACTIVA},{COLOR_BORDE},{COLOR_SOMBRA},-1,0,0,0,100,100,0.5,0,1,6,2,2,70,70,{MARGEN_INF},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def t_ass(s):
    s = max(0.0, s); h = int(s // 3600); m = int(s % 3600 // 60); sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"

def limpiar(w):
    return re.sub(r'\s+', ' ', w).strip()

def frases(palabras):
    """Agrupa palabras en frases cortas (por conteo, longitud, pausas y puntuación)."""
    grupo = []; salida = []
    for i, p in enumerate(palabras):
        grupo.append(p)
        texto = ' '.join(x['word'] for x in grupo)
        fin_puntuacion = p['word'].rstrip().endswith(('.', ',', '?', '!', ':', ';'))
        pausa = i + 1 < len(palabras) and palabras[i + 1]['start'] - p['end'] > PAUSA_CORTE
        lleno = len(grupo) >= MAX_PALABRAS or len(texto) > MAX_CHARS * MAX_LINEAS - 6
        if fin_puntuacion or pausa or lleno or i == len(palabras) - 1:
            salida.append(grupo); grupo = []
    return salida

def partir_lineas(palabras):
    """Reparte las palabras en hasta dos líneas equilibradas."""
    texto = ' '.join(p['word'] for p in palabras)
    if len(texto) <= MAX_CHARS or len(palabras) == 1:
        return [palabras]
    mejor, mejor_dif = 1, 10**9
    for k in range(1, len(palabras)):
        a = len(' '.join(p['word'] for p in palabras[:k])); b = len(' '.join(p['word'] for p in palabras[k:]))
        if max(a, b) <= MAX_CHARS + 4 and abs(a - b) < mejor_dif:
            mejor, mejor_dif = k, abs(a - b)
    return [palabras[:mejor], palabras[mejor:]]

def eventos(palabras, desplazamiento):
    lineas_out = []
    for grupo in frases(palabras):
        lineas = partir_lineas(grupo)
        ini = grupo[0]['start'] + desplazamiento
        fin = grupo[-1]['end'] + desplazamiento + 0.15
        # un evento por palabra activa: toda la frase visible, la palabra en curso en celeste
        for idx, p in enumerate(grupo):
            a = p['start'] + desplazamiento if idx else ini
            b = grupo[idx + 1]['start'] + desplazamiento if idx + 1 < len(grupo) else fin
            if b - a < 0.05: continue
            partes = []
            n = 0
            for linea in lineas:
                ws = []
                for w in linea:
                    txt = limpiar(w['word'])
                    ws.append(f"{{\\c{COLOR_ACTIVA}}}{txt}{{\\c{COLOR_TEXTO}}}" if n == idx else txt)
                    n += 1
                partes.append(' '.join(ws))
            texto = '\\N'.join(partes)
            lineas_out.append(f"Dialogue: 0,{t_ass(a)},{t_ass(b)},Reel,,0,0,0,,{texto}")
    return lineas_out

def main():
    salida = sys.argv[1]; fuentes = sys.argv[2:]
    out = [CABECERA]
    total = 0
    for item in fuentes:
        ruta, ini = item.rsplit(':', 1)
        datos = json.load(open(ruta))
        palabras = [{'word': w['word'], 'start': float(w['start']), 'end': float(w['end'])}
                    for s in datos['segments'] for w in s.get('words', []) if limpiar(w['word'])]
        ev = eventos(palabras, float(ini)); total += len(ev); out += ev
    open(salida, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(f"{salida}: {total} eventos")

if __name__ == '__main__':
    main()
