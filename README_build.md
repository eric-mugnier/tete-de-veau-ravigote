# Build — *Tête de veau ravigote*

## Prérequis

| Outil | Rôle |
|---|---|
| `lualatex` + `latexmk` | compilation LaTeX |
| `rsvg-convert` | conversion SVG → PDF (`librsvg`) |
| `pandoc` | génération EPUB |
| `python3` + `invoke` | orchestration (`pip install invoke`) |
| `latexdiff` + `make_diff.py` | PDF de diff (cible `diffs` uniquement) |

## Tâches

```
inv build    →  main PDF (build/tete_de_veau_ravigote.pdf) + sommaire
inv notes    →  build + PDF annoté + notes seules + illustrations
inv diffs    →  build + PDF de diff (latexdiff)
inv epub     →  build + EPUB (pandoc)
inv clean    →  supprime les fichiers temporaires (racine + build/)
```

> `notes`, `diffs` et `epub` déclenchent `build` automatiquement (`pre=[build]`).

## Combiner des cibles

```
inv diffs notes      # build (une seule fois), puis diffs, puis notes
inv build clean      # équivalent de ./build_all.sh sans options
```

## Sortie

Les PDF générés atterrissent dans `build/` (configuré dans `.latexmkrc`) :

```
build/tete_de_veau_ravigote.pdf
build/tete_de_veau_ravigote_sommaire.pdf
build/tete_de_veau_ravigote_annote.pdf   (cible notes)
build/tete_de_veau_ravigote_notes.pdf    (cible notes)
build/tete_de_veau_ravigote_illustrations.pdf  (cible notes)
build/tete_de_veau_ravigote_diff.pdf     (cible diffs)
tete_de_veau_ravigote.epub               (cible epub)
```
