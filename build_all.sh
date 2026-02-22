#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "=== 1/4  main PDF ==="
latexmk -g -pdf -interaction=nonstopmode tete_de_veau_ravigote.tex

echo "=== 2/4  sommaire PDF ==="
latexmk -g -pdf -interaction=nonstopmode tete_de_veau_ravigote_sommaire.tex

echo "=== 3/4  diff PDF ==="
python3 diff_work/make_diff.py
cp diff_work/tete_de_veau_ravigote_diff.pdf tete_de_veau_ravigote_diff.pdf

echo "=== 4/4  COMPLET PDF ==="
pdftk tete_de_veau_ravigote_couverture_minimaliste.pdf tete_de_veau_ravigote.pdf \
      cat output tete_de_veau_ravigote_COMPLET.pdf

echo ""
echo "Done."
ls -lh tete_de_veau_ravigote.pdf \
        tete_de_veau_ravigote_sommaire.pdf \
        tete_de_veau_ravigote_diff.pdf \
        tete_de_veau_ravigote_COMPLET.pdf
