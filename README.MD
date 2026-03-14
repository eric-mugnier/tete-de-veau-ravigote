© Éric Mugnier, all rights reserved — this repository is for version tracking purposes only

## Prérequis

- TeXLive (2024 ou ultérieur) avec LuaLaTeX
- LilyPond (`/usr/local/bin/lilypond`)
- Python 3 + [Invoke](https://www.pyinvoke.org/) (`pip install invoke`)

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
inv pers           # liste des personnages
inv couv           # couverture
inv postface       # postfaces (Claude + ChatGPT)
inv total          # LA TOTALE (tout en un)
inv all            # tout compiler + clean
inv clean          # supprimer les fichiers auxiliaires
```
