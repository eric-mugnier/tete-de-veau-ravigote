#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
for f in *.ly; do
    echo "▶ $f"
    lilypond "$f"
done
