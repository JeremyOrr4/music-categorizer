#!/bin/sh
set -euo pipefail

echo "Starting cleanup of directories in /music-categorizer-data"

cd /music-categorizer-data

rm -rf lr-generator pcm_encoder pr-generator audio

echo "Cleanup complete: deleted lr-generator, pcm_encoder, pr-generator"
