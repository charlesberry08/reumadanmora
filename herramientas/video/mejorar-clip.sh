#!/bin/zsh
# Mejora un clip de celular para reel: denoise ligero + nitidez leve + limpieza y compresión de voz.
# Uso: mejorar-clip.sh <entrada.mov> <salida.mp4> [duración_máx_seg]
# Salida: 1080×1920, 30 fps, H.264 crf 18, AAC 192k estéreo (listo para armar-reel.sh).
set -e
IN=$1; OUT=$2; T=${3:+-t $3}
VF="scale=1080:1920:flags=lanczos,setsar=1,fps=30,hqdn3d=2:1.5:3:3,unsharp=5:5:0.45:5:5:0,format=yuv420p"
AF="aresample=48000,aformat=channel_layouts=stereo,highpass=f=80,afftdn=nf=-28:nr=10:tn=1,deesser=i=0.3,acompressor=threshold=-20dB:ratio=3:attack=8:release=160:makeup=4dB"
ffmpeg -y -loglevel error -i "$IN" ${=T} -vf "$VF" -af "$AF" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k "$OUT"
echo "mejorado: $OUT"
