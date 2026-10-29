#!/usr/bin/env python3
"""Sobrepone tarjetas de puntos numerados (1, 2, 3…) en el reel, cada una en el momento en que el doctor
presenta ese punto. Entran subiendo con fundido, se quedan DUR segundos y se van igual.

Uso: puntos.py reel.mp4 salida.mp4 "N|Texto del punto|INICIO|DUR" ["N|Texto|INICIO|DUR" ...] [--de 3] [--eyebrow "Señal de alarma"] [--y 240]
  --y: altura de la tarjeta en px (780 = pecho; 240 = arriba, sobre la frente, si el doctor está cerca de la cámara).
Requiere el dev-server en :4328 (sirve puntos.html) y Chrome. Hacerlo ANTES de quemar subtítulos.
"""
import os, subprocess, sys, tempfile, urllib.parse

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
URL = 'http://localhost:4328/herramientas/video/puntos.html'
FUNDIDO, DESPLAZ = 0.35, 60   # segundos de fundido, píxeles de deslizamiento

def main():
    args = sys.argv[1:]
    de = args[args.index('--de') + 1] if '--de' in args else ''
    eyebrow = args[args.index('--eyebrow') + 1] if '--eyebrow' in args else None
    altura = args[args.index('--y') + 1] if '--y' in args else ''
    items = [a for a in args if '|' in a]
    base, salida = args[0], args[1]
    with tempfile.TemporaryDirectory() as tmp:
        entradas = ['-i', base]; cadena = []; etiqueta = '[0:v]'
        for i, item in enumerate(items):
            n, texto, ini, dur = item.split('|'); ini, dur = float(ini), float(dur)
            q = {'n': n, 'texto': texto}
            if de: q['de'] = de
            if eyebrow is not None: q['eyebrow'] = eyebrow
            if altura: q['y'] = altura
            png = os.path.join(tmp, f'p{i}.png')
            subprocess.run([CHROME, '--headless=new', '--no-first-run', '--disable-gpu', f'--user-data-dir={tmp}/perfil',
                            '--hide-scrollbars', '--window-size=1080,1920', '--force-device-scale-factor=1',
                            '--default-background-color=00000000', '--virtual-time-budget=4000',
                            f'--screenshot={png}', f'{URL}?{urllib.parse.urlencode(q)}'],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            entradas += ['-loop', '1', '-t', str(dur), '-i', png]
            fin = ini + dur
            # alfa: fundido de entrada y salida; y: sube DESPLAZ px al entrar y baja al salir
            cadena.append(f"[{i+1}:v]format=yuva420p,fade=t=in:st=0:d={FUNDIDO}:alpha=1,fade=t=out:st={dur-FUNDIDO:.2f}:d={FUNDIDO}:alpha=1,setpts=PTS+{ini}/TB[c{i}]")
            y = (f"if(lt(t,{ini+FUNDIDO:.3f}),{DESPLAZ}*(1-(t-{ini:.3f})/{FUNDIDO}),"
                 f"if(gt(t,{fin-FUNDIDO:.3f}),{DESPLAZ}*((t-{fin-FUNDIDO:.3f})/{FUNDIDO}),0))")
            cadena.append(f"{etiqueta}[c{i}]overlay=eval=frame:x=0:y='{y}':enable='between(t,{ini},{fin})':format=auto[o{i}]")
            etiqueta = f'[o{i}]'
        filtro = ';'.join(cadena) + f";{etiqueta}format=yuv420p[vout]"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *entradas, '-filter_complex', filtro,
                        '-map', '[vout]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
                        '-c:a', 'copy', '-movflags', '+faststart', salida], check=True)
    print('listo:', salida, '| puntos:', len(items))

if __name__ == '__main__':
    main()
