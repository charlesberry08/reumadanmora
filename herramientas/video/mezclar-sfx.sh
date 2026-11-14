#!/bin/zsh
# Mezcla un efecto de sonido sobre el reel YA normalizado, con ganancia fija (sin pasar por loudnorm, que sube los sonidos sostenidos).
# Uso: mezclar-sfx.sh entrada.mp4 salida.mp4 efecto.mp3 INICIO DUR VOL   (fade de entrada 0.25 s y de salida 0.5 s; el video se copia)
# Referencia: audio/frase-coche.mp3 mide -7.3 LUFS; VOL 0.46 lo deja ≈ -14 LUFS, al nivel de la voz (-13).
set -e
IN=$1; OUT=$2; FX=$3; T0=$4; DUR=$5; VOL=${6:-0.46}
MS=$(python3 -c "print(int(float('$T0')*1000))"); FO=$(python3 -c "print(round(float('$DUR')-0.5,3))")
ffmpeg -nostdin -y -loglevel error -i "$IN" -i "$FX" -filter_complex \
  "[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:$DUR,afade=t=in:d=0.25,afade=t=out:st=$FO:d=0.5,volume=$VOL,adelay=${MS}|${MS}[fx];[0:a][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.891:level=false[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT" </dev/null
echo "listo: $OUT | efecto en $T0 s por $DUR s a $VOL"
