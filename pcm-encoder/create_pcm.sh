#!/bin/sh
set -euo pipefail

echo "Starting PCM-Encoder pod"

pcm_directory="/music-categorizer-data/pcm_encoder"
mkdir -p "$pcm_directory"

get_audio() {
    dir_name="$1"
    for file in "$dir_name"/*; do
        [ -f "$file" ] || continue
        base_name=$(basename "$file")

        clean_name=$(echo "$base_name" | tr ' ' '_' | tr -cd '[:alnum:]_.-')
        clean_name="${clean_name%.*}"

        out_file="$pcm_directory/${clean_name}.raw"

        ffmpeg -i "$file" -f s16le -acodec pcm_s16le -ar 44100 -ac 1 "$out_file"
    done
}

get_audio "/app/audio"
get_audio "/music-categorizer-data/audio"

echo "Finished PCM-Encoder pod"