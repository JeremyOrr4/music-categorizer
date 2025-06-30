#!/bin/sh

SRC_DIR="/app/dags"
DEST_DIR="/music-categorizer-data/dags"

mkdir -p "$DEST_DIR"
cp -r "$SRC_DIR"/* "$DEST_DIR"/