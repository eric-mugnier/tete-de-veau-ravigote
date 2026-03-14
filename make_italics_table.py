"""
make_italics_table.py — génère check_italics.md
Table des titres trouvés sans \\textit dans la prose.
Colonnes : text (contexte), title, todo (à remplir par l'auteur).
"""

import re
from pathlib import Path
from collections import defaultdict

ACTES_DIR = Path(__file__).parent / "actes"
OUT_FILE   = Path(__file__).parent / "check_italics.md"

# Extract title from \nf{... \textit{Title} ...}
NOTE_RE  = re.compile(r'\\nf\{[^}]*?\\textit\{([^}~,(]+)')
# Match title NOT preceded by \textit{
def plain_positions(text, title):
    """Return list of (lineno, excerpt) where title appears without \\textit."""
    results = []
    pattern = re.compile(r'(?<!\\textit\{)' + re.escape(title) + r'\b')
    for m in pattern.finditer(text):
        # exclude occurrences inside \nf{...}
        before = text[:m.start()]
        # count unclosed \nf{ before this position
        in_note = before.count(r'\nf{') > before.count(r'\nf{') - before.count('}')
        lineno = text[:m.start()].count('\n') + 1
        # short excerpt: up to 60 chars centred on match
        start = max(0, m.start() - 30)
        end   = min(len(text), m.end() + 30)
        excerpt = text[start:end].replace('\n', ' ').strip()
        # strip latex commands from excerpt for readability
        excerpt = re.sub(r'\\[a-zA-Z]+\{?', '', excerpt)
        excerpt = excerpt[:80]
        results.append((lineno, excerpt))
    return results

# Collect (file, title) → [(lineno, excerpt), ...]
findings = defaultdict(list)

for tex in sorted(ACTES_DIR.glob("*.tex")):
    text = tex.read_text()
    titles = set(m.group(1).strip() for m in NOTE_RE.finditer(text))
    for title in titles:
        if len(title) <= 3:
            continue
        hits = plain_positions(text, title)
        if hits:
            findings[(tex.name, title)].extend(hits)

# Write markdown table
rows = []
for (fname, title), hits in sorted(findings.items()):
    # Deduplicate by lineno
    seen = {}
    for lineno, excerpt in hits:
        if lineno not in seen:
            seen[lineno] = excerpt
    for lineno, excerpt in sorted(seen.items()):
        rows.append((fname, lineno, title, excerpt))

with OUT_FILE.open("w") as f:
    f.write("# Titres sans \\textit dans la prose\n\n")
    f.write("Remplir la colonne **todo** : `ok` = ajouter `\\textit`, `skip` = laisser tel quel.\n\n")
    f.write("| fichier | ligne | title | text | todo |\n")
    f.write("|---|---|---|---|---|\n")
    for fname, lineno, title, excerpt in rows:
        excerpt_md = excerpt.replace('|', '\\|')
        f.write(f"| {fname} | {lineno} | {title} | {excerpt_md} | |\n")

print(f"  → {OUT_FILE.name} : {len(rows)} entrées")
