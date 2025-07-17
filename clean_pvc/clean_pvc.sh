#!/bin/sh
set -euo pipefail

echo "Starting cleanup of directories in /music-categorizer-data"

cd /music-categorizer-data

rm -rf pcm_encoder pr-generator audio

echo "Cleanup complete: deleted pcm_encoder, pr-generator audio"
