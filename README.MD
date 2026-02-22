© Éric Mugnier, all rights reserved — this repository is for version tracking purposes only

## Compilation

### Livre

```bash
pdflatex tete_de_veau_ravigote.tex
```

### Couverture

```bash
pdflatex tete_de_veau_ravigote_couverture_minimaliste.tex
```

### PDF complet (couverture + livre)

```bash
pdftk tete_de_veau_ravigote_couverture_minimaliste.pdf tete_de_veau_ravigote.pdf cat output tete_de_veau_ravigote_COMPLET.pdf
```