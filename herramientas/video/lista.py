#!/usr/bin/env python3
"""Lista acumulativa en el reel: la tarjeta aparece con el primer punto, cada punto se suma en el segundo en que
el doctor lo menciona (fundido + deslizamiento corto) y la lista completa se queda hasta FIN, cuando sale entera.

Uso: lista.py reel.mp4 salida.mp4 --eyebrow "También dañan el hígado" --fin 87.6 [--y 200] [--sin-fondo] "Texto|INICIO" ["Texto|INICIO" ...]
  --sin-fondo: sin recuadro (texto con contorno); ocupa menos y puede ir sobre el pecho, bajando los subtítulos en ese tramo.
Requiere el dev-server en :4328 (sirve lista.html) y Chrome. Hacerlo ANTES de quemar subtítulos.
"""
import os, subprocess, sys, tempfile, urllib.parse

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
URL = 'http://localhost:4328/herramientas/video/lista.html'
FUNDIDO, DESPLAZ = 0.25, 28

def opcion(args, nombre, defecto=None):
    return args[args.index(nombre) + 1] if nombre in args else defecto

def main():
    args = sys.argv[1:]
    base, salida = args[0], args[1]
    eyebrow = opcion(args, '--eyebrow', ''); fin = float(opcion(args, '--fin')); y = opcion(args, '--y', '200')
    items = [a.rsplit('|', 1) for a in args[2:] if '|' in a]
    textos = [t for t, _ in items]; tiempos = [float(t) for _, t in items]
    q0 = {'items': '|'.join(textos), 'eyebrow': eyebrow, 'y': y}
    if '--sin-fondo' in args: q0['fondo'] = '0'
    with tempfile.TemporaryDirectory() as tmp:
        capas = [('base', tiempos[0])] + [(str(i + 1), t) for i, t in enumerate(tiempos)]
        entradas = ['-i', base]; cadena = []; etiqueta = '[0:v]'
        for k, (capa, ini) in enumerate(capas):
            png = os.path.join(tmp, f'c{k}.png')
            subprocess.run([CHROME, '--headless=new', '--no-first-run', '--disable-gpu', f'--user-data-dir={tmp}/perfil',
                            '--hide-scrollbars', '--window-size=1080,1920', '--force-device-scale-factor=1',
                            '--default-background-color=00000000', '--virtual-time-budget=4000',
                            f'--screenshot={png}', f"{URL}?{urllib.parse.urlencode({**q0, 'capa': capa})}"],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            dur = fin - ini
            entradas += ['-loop', '1', '-framerate', '30', '-t', f'{dur:.3f}', '-i', png]
            cadena.append(f"[{k+1}:v]format=yuva420p,fade=t=in:st=0:d={FUNDIDO}:alpha=1,"
                          f"fade=t=out:st={dur-0.35:.3f}:d=0.35:alpha=1,setpts=PTS+{ini}/TB[l{k}]")
            if capa == 'base':   # la tarjeta sube un poco al entrar
                x, yy = '0', f"if(lt(t,{ini+FUNDIDO:.3f}),{DESPLAZ}*(1-(t-{ini:.3f})/{FUNDIDO}),0)"
            else:                # cada punto llega deslizándose desde la izquierda
                x, yy = f"if(lt(t,{ini+FUNDIDO:.3f}),-{DESPLAZ}*(1-(t-{ini:.3f})/{FUNDIDO}),0)", '0'
            cadena.append(f"{etiqueta}[l{k}]overlay=eval=frame:x='{x}':y='{yy}':enable='between(t,{ini},{fin})':format=auto[o{k}]")
            etiqueta = f'[o{k}]'
        filtro = ';'.join(cadena) + f";{etiqueta}format=yuv420p[vout]"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *entradas, '-filter_complex', filtro,
                        '-map', '[vout]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
                        '-c:a', 'copy', '-movflags', '+faststart', salida], check=True)
    print('listo:', salida, '| puntos:', len(items))

if __name__ == '__main__':
    main()
