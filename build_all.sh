#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Options : --no-diff  sauter l'étape diff
#           annote     compiler aussi la version avec notes finales
NO_DIFF=0
ANNOTE=0
for arg in "$@"; do
  [ "$arg" = "--no-diff" ] && NO_DIFF=1
  [ "$arg" = "annote" ]    && ANNOTE=1
done

echo "=== 1/4  main PDF ==="
latexmk -g -pdf -interaction=nonstopmode tete_de_veau_ravigote.tex

echo "=== 2/4  sommaire PDF ==="
latexmk -g -pdf -interaction=nonstopmode tete_de_veau_ravigote_sommaire.tex

if [ "$NO_DIFF" = "1" ]; then
  echo "=== 3/4  diff PDF === (ignoré : --no-diff)"
else
  echo "=== 3/4  diff PDF ==="
  python3 diff_work/make_diff.py
  cp diff_work/tete_de_veau_ravigote_diff.pdf tete_de_veau_ravigote_diff.pdf
fi

echo "=== 4/4  COMPLET PDF ==="
pdftk tete_de_veau_ravigote_couverture_minimaliste.pdf tete_de_veau_ravigote.pdf \
      cat output tete_de_veau_ravigote_COMPLET.pdf

echo ""
echo "Done."

# ─── Cible annotée (optionnelle) ──────────────────────────────────────────────
if [ "$ANNOTE" = "1" ]; then
  echo ""
  echo "=== ANNOTE : compilation avec notes finales ==="
  pdflatex -interaction=nonstopmode "\def\AVECNOTES{}\input{tete_de_veau_ravigote}"
  pdflatex -interaction=nonstopmode "\def\AVECNOTES{}\input{tete_de_veau_ravigote}"
  mv tete_de_veau_ravigote.pdf tete_de_veau_ravigote_annote.pdf
  echo "→ tete_de_veau_ravigote_annote.pdf"
fi
ls -lh tete_de_veau_ravigote.pdf \
        tete_de_veau_ravigote_sommaire.pdf \
        tete_de_veau_ravigote_diff.pdf \
        tete_de_veau_ravigote_COMPLET.pdf
