#!/usr/bin/env python3
"""
Generate a bar chart of illustration density (images per page)
from the compiled PDF, with act/scene boundaries and notes spans
read directly from the PDF bookmarks.

Usage:
    python3 illustration_density.py
    python3 illustration_density.py build/my_other.pdf  # custom PDF path

Output: illustration_density.png (next to this script)

Requirements: pdfimages, pdfinfo (poppler), pymupdf (pip install pymupdf)
"""

import collections
import subprocess
import sys

import fitz  # pymupdf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

PDF_PATH = sys.argv[1] if len(sys.argv) > 1 else 'build/extrait_actes.pdf'

# ── 1. Read bookmarks from PDF ────────────────────────────────────────────────

doc = fitz.open(PDF_PATH)
toc = doc.get_toc()          # [[level, title, page], ...]
total_pages = doc.page_count
doc.close()

acts   = []   # (title, page)
scenes = []   # (title, page)
notes  = []   # page

for level, title, page in toc:
    t = title.strip()
    if level == 1 and t.startswith('Acte'):
        acts.append((t, page))
    elif level >= 2 and t.startswith('Scène'):
        scenes.append((t, page))
    elif t == 'Notes':
        notes.append(page)

print(f"Bookmarks — Acts: {len(acts)}, Scenes: {len(scenes)}, Notes sections: {len(notes)}")

# ── 2. Notes spans: from Notes page to next act/scene/notes start ─────────────

scene_pages = sorted(p for _, p in scenes)

def notes_end(notes_page):
    """Last page of a notes section = page before the next scene starts."""
    candidates = [p for p in scene_pages if p > notes_page]
    return (min(candidates) - 1) if candidates else total_pages

notes_spans = [(p, notes_end(p)) for p in notes]

# ── 3. Count images per page via pdfimages ────────────────────────────────────

result = subprocess.run(
    ['pdfimages', '-list', PDF_PATH],
    capture_output=True, text=True
)
counts = collections.Counter()
for line in result.stdout.splitlines()[2:]:
    parts = line.split()
    if len(parts) < 4:
        continue
    if parts[2] == 'smask':
        continue
    counts[int(parts[0])] += 1

pages  = list(range(1, total_pages + 1))
values = [counts.get(p, 0) for p in pages]

print(f"Pages: {total_pages}  |  Pages with images: {sum(1 for v in values if v > 0)}")
print(f"Max images on one page: {max(values)} (p.{pages[values.index(max(values))]})")

# ── 4. Plot ───────────────────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(18, 4))

# Notes spans — light grey background
for start, end in notes_spans:
    ax.axvspan(start, end + 1, color='lightgrey', alpha=0.6, linewidth=0)

# Image bars
ax.bar(pages, values, width=1.0, color='steelblue', linewidth=0)

top = max(values)

# Scene lines — green
for title, p in scenes:
    num = title.replace('Scène', '').strip()
    ax.axvline(p, color='seagreen', linewidth=0.6, alpha=0.6)
    ax.text(p + 1, top * 0.55, num, color='seagreen', fontsize=6, va='top')

# Act lines — red
for title, p in acts:
    label = title.replace('Acte', '').strip()
    ax.axvline(p, color='crimson', linewidth=1.2, alpha=0.85)
    ax.text(p + 1, top * 0.98, label, color='crimson', fontsize=7,
            va='top', fontweight='bold')

ax.set_xlabel('Page')
ax.set_ylabel('Images per page')
ax.set_title(f'Illustration density — {PDF_PATH}')
ax.set_xlim(1, total_pages)
ax.yaxis.get_major_locator().set_params(integer=True)

legend = [
    Line2D([0], [0], color='crimson',   linewidth=1.5, label='Acte'),
    Line2D([0], [0], color='seagreen',  linewidth=1.0, label='Scène'),
    Patch(facecolor='lightgrey', alpha=0.6,             label='Notes'),
]
ax.legend(handles=legend, fontsize=8, loc='upper right')

plt.tight_layout()
out = 'illustration_density.png'
plt.savefig(out, dpi=150)
print(f"Saved: {out}")
