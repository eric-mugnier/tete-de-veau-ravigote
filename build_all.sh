#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Options : diffs  compiler le PDF de diffs
#           notes  compiler tete_de_veau_ravigote_annote.pdf (roman annoté)
#                  et tete_de_veau_ravigote-notes.pdf (notes seules)
#           epub   compiler tete_de_veau_ravigote.epub
DIFFS=0
NOTES=0
EPUB=0
for arg in "$@"; do
  [ "$arg" = "diffs" ] && DIFFS=1
  [ "$arg" = "notes" ] && NOTES=1
  [ "$arg" = "epub"  ] && EPUB=1
done

echo "=== git hash ==="
git log -1 --format=%h > tete_de_veau_ravigote.gitinfo

echo "=== svg → pdf ==="
for svg in images/*.svg; do
  rsvg-convert -f pdf -o "${svg}.pdf" "$svg"
done

echo "=== 1/4  main PDF ==="
latexmk -g -lualatex -interaction=nonstopmode tete_de_veau_ravigote.tex

echo "=== 2/4  sommaire PDF ==="
latexmk -g -lualatex -interaction=nonstopmode tete_de_veau_ravigote_sommaire.tex

if [ "$EPUB" = "1" ]; then
  echo "=== epub ==="
  pandoc tete_de_veau_ravigote.tex -o tete_de_veau_ravigote.epub \
    --metadata title="Tête de veau ravigote" \
    --metadata author="Éric Mugnier" \
    --metadata lang="fr"
else
  echo "=== epub === (ignoré : passer 'epub' pour compiler)"
fi

if [ "$DIFFS" = "1" ]; then
  echo "=== 3/4  diff PDF ==="
  python3 diff_work/make_diff.py
  cp diff_work/tete_de_veau_ravigote_diff.pdf tete_de_veau_ravigote_diff.pdf
else
  echo "=== 3/4  diff PDF === (ignoré : passer 'diffs' pour compiler)"
fi

echo "=== 4/4  COMPLET PDF ==="
### pdftk tete_de_veau_ravigote_couverture_minimaliste.pdf tete_de_veau_ravigote.pdf \
###       cat output tete_de_veau_ravigote_COMPLET.pdf
### 
### echo ""
echo "Done."

# ─── Cible notes (optionnelle) ────────────────────────────────────────────────
if [ "$NOTES" = "1" ]; then
  echo ""
  echo "=== NOTES : génération du .ent ==="
  lualatex -interaction=nonstopmode -jobname=tete_de_veau_ravigote "\def\AVECNOTES{}\def\SANSNOTESFINALES{}\input{tete_de_veau_ravigote}"
  lualatex -interaction=nonstopmode -jobname=tete_de_veau_ravigote "\def\AVECNOTES{}\def\SANSNOTESFINALES{}\input{tete_de_veau_ravigote}"
  # 1. Roman annoté : numéros de notes inline, sans les notes finales
  cp tete_de_veau_ravigote.pdf tete_de_veau_ravigote_annote.pdf
  echo "→ tete_de_veau_ravigote_annote.pdf"
  # 2. Notes seules (compiler AVANT de restaurer le roman, .ent encore peuplé)
  latexmk -g -lualatex -interaction=nonstopmode tete_de_veau_ravigote_notes.tex
  echo "→ tete_de_veau_ravigote_notes.pdf"
  # 3. Illustrations
  latexmk -g -lualatex -interaction=nonstopmode tete_de_veau_ravigote_illustrations.tex
  echo "→ tete_de_veau_ravigote_illustrations.pdf"
  # Restaurer le PDF principal propre (sans numéros de notes)
  latexmk -g -lualatex -interaction=nonstopmode tete_de_veau_ravigote.tex
fi
ls -lh tete_de_veau_ravigote.pdf \
        tete_de_veau_ravigote.epub \
        tete_de_veau_ravigote_sommaire.pdf \
        tete_de_veau_ravigote_diff.pdf \
        tete_de_veau_ravigote_COMPLET.pdf \
        tete_de_veau_ravigote_illustrations.pdf \
        tete_de_veau_ravigote_annote.pdf \
        tete_de_veau_ravigote_notes.pdf \
        2>/dev/null || true
