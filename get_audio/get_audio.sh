#!/bin/bash
set -euo pipefail

audio_directory="/music-categorizer-data/audio"
mkdir -p "$audio_directory"

PLAYLIST_URL="https://www.youtube.com/watch?v=PGEztInKTAA"

echo "Downloading audio from playlist..."
yt-dlp -i -x --audio-format mp3 --output "${audio_directory}/%(title)s.%(ext)s" "$PLAYLIST_URL"

echo "Download complete. Files saved to: $audio_directory"
ls "$audio_directory"
