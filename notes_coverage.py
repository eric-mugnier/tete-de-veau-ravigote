#!/usr/bin/env python3
"""
notes_coverage.py — génère notes_coverage.md
Extrait toutes les plages AAAA--AAAA des notes de tous les actes
et produit un graphique Mermaid xychart-beta.
"""

import re
import glob
from collections import defaultdict

# --- collecte des plages ------------------------------------------------

files = sorted(glob.glob('actes/acte_*.tex'))

counts = defaultdict(int)
total_ranges = 0

for path in files:
    with open(path) as f:
        text = f.read()
    for start, end in re.findall(r'(\d{4})--(\d{4})', text):
        for y in range(int(start), int(end) + 1):
            counts[y] += 1
        total_ranges += 1

# --- calcul des bornes et valeurs ---------------------------------------

y_min = min(counts)
y_max = max(counts)
max_val = max(counts.values())
peak_year = max(counts, key=counts.__getitem__)
y_axis_max = round(max_val * 1.1 / 10) * 10   # +10 %, arrondi à la dizaine

years = list(range(y_min, y_max + 1))
values = [counts.get(y, 0) for y in years]

# --- génération du markdown ---------------------------------------------

lines = [
    '```mermaid',
    'xychart-beta',
    f'    title "Couverture temporelle des notes — tous les actes"',
    f'    x-axis "Année" {y_min} --> {y_max}',
    f'    y-axis "Notes actives" 0 --> {y_axis_max}',
    '    bar [' + ', '.join(str(v) for v in values) + ']',
    '```',
    '',
    f'**{total_ranges} plages temporelles** extraites de {len(files)} actes.  ',
    f'**Pic :** {max_val} notes actives simultanées en {peak_year}.',
]

output = '\n'.join(lines) + '\n'

with open('notes_coverage.md', 'w') as f:
    f.write(output)

print(f"notes_coverage.md généré — {len(years)} barres, pic {max_val} en {peak_year}")
