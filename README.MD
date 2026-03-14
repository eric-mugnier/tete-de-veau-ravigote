© Éric Mugnier, all rights reserved — this repository is for version tracking purposes only

## Prérequis

| Outil | Rôle |
|---|---|
| TeXLive + LuaLaTeX + latexmk | compilation LaTeX |
| LilyPond (`/usr/local/bin/lilypond`) | partition musicale (lyluatex) |
| `rsvg-convert` | conversion SVG → PDF (librsvg) |
| `pandoc` | EPUB et postfaces |
| `latexdiff` + `diff_work/make_diff.py` | PDF de diff (cible `diffs` uniquement) |
| Python 3 + [Invoke](https://www.pyinvoke.org/) (`pip install invoke`) | orchestration |

## Installation (nouvelle machine)

Après `git clone`, appliquer le patch local sur un fichier système TeXLive :

```bash
inv setup
```

Cela copie `luaoptions-lib.lua` depuis TeXLive et applique `luaoptions-lib.patch`
(correctif d'un bug lyluatex avec `-output-directory`, cf. le fichier `.patch`).
Le fichier patché est déjà commité dans le dépôt — `inv setup` sert à le régénérer
si le fichier système a changé.

## Compilation

```bash
inv build          # PDF principal
inv sommaire       # sommaire seul
inv notes          # PDF annoté + notes finales
inv epub           # EPUB
inv extrait        # extrait (actes publiés)
inv pers           # liste des personnages
inv couv           # couverture
inv postface       # postfaces (Claude + ChatGPT)
inv total          # LA TOTALE (tout en un)
inv all            # tout compiler + clean
inv clean          # supprimer les fichiers auxiliaires
```

Les tâches `notes`, `diffs` et `epub` déclenchent `build` automatiquement.
On peut combiner des cibles : `inv diffs notes` (build exécuté une seule fois).

Tous les PDF générés atterrissent dans `build/`.
