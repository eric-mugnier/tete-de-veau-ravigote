#!/bin/bash
# cd "$(dirname "$0")/figures"
for f in *.tex; do
  [[ "$f" != *_fig.tex && "$f" != figure.tex ]] && lualatex "$f"
done