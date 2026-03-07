# TODO — fetch_images.py

## Setup

1. Copy `config.py.example` to `config.py` and fill in your credentials:
   ```
   GOOGLE_API_KEY = "your_key_here"
   GOOGLE_CX      = "your_cx_here"
   ```
   - Get a Google API key: https://console.developers.google.com/
   - Create a Custom Search Engine (cx): https://cse.google.com/cse/
     - Enable "Image search" in the CSE settings
     - Set it to search the entire web

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## First run

```
python fetch_images.py
```

The script will show the first 10 extracted note subjects and ask for confirmation
before starting the download. Type `y` to proceed.

Images are saved to `iconographie/note_NNN_<slug>.jpg`.
Progress is logged to `fetch_log.csv` (resumable — safe to interrupt and restart).

## Daily runs (100 Google API calls per run ≈ 50 notes/day)

Either run manually:
```
python fetch_images.py
```

Or set up the cron job (runs every day at 08:00):
```
0 8 * * * cd ~/tdvr && venv/bin/python fetch_images.py >> logs/fetch.log 2>&1
```

Add it with `crontab -e` (create `~/tdvr/logs/` first).

## Other commands

```
python fetch_images.py --dry-run          # list all 846 extracted subjects, no download
python fetch_images.py --pdf path/to.pdf  # use a different notes PDF
```


Peux-tu essayer d'écrire une dizaine de paragraphes pour une postface ? C'est moi qui la signe. J'aimerais imiter le style de Charles Kinbote dans Feu Pâle de Nabokov. Kinbote écrit dans un style académique, mais on comprend qu'il ne va pas bien :)



résumé de Feu Pâle :



Le poète américain John Shade est mort ; assassiné. Son dernier poème, « Feu pâle », a été publié dans un recueil, accompagné d'une préface, d'un long commentaire et de notes de son éditeur, Charles Kinbote. (...) Kinbote est hautain, curieux, intolérant, mais aussi fou, méchant et même dangereux.



Si tu veux, on peut procéder par dialogue, tu me poses des questions, j'y réponds, et tu écris la postface basée sus mes réponses, CharlesKinbotisées.