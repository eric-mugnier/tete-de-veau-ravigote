#!/bin/bash
cd "$(dirname "$0")"
for f in *.tex; do
  [[ "$f" == *_fig.tex || "$f" == figure.tex ]] && continue
  lualatex -interaction=nonstopmode "$f"
  # second pass for files whose _fig uses TikZ remember picture
  stem="${f%.tex}"
  if grep -q "remember picture" "${stem}_fig.tex" 2>/dev/null; then
    lualatex -interaction=nonstopmode "$f"
  fi
done
