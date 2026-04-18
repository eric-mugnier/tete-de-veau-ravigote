"""
check_unreferenced_images.py — List image files in iconography/ not referenced in any .tex file,
and print all references with their file:line number.
Run: python3 check_unreferenced_images.py
"""

import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent

tex_files = sorted(list((ROOT / "actes").glob("*.tex"))
                   + list((ROOT / "figures").glob("*.tex")))

# collect references with file:line
refs: dict[str, list[str]] = {}  # basename (NFC) -> ["file:line", ...]
for tex in tex_files:
    for lineno, line in enumerate(tex.read_text(encoding="utf-8").splitlines(), 1):
        if re.match(r'\s*%', line):
            continue
        for m in re.finditer(r'\{([^{}]+\.(?:jpg|jpeg|png))\}', line):
            name = unicodedata.normalize('NFC', Path(m.group(1)).name)
            refs.setdefault(name, []).append(
                f"{tex.relative_to(ROOT)}:{lineno}")

# all image files in iconography/
all_images = sorted(
    f for f in (ROOT / "iconography").rglob("*")
    if f.suffix.lower() in {".jpg", ".jpeg", ".png"} and f.is_file()
)

# unreferenced
unreferenced = [
    f for f in all_images
    if unicodedata.normalize('NFC', f.name) not in refs
]

print(f"── {len(all_images)} image files in iconography/")
print(f"── {len(refs)} distinct referenced basenames")
print(f"── {len(unreferenced)} unreferenced\n")

if unreferenced:
    print("UNREFERENCED:")
    for p in unreferenced:
        print(f"  {p.relative_to(ROOT)}")
    print()

# referenced basenames with no matching file in iconography/
existing_names = {unicodedata.normalize('NFC', f.name) for f in all_images}
missing = {name: locs for name, locs in refs.items() if name not in existing_names}
if missing:
    print("MISSING (referenced but not found in iconography/):")
    for name, locs in sorted(missing.items()):
        for loc in locs:
            print(f"  {loc:50s}  {name}")
    print()


print("REFERENCES (file:line → image):")
all_refs = [(loc, name) for name, locations in refs.items() for loc in locations]
all_refs.sort(key=lambda x: (x[0].split(":")[0], int(x[0].split(":")[1])))
for loc, name in all_refs:
    print(f"  {loc:50s}  {name}")

# ── figures/*.tex not referenced from any actes/*.tex ─────────────────────────
actes_text = "\n".join(f.read_text(encoding="utf-8")
                       for f in (ROOT / "actes").glob("*.tex"))
actes_text = re.sub(r'(?m)^[^\S\n]*%.*', '', actes_text)

referenced_figs = set()
for m in re.finditer(r'\\iconographietex(?:pair)?\{([^}]+)\}(?:\{([^}]+)\})?', actes_text):
    for g in filter(None, [m.group(1), m.group(2)]):
        referenced_figs.add(g.strip())

all_figs = sorted((ROOT / "figures").glob("*_fig.tex"))
unused_figs = [f for f in all_figs
               if f"figures/{f.name}" not in referenced_figs
               and str(f.relative_to(ROOT)) not in referenced_figs]

print(f"\n── FIGURES NOT INCLUDED IN DOCUMENT ({len(unused_figs)}/{len(all_figs)}):")
for f in unused_figs:
    print(f"  figures/{f.name}")
