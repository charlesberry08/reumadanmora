#!/bin/zsh
# Nivela el volumen del reel terminado en dos pasadas (lineal, sin bombear): -13 LUFS integrados, picos ≤ -1 dBTP.
# Uso: normalizar.sh entrada.mp4 salida.mp4 [LUFS]   (el video se copia sin recodificar)
set -e
IN=$1; OUT=$2; I=${3:--13}
M=$(ffmpeg -nostats -i "$IN" -af "loudnorm=I=$I:TP=-1.0:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
v(){ echo "$M" | python3 -c "import sys,json; print(json.load(sys.stdin)['$1'])"; }
ffmpeg -y -loglevel error -i "$IN" -c:v copy \
  -af "loudnorm=I=$I:TP=-1.0:LRA=11:measured_I=$(v input_i):measured_TP=$(v input_tp):measured_LRA=$(v input_lra):measured_thresh=$(v input_thresh):offset=$(v target_offset):linear=true,aresample=48000" \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"
echo "$(basename "$OUT"): $(v input_i) → $I LUFS"
