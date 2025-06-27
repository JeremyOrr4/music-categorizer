#!/bin/sh
set -euo pipefail

echo "Starting PCM-Encoder pod"

pcm_directory="/music-categorizer-data/pcm_encoding"
# Ensure output directory exists
mkdir -p "$pcm_directory"

for file in /app/audio/*; do
    [ -f "$file" ] || continue
    base_name=$(basename "$file")
    out_file="$pcm_directory/${base_name%.*}.raw"
    ffmpeg -i "$file" -f s16le -acodec pcm_s16le "$out_file"
done


echo "Finished PCM-Encoder pod"