#!/bin/sh
echo "Starting create_pcm pod"

mkdir -p /music-categorizer-data/pcm_encoding

for file in /app/audio/*; do
    [ -f "$file" ] || continue

    if ffmpeg -i "$file" -f s16le -acodec pcm_s16le "/music-categorizer-data/pcm_encoding/$(basename "$file").raw"; then
        echo "Processed $file"
    else
        echo "Failed to process $file" >&2
    fi
done

