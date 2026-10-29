#!/usr/bin/env python3
"""Inserta videos de apoyo (B-roll) a pantalla completa sobre el reel, en los momentos indicados,
con fundido de entrada/salida y un acercamiento suave. El audio del reel no se toca.

Uso: broll.py reel.mp4 salida.mp4 apoyo1.mp4:INICIO:DURACION[:DESDE] [apoyo2.mp4:INICIO:DURACION[:DESDE] ...]
  DESDE = segundo del video de apoyo desde el que se toma el extracto (por defecto 0).
  INICIO = segundo del reel en el que entra; DURACION = segundos en pantalla (2.5–4 funciona bien).
Hacerlo ANTES de quemar los subtítulos, para que queden encima.
"""
import os, subprocess, sys, tempfile

W, H, FPS = 1080, 1920, 30
FUNDIDO = 0.35

def preparar(src, dur, destino, desde=0.0):
    """Recorta a dur, llena 1080×1920 (recorte centrado), acercamiento del 1 al 6 %, fundidos en alfa."""
    n = int(dur * FPS)
    vf = (f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
          f"format=yuva420p,fade=t=in:st=0:d={FUNDIDO}:alpha=1,fade=t=out:st={dur-FUNDIDO:.2f}:d={FUNDIDO}:alpha=1")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(desde), '-t', str(dur), '-i', src, '-an', '-vf', vf,
                    '-c:v', 'qtrle', destino], check=True)   # qtrle conserva el canal alfa

def main():
    base, salida = sys.argv[1], sys.argv[2]
    items = []
    for a in sys.argv[3:]:
        partes = a.rsplit(':', 3)
        if len(partes) == 4 and partes[0].count(':') == 0 and not partes[1].replace('.', '').isdigit():
            partes = a.rsplit(':', 2) + ['0']
        if len(partes) == 3: partes.append('0')
        items.append(partes)
    with tempfile.TemporaryDirectory() as tmp:
        entradas = ['-i', base]; cadena = []; etiqueta = '[0:v]'
        for i, (src, ini, dur, desde) in enumerate(items):
            ini, dur = float(ini), float(dur)
            mov = os.path.join(tmp, f'b{i}.mov'); preparar(src, dur, mov, float(desde))
            entradas += ['-i', mov]
            cadena.append(f"[{i+1}:v]setpts=PTS+{ini}/TB[b{i}]")
            cadena.append(f"{etiqueta}[b{i}]overlay=eval=frame:enable='between(t,{ini},{ini+dur})':format=auto[o{i}]")
            etiqueta = f'[o{i}]'
        filtro = ';'.join(cadena) + f";{etiqueta}format=yuv420p[vout]"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *entradas, '-filter_complex', filtro,
                        '-map', '[vout]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
                        '-c:a', 'copy', '-movflags', '+faststart', salida], check=True)
    print('listo:', salida, '| apoyos:', len(items))

if __name__ == '__main__':
    main()
