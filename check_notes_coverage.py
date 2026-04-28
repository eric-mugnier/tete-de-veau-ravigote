#!/usr/bin/env python3
"""
notes_coverage.py — génère notes_coverage.md, notes_coverage.pdf, notes_coverage.jpg
Extrait toutes les plages AAAA--AAAA (et AAAA--AAAA av. J.-C.) des notes
de tous les actes et produit un graphique Mermaid xychart-beta + matplotlib.

Conventions :
  - av. J.-C. → années négatives  (ex. 384--322 av. J.-C. → −384 à −322)
  - AD        → années positives  (ex. 1743--1826)
"""

import re
import glob
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Plages av. J.-C. : AAAA--AAAA suivi de "av" (av. J.-C. / av.\ J.-C.)
BC_PAT = re.compile(r'(\d+)--(\d+)\s*av[.\\]')
# Plages AD : exactement 4 chiffres des deux côtés
AD_PAT = re.compile(r'(\d{4})--(\d{4})')


def extract_ranges(text):
    """Retourne une liste de tuples (lo, hi) en années astronomiques."""
    ranges = []
    bc_spans = set()

    for m in BC_PAT.finditer(text):
        a, b = int(m.group(1)), int(m.group(2))
        lo, hi = min(-a, -b), max(-a, -b)   # ex. −384 à −322
        ranges.append((lo, hi))
        bc_spans.update(range(m.start(), m.end()))

    for m in AD_PAT.finditer(text):
        # ignorer les positions déjà traitées comme av. J.-C.
        if not bc_spans.intersection(range(m.start(), m.end())):
            a, b = int(m.group(1)), int(m.group(2))
            ranges.append((min(a, b), max(a, b)))

    return ranges


# ── collecte ────────────────────────────────────────────────────────────────

files = sorted(glob.glob('actes/acte_*.tex'))

counts = defaultdict(int)
total_ranges = 0
total_notes  = 0

for path in files:
    with open(path) as f:
        text = f.read()
    total_notes += text.count(r'\nf{')
    for lo, hi in extract_ranges(text):
        for y in range(lo, hi + 1):
            counts[y] += 1
        total_ranges += 1

# ── axes ─────────────────────────────────────────────────────────────────────

x_min      = min(counts)
x_max      = max(counts)
x_max_disp = 2050
max_val    = max(counts.values())
peak_year  = max(counts, key=counts.__getitem__)
y_axis_max = round(max_val * 1.1 / 10) * 10   # +10 %, arrondi à la dizaine

years  = list(range(x_min, x_max + 1))
values = [counts.get(y, 0) for y in years]

# ── markdown ─────────────────────────────────────────────────────────────────

lines = [
    '```mermaid',
    'xychart-beta',
    '    title "Couverture temporelle des notes — tous les actes"',
    f'    x-axis "Année" {x_min} --> {x_max}',
    f'    y-axis "Notes actives" 0 --> {y_axis_max}',
    '    bar [' + ', '.join(str(v) for v in values) + ']',
    '```',
    '',
    f'**{total_notes} notes au total** ({total_ranges} avec plages temporelles).  ',
    f'**Pic :** {max_val} notes actives simultanées en {peak_year}.',
]

with open('notes_coverage.md', 'w') as f:
    f.write('\n'.join(lines) + '\n')

print(f'notes_coverage.md généré — {len(years)} barres, pic {max_val} en {peak_year}')
print(f'  Plage : {x_min} → {x_max}  ({total_ranges} plages dans {len(files)} actes)')

# ── matplotlib ───────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(18, 7))

ax.fill_between(years, values, step='mid', alpha=0.85, color='steelblue')
ax.step(years, values, where='mid', color='steelblue', linewidth=0.4)

ax.set_title('Couverture temporelle des notes — tous les actes', fontsize=14, pad=12)
ax.set_xlabel('Année', fontsize=11)
ax.set_ylabel('Notes actives', fontsize=11)
ax.set_xlim(x_min, x_max_disp)
ax.set_ylim(0, y_axis_max)
ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(100))
ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.4)
ax.axhline(0, color='black', linewidth=0.6)

# annotation pic : texte au-dessus, flèche pointant vers le bas
ax.annotate(f'pic : {max_val} ({peak_year})',
            xy=(peak_year, max_val),
            xytext=(peak_year - 250, max_val * 0.82),
            arrowprops=dict(arrowstyle='->', color='dimgray', lw=1.2),
            fontsize=9, color='dimgray',
            ha='right')


caption = (f'{total_notes} notes au total  ({total_ranges} avec plages temporelles)  —  '
           f'pic : {max_val} notes actives simultanées en {peak_year}')
fig.text(0.5, 0.01, caption, ha='center', fontsize=8, color='dimgray')

plt.tight_layout(rect=[0, 0.03, 1, 1])

fig.savefig('notes_coverage.pdf', dpi=150)
fig.savefig('notes_coverage.jpg', dpi=150)
plt.close()

print('notes_coverage.pdf et notes_coverage.jpg générés')
