#!/bin/zsh
# Arma un reel vertical: intro (preloader del sitio) + clips con fundido + pleca de nombre.
# Uso: armar-reel.sh <carpeta_trabajo> <salida.mp4> clip1.mp4 clip2.mp4 ...
# Requiere: dev-server en :4328 (para intro.html y pleca-muestra.html), Chrome, ffmpeg.
set -e
W=$1; OUT=$2; shift 2; CLIPS=("$@")
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE="http://localhost:4328/herramientas/video"
FPS=30; INTRO_DUR=3.3; INTRO_HOLD=0.5; XF=0.6
mkdir -p "$W/intro" && cd "$W"

# 1) Intro: cuadro por cuadro con las animaciones congeladas en t
if [ ! -f intro.mp4 ]; then
  N=$(python3 -c "print(int($INTRO_DUR*$FPS))")
  for ((i=0;i<N;i++)); do
    t=$(python3 -c "print(round($i/$FPS,4))")
    "$CHROME" --headless=new --no-first-run --disable-gpu --user-data-dir=./perfil --hide-scrollbars \
      --window-size=1080,1920 --force-device-scale-factor=1 --virtual-time-budget=2500 \
      --screenshot=intro/f$(printf %04d $i).png "$BASE/intro.html?t=$t" >/dev/null 2>&1
  done
  HOLD=$(python3 -c "print(int($INTRO_HOLD*$FPS))")
  for ((k=1;k<=HOLD;k++)); do cp intro/f$(printf %04d $((N-1))).png intro/f$(printf %04d $((N-1+k))).png; done
  ffmpeg -y -loglevel error -framerate $FPS -i intro/f%04d.png -f lavfi -i anullsrc=r=48000:cl=stereo -shortest \
    -vf "format=yuv420p" -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 192k intro.mp4
fi

# 2) Pleca de nombre (PNG transparente de cuadro completo)
if [ ! -f pleca-B.png ]; then
  "$CHROME" --headless=new --no-first-run --disable-gpu --user-data-dir=./perfil --hide-scrollbars \
    --window-size=1080,1920 --force-device-scale-factor=1 --default-background-color=00000000 --virtual-time-budget=4000 \
    --screenshot=pleca-B.png "$BASE/pleca-muestra.html?v=B&solo=1" >/dev/null 2>&1
fi

# 3) Cadena de fundidos: intro + clips
INPUTS=(-i intro.mp4); for c in "${CLIPS[@]}"; do INPUTS+=(-i "$c"); done
python3 - "$XF" intro.mp4 "${CLIPS[@]}" > filtro.txt <<'PY'
import sys, subprocess
xf=float(sys.argv[1]); files=sys.argv[2:]
dur=[float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode().strip()) for f in files]
v='[0:v]'; a='[0:a]'; t=0; partes=[]
for i in range(1,len(files)):
    t += dur[i-1] - xf
    partes.append(f"{v}[{i}:v]xfade=transition=fade:duration={xf}:offset={t:.3f}[v{i}]")
    partes.append(f"{a}[{i}:a]acrossfade=d={xf}[a{i}]")
    v=f'[v{i}]'; a=f'[a{i}]'
inicio_clip1 = dur[0]-xf
print(';'.join(partes)); print(f"{v}|{a}|{inicio_clip1:.3f}", file=sys.stderr)
PY
FILTRO=$(cat filtro.txt)
read VF AF T1 <<< "$(python3 - "$XF" intro.mp4 "${CLIPS[@]}" 2>&1 >/dev/null <<'PY' | tr '|' ' '
import sys, subprocess
xf=float(sys.argv[1]); files=sys.argv[2:]
dur=[float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode().strip()) for f in files]
n=len(files)-1; print(f"[v{n}]|[a{n}]|{dur[0]-xf:.3f}", file=sys.stderr)
PY
)"
# 4) Pleca sobre el primer clip: entra 0.8 s después del corte, dura 5 s
P0=$(python3 -c "print(round($T1+0.8,3))"); P1=$(python3 -c "print(round($T1+1.4,3))"); P2=$(python3 -c "print(round($T1+6.4,3))"); P3=$(python3 -c "print(round($T1+6.8,3))")
ffmpeg -y -loglevel error "${INPUTS[@]}" -i pleca-B.png -filter_complex \
  "$FILTRO;${VF}[$((${#CLIPS[@]}+1)):v]overlay=eval=frame:x='if(lt(t,$P0),-1100,if(lt(t,$P1),-1100*pow(1-(t-$P0)/0.6,3),if(lt(t,$P2),0,if(lt(t,$P3),-1100*pow((t-$P2)/0.4,3),-1100))))':y=0:format=auto,format=yuv420p[vout];${AF}loudnorm=I=-16:TP=-1.5:LRA=11[aout]" \
  -map "[vout]" -map "[aout]" -c:v libx264 -preset medium -crf 19 -r $FPS -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "listo: $OUT"
