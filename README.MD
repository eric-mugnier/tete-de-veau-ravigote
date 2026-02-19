© Éric Mugnier, all rights reserved — this repository is for version tracking purposes only

## Compilation

### Livre

```bash
pdflatex tete_de_veau_ravigote.tex
```

### Couvertures

```bash
pdflatex tete_de_veau_ravigote_couverture_minimaliste.tex
pdflatex tete_de_veau_ravigote_couverture.tex
pdflatex tete_de_veau_ravigote_couverture_minuit.tex
pdflatex tete_de_veau_ravigote_couverture_minuit_sans_bandeau.tex
pdflatex tete_de_veau_ravigote_couverture_fayard.tex
pdflatex tete_de_veau_ravigote_couverture_sn.tex
pdflatex tete_de_veau_ravigote_couverture_polar.tex
pdflatex tete_de_veau_ravigote_couverture_actes_noirs.tex
```

### PDF complet (couverture + livre)

```bash
pdftk tete_de_veau_ravigote_couverture_minimaliste.pdf tete_de_veau_ravigote.pdf cat output tete_de_veau_ravigote_COMPLET.pdf
```