#!/usr/bin/env python3
"""
Generate a bar chart of illustration density (images per page)
from the compiled PDF, with act and scene boundaries overlaid.

Usage:
    python3 illustration_density.py
    python3 illustration_density.py build/my_other.pdf  # custom PDF path

Output: illustration_density.png (next to this script)
"""

import collections
import re
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PDF_PATH = sys.argv[1] if len(sys.argv) > 1 else 'build/extrait_actes.pdf'
TOC_PATH = str(Path(PDF_PATH).with_suffix('.toc'))

ROMAN = ['I','II','III','IV','V','VI','VII','VIII','IX','X']

# --- parse act and scene start pages from TOC ---
def parse_toc(toc_path):
    toc = Path(toc_path).read_text(encoding='utf-8')
    acts   = [int(m.group(1)) for m in re.finditer(r'Acte~[IVXLC]+\}\{(\d+)\}', toc)]
    scenes = [int(m.group(1)) for m in re.finditer(r'\\chapternumberline\s*\{[^}]+\}\}\{(\d+)\}', toc)]
    return acts, scenes

acts, scenes = parse_toc(TOC_PATH)

# --- get total page count ---
info = subprocess.run(['pdfinfo', PDF_PATH], capture_output=True, text=True)
total_pages = 1
for line in info.stdout.splitlines():
    if line.startswith('Pages:'):
        total_pages = int(line.split()[1])
        break

# --- parse pdfimages -list ---
result = subprocess.run(
    ['pdfimages', '-list', PDF_PATH],
    capture_output=True, text=True
)
counts = collections.Counter()
for line in result.stdout.splitlines()[2:]:   # skip 2 header lines
    parts = line.split()
    if len(parts) < 4:
        continue
    if parts[2] == 'smask':          # skip alpha masks (not standalone images)
        continue
    page = int(parts[0])
    counts[page] += 1

pages  = list(range(1, total_pages + 1))
values = [counts.get(p, 0) for p in pages]

print(f"PDF:   {PDF_PATH}")
print(f"Pages: {total_pages}")
print(f"Pages with images: {sum(1 for v in values if v > 0)}")
print(f"Max images on a single page: {max(values)} (page {pages[values.index(max(values))]})")

# --- plot ---
fig, ax = plt.subplots(figsize=(18, 4))
ax.bar(pages, values, width=1.0, color='steelblue', linewidth=0)

top = max(values)

# scene lines — green, thin, label near bottom
for i, p in enumerate(scenes, 1):
    ax.axvline(p, color='seagreen', linewidth=0.6, alpha=0.6)
    ax.text(p + 1, top * 0.55, str(i),
            color='seagreen', fontsize=6, va='top')

# act lines — red, thicker, label near top
for i, p in enumerate(acts):
    ax.axvline(p, color='crimson', linewidth=1.2, alpha=0.85)
    ax.text(p + 1, top * 0.98, ROMAN[i],
            color='crimson', fontsize=7, va='top', fontweight='bold')

ax.set_xlabel('Page')
ax.set_ylabel('Images per page')
ax.set_title(f'Illustration density — {PDF_PATH}')
ax.set_xlim(1, total_pages)
ax.yaxis.get_major_locator().set_params(integer=True)

# legend
from matplotlib.lines import Line2D
legend = [
    Line2D([0], [0], color='crimson',  linewidth=1.5, label='Acte'),
    Line2D([0], [0], color='seagreen', linewidth=1.0, label='Scène'),
]
ax.legend(handles=legend, fontsize=8, loc='upper right')

plt.tight_layout()
out = 'illustration_density.png'
plt.savefig(out, dpi=150)
print(f"Saved: {out}")
