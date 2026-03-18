# Proposals — illustrations acte_05

Naming convention: `_NNNT_slug-of-subject.jpg|png`
- `NNN` = left-zero-padded note number (3 digits)
- `T` = trailing `0` (standalone) or `1`–`9` (between two notes, or variant)
- slug: lowercase, hyphens, `.jpg` or `.png` only
- drop in `iconography/acte_05/`

Fill the **Filename** column, then tell me to proceed.

| # | Line | Anchor text / context | Suggested subject | Command | Placement | Filename |
|--:|-----:|----------------------|-------------------|---------|-----------|----------|
| 5 | 377 | Titus fait des moulinets avec son Glock façon Jamie Foxx dans Django Unchained | Affiche ou still de *Django Unchained* | `wrapfig` r 0.40 | après `\nf{Django Unchained…}` | `_0110_django-unchained.jpg` |
| 6 | 409 | Aberfeldy 12 ans d'âge | Bouteille Aberfeldy 12 | `wrapfig` r 0.3 | après `\nf{Distillerie Aberfeldy…}` | `_0120_aberfeldy-12.png` |
| 7 | 477 | Luger P08 hérité de son arrière-grand-père | Luger P08 | `wrapfig` l 0.33 | après `\nf{Le Luger P08…}` | `_0130_luger-p08.jpg` |
| 8 | 545 | bollito misto | Assiette de bollito misto | `wrapfig` r 0.32 | après `\nf{bollito misto…}` | `_0140_bollito-misto.png` |
| 9 | 547 | Volnay Santenots 1984 des Hospices de Beaune | Étiquette ou bouteille Volnay Hospices de Beaune | `wrapfig` l 0.3 | après `\nf{Premier cru…Volnay…}` | `_0150_volnay-hospices.png` |
| 10 | 589 | Gunfight at the O.K. Corral (Wyatt Earp / Doc Holliday) | Affiche du film ou photo de la fusillade | `wrapfig` r 0.30 | après `\nf{Règlements de comptes à O.K. Corral…}` | `_0160_ok-corral.jpg` |
| 11 | 755 | paillasson WELCOME TO THE JUNGLE | Affiche *Welcome to the Jungle* (Peter Berg, 2003)  | `wrapfig` r 0.3 | après `\nf{Peter Berg…}` | `_0160_welcome-to-the-jungle.jpg` |
| 12 | 785 | plateau de fromages (couronne lochoise, neufchâtel, brie de Nangis, tomme de Donezan…) | Plateau de fromages | `iconographieimg` pleine page | après §785 (fin description fromages) | `_0180_fromages.jpg` |
| 14 | 1013 | Ferrari 250 GT California Spyder (comte Di Brizzi) | Ferrari 250 GT California Spyder | `inlineblock` t | après le §1013 (fin de l'anecdote du comte) | `_0200_ferrari-250-gt.png` |

---

## Pages figure (§7)

Remplacent les propositions 1–3 ci-dessus. Deux pages dédiées insérées via `\iconographietex` dans §7.

### Figure A — `figures/spandau_fig.tex`

Les 7 prisonniers de Spandau, grille 3+3+1 (comme `women_fig.tex`).
Insertion : après `\nf{La prison de Spandau…}` (fin du passage sur Hess), ligne 7.

| Rang | Sujet | Filename |
|-----:|-------|----------|
| 1 | Rudolf Hess | `_0050_rudolf-hess.jpg` |
| 2 | Karl Dönitz | `_0051_karl-donitz.jpg` |
| 3 | Erich Raeder | `_0052_erich-raeder.jpg` |
| 4 | Konstantin von Neurath | `_0053_konstantin-von-neurath.jpg` |
| 5 | Albert Speer | `_0055_albert-speer.jpg` |
| 6 | Baldur von Schirach | `_0056_baldur-von-schirach.jpg` |
| 7 | Walther Funk | `_0054_walther-funk.jpg` |
| 8 | Prison de Spandau| `_0090_prison-de-spandau.jpg` |

### Figure B — `figures/enfants-nazis_fig.tex`

Les trois enfants de dignitaires nazis, rangée unique côte à côte.
Insertion : après `\nf{Wolf Rüdiger Hess…}` (fin du passage sur les enfants), ligne 7.

| Rang | Sujet | Filename |
|-----:|-------|----------|
| 1 | Wolf Rüdiger Hess | `_0057_wolf-rudiger-hess.jpg` |
| 2 | Gudrun Burwitz (fille Himmler) | `_0058_gudrun-burwitz.jpg` |
| 3 | Edda Göring | `_0059_edda-goring.jpg` |

---

**Notes de travail**

- Propositions 1–3 du tableau remplacées par les figures A et B ci-dessus.
- Pour la figure A, fournir les 7 images avec leurs ratios (hauteur/largeur) pour que je calcule les largeurs de colonnes.
- Pour la figure B, idem pour les 3 images.
- Proposition 12 (plateau de fromages) : pleine page `\iconographieimg` — ne conviendra que si une belle photo généraliste de plateau de fromages français existe.
- Proposition 4 (forêt de nuit) : optionnelle / ambiance. À supprimer si aucune image satisfaisante.
- Ajuster les largeurs wrapfig selon le ratio de l'image retenue.
