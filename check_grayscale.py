"""
check_grayscale.py — list images in iconography/ that are not grayscale.

Usage: python3 check_grayscale.py
"""

from pathlib import Path
from PIL import Image

EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp"}
ROOT = Path(__file__).parent / "iconography"


def is_grayscale(path: Path) -> bool:
    with Image.open(path) as img:
        if img.mode in ("L", "LA", "1"):
            return True
        if img.mode in ("P",):
            img = img.convert("RGB")
        if img.mode in ("RGB", "RGBA"):
            r, g, b = img.convert("RGB").split()[:3]
            return r.tobytes() == g.tobytes() == b.tobytes()
        return False


not_gray = []
for path in sorted(ROOT.rglob("*")):
    if path.suffix.lower() not in EXTS:
        continue
    if "deprecated" in path.parts:
        continue
    stem = path.stem
    if stem.endswith("-original"):
        counterpart = path.with_stem(stem[: -len("-original")])
        if counterpart.exists():
            continue
    try:
        if not is_grayscale(path):
            not_gray.append(path.relative_to(ROOT.parent))
    except Exception as e:
        print(f"  [error] {path.relative_to(ROOT.parent)}: {e}")

if not_gray:
    print(f"{len(not_gray)} non-grayscale image(s):\n")
    for p in not_gray:
        print(f"  {p}")
else:
    print("All images are grayscale.")
