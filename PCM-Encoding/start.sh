#!/bin/sh

for file in app/audio/*; do
    ffmpeg -i "$file" -f s16le -acodec pcm_s16le "${file}.raw"
done

