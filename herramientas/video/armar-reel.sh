#!/bin/zsh
# Arma un reel vertical: intro (preloader del sitio) + clips con fundido + pleca de nombre + cierre con datos.
# Uso: armar-reel.sh <carpeta_trabajo> <salida.mp4> clip1.mp4 clip2.mp4 ...
# Requiere: dev-server en :4328 (sirve herramientas/video/*.html), Chrome, ffmpeg.
# Los clips deben venir ya normalizados a 1080×1920, 30 fps, AAC estéreo.
set -e
W=$1; OUT=$2; shift 2; CLIPS=("$@")
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE="http://localhost:4328/herramientas/video"
FPS=30; XF=0.6
INTRO_VEL=1.6; INTRO_DUR=2.1; INTRO_HOLD=0.4      # el preloader del sitio dura 3.3 s; aquí va 1.6× más rápido
OUTRO_DUR=3.3;  OUTRO_HOLD=1.6                     # cierre: animación + pausa para leer los datos
PLECA_IN=0.8; PLECA_DUR=5                          # pleca de nombre: entra 0.8 s después del corte, 5 s
: ${PLECA2:=}; : ${PLECA2_CLIP:=2}; : ${PLECA2_IN:=0.8}; : ${PLECA2_DUR:=5}   # pleca de tema opcional (PNG de cuadro completo)
: ${PLECA_SFX:=}                                   # efecto de sonido opcional en cada entrada y salida de pleca
mkdir -p "$W" && cd "$W"

cuadros() {  # cuadros <html> <carpeta> <dur> <hold> <vel>
  local html=$1 dir=$2 dur=$3 hold=$4 vel=$5; mkdir -p $dir
  local N=$(python3 -c "print(int($dur*$FPS))")
  for ((i=0;i<N;i++)); do
    local t=$(python3 -c "print(round($i/$FPS,4))")
    "$CHROME" --headless=new --no-first-run --disable-gpu --user-data-dir=./perfil --hide-scrollbars \
      --window-size=1080,1920 --force-device-scale-factor=1 --virtual-time-budget=2500 \
      --screenshot=$dir/f$(printf %04d $i).png "$BASE/$html?t=$t&vel=$vel" >/dev/null 2>&1
  done
  local H=$(python3 -c "print(int($hold*$FPS))")
  for ((k=1;k<=H;k++)); do cp $dir/f$(printf %04d $((N-1))).png $dir/f$(printf %04d $((N-1+k))).png; done
  ffmpeg -y -loglevel error -framerate $FPS -i $dir/f%04d.png -f lavfi -i anullsrc=r=48000:cl=stereo -shortest \
    -vf "format=yuv420p" -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k $dir.mp4
}
[ -f intro.mp4 ] || cuadros intro.html intro $INTRO_DUR $INTRO_HOLD $INTRO_VEL
[ -f outro.mp4 ] || cuadros outro.html outro $OUTRO_DUR $OUTRO_HOLD 1

if [ ! -f pleca-B.png ]; then
  "$CHROME" --headless=new --no-first-run --disable-gpu --user-data-dir=./perfil --hide-scrollbars \
    --window-size=1080,1920 --force-device-scale-factor=1 --default-background-color=00000000 --virtual-time-budget=4000 \
    --screenshot=pleca-B.png "$BASE/pleca-muestra.html?v=B&solo=1" >/dev/null 2>&1
fi

# Cadena: intro + clips + outro, con fundidos; la pleca va en el primer clip y en el último
FILES=(intro.mp4 "${CLIPS[@]}" outro.mp4)
INPUTS=(); for f in "${FILES[@]}"; do INPUTS+=(-i "$f"); done
python3 - "$XF" "$PLECA_IN" "$PLECA_DUR" "$PLECA2" "$PLECA2_CLIP" "$PLECA2_IN" "$PLECA2_DUR" "$PLECA_SFX" "${FILES[@]}" <<'PY'
import sys, subprocess, json
xf=float(sys.argv[1]); pin=float(sys.argv[2]); pdur=float(sys.argv[3]); p2=sys.argv[4]; p2clip=int(sys.argv[5]); p2in=float(sys.argv[6]); p2dur=float(sys.argv[7]); sfx=sys.argv[8]; files=sys.argv[9:]
dur=[float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode().strip()) for f in files]
v='[0:v]'; a='[0:a]'; t=0; partes=[]; inicio=[0.0]
for i in range(1,len(files)):
    t += dur[i-1] - xf; inicio.append(t)
    partes.append(f"{v}[{i}:v]xfade=transition=fade:duration={xf}:offset={t:.3f}[v{i}]")
    partes.append(f"{a}[{i}:a]acrossfade=d={xf}[a{i}]")
    v=f'[v{i}]'; a=f'[a{i}]'
primero=inicio[1]+pin                       # pleca en el primer clip
ultimo=inicio[-2]+1.0                       # pleca en el último clip, 1 s después de su corte
def pleca(p0):
    p1,p2,p3=p0+0.6,p0+pdur,p0+pdur+0.4
    return f"if(lt(t,{p0:.3f}),-1100,if(lt(t,{p1:.3f}),-1100*pow(1-(t-{p0:.3f})/0.6,3),if(lt(t,{p2:.3f}),0,if(lt(t,{p3:.3f}),-1100*pow((t-{p2:.3f})/0.4,3),-1100))))"
x=f"if(lt(t,{inicio[-2]:.3f}),{pleca(primero)},{pleca(ultimo)})"
n=len(files)
capa=f"{v}[{n}:v]overlay=eval=frame:x='{x}':y=0:format=auto[vp]"; final='[vp]'
momentos=[primero, primero+pdur, ultimo, ultimo+pdur]   # entradas y salidas de pleca (para el efecto de sonido)
if p2:
    def pleca2(p0):
        p1,p2_,p3=p0+0.6,p0+p2dur,p0+p2dur+0.4
        return f"if(lt(t,{p0:.3f}),-1100,if(lt(t,{p1:.3f}),-1100*pow(1-(t-{p0:.3f})/0.6,3),if(lt(t,{p2_:.3f}),0,if(lt(t,{p3:.3f}),-1100*pow((t-{p2_:.3f})/0.4,3),-1100))))"
    capa+=f";[vp][{n+1}:v]overlay=eval=frame:x='{pleca2(inicio[p2clip]+p2in)}':y=0:format=auto[vq]"; final='[vq]'
    t2=inicio[p2clip]+p2in; momentos+=[t2, t2+p2dur]
audio=f"{a}loudnorm=I=-16:TP=-1.5:LRA=11[aout]"
if sfx:
    k=len(momentos); idx=n+1+(1 if p2 else 0)
    ramas=f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume=-6dB,asplit={k}"+''.join(f"[s{i}]" for i in range(k))
    delays=';'.join(f"[s{i}]adelay={int(m*1000)}|{int(m*1000)}[d{i}]" for i,m in enumerate(momentos))
    mezcla=f"{a}"+''.join(f"[d{i}]" for i in range(k))+f"amix=inputs={k+1}:normalize=0:duration=first[amx]"
    audio=f"{ramas};{delays};{mezcla};[amx]loudnorm=I=-16:TP=-1.5:LRA=11[aout]"
filtro=';'.join(partes)+f";{capa};{final}format=yuv420p[vout];{audio}"
open('filtro.txt','w').write(filtro)
print('inicios:', [round(s,2) for s in inicio], '| total ≈', round(sum(dur)-xf*(n-1),1), 's')
PY
EXTRA=(); [ -n "$PLECA2" ] && EXTRA+=(-i "$PLECA2"); [ -n "$PLECA_SFX" ] && EXTRA+=(-i "$PLECA_SFX")
ffmpeg -y -loglevel error "${INPUTS[@]}" -i pleca-B.png "${EXTRA[@]}" -filter_complex_script filtro.txt \
  -map "[vout]" -map "[aout]" -c:v libx264 -preset medium -crf 19 -r $FPS -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "listo: $OUT"
