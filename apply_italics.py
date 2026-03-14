"""
apply_italics.py — lit check_italics.md et applique les \textit dans les .tex.

todo rules:
  empty / blank → skip
  x             → wrap the title in \textit{} before \nf{
  **alt text**  → wrap alt text (a wider span) in \textit{} before \nf{
"""

import re
from pathlib import Path

ACTES_DIR = Path(__file__).parent / "actes"
TABLE     = Path(__file__).parent / "check_italics.md"

def parse_table(path):
    rows = []
    for line in path.read_text().splitlines():
        if not line.startswith('|') or line.startswith('|---') or 'fichier' in line:
            continue
        cols = [c.strip() for c in line.strip('|').split('|')]
        if len(cols) < 5:
            continue
        fname, lineno, title, _, todo = cols[0], int(cols[1]), cols[2], cols[3], cols[4]
        todo = todo.strip()
        if not todo:
            continue
        # Check for alternate text **some text**
        alt = re.search(r'\*\*(.+?)\*\*', todo)
        target = alt.group(1).strip() if alt else title
        rows.append((fname, lineno, target))
    return rows

def apply_fix(tex_path, lineno, target):
    text = tex_path.read_text()
    lines = text.splitlines(keepends=True)

    pattern = re.compile(r'(?<!\\textit\{)' + re.escape(target) + r'(?=\\nf\{)')
    replacement = r'\\textit{' + target + r'}'

    # Try to apply near the specified line first (±3 lines), then globally
    lo, hi = max(0, lineno - 4), min(len(lines), lineno + 3)
    chunk = ''.join(lines[lo:hi])
    new_chunk, n = pattern.subn(replacement, chunk)
    if n:
        lines[lo:hi] = [new_chunk]
        tex_path.write_text(''.join(lines))
        return True

    # Fallback: global replace (e.g. line number slightly off)
    new_text, n = pattern.subn(replacement, text)
    if n:
        tex_path.write_text(new_text)
        return True

    return False

rows = parse_table(TABLE)
applied, failed = [], []

for fname, lineno, target in rows:
    tex_path = ACTES_DIR / fname
    if not tex_path.exists():
        failed.append((fname, lineno, target, 'file not found'))
        continue
    ok = apply_fix(tex_path, lineno, target)
    if ok:
        applied.append((fname, lineno, target))
    else:
        failed.append((fname, lineno, target, 'pattern not found'))

print(f"\n✓ Applied : {len(applied)}")
for fname, lineno, target in applied:
    print(f"  {fname}:{lineno}  {target}")

if failed:
    print(f"\n✗ Failed  : {len(failed)}")
    for fname, lineno, target, reason in failed:
        print(f"  {fname}:{lineno}  {target}  ({reason})")
