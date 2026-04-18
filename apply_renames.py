"""
apply_renames.py — Rename illustration files and update .tex references.

Mapping file format (one rename per line, comments with #):
  0020 0040      →  rename _0020_* to _0040_* in the scene directory
  0030 0050      →  rename _0030_* to _0050_*

Usage:
  python3 apply_renames.py --scene N --map mapping.txt [--dry-run]

--dry-run prints what would happen without making any changes.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT        = Path(__file__).parent
ICONOGRAPHY = ROOT / "iconography"
ACTES_DIR   = ROOT / "actes"
FIGURES_DIR = ROOT / "figures"

NUM_RE    = re.compile(r'_(\d{4})_')
SCENE_DIR = re.compile(r'scene_(\d+)')


def load_mapping(map_file: Path) -> list[tuple[str, str]]:
    """Return list of (old_prefix, new_prefix) e.g. ('0020', '0040')."""
    mapping = []
    for lineno, line in enumerate(map_file.read_text(encoding="utf-8").splitlines(), 1):
        line = line.split("#")[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
            print(f"  ! line {lineno}: invalid format '{line}' — skipped", file=sys.stderr)
            continue
        mapping.append((f"{int(parts[0]):04d}", f"{int(parts[1]):04d}"))
    return mapping


def find_scene_dirs(scene_num: int) -> list[Path]:
    """Return all iconography subdirectories for this scene number."""
    return [
        d for d in ICONOGRAPHY.rglob(f"scene_{scene_num}")
        if d.is_dir()
    ]


def find_images_with_prefix(dirs: list[Path], prefix: str) -> list[Path]:
    """Return all image files starting with _{prefix}_ in given dirs (recursively)."""
    images = []
    for d in dirs:
        for f in d.rglob("*"):
            if f.is_file() and f.suffix.lower() in {".jpg", ".jpeg", ".png"}:
                if f.name.startswith(f"_{prefix}_"):
                    images.append(f)
    return sorted(images)


def tex_files() -> list[Path]:
    return sorted(ACTES_DIR.glob("*.tex")) + sorted(FIGURES_DIR.glob("*.tex"))


def apply(scene_num: int, mapping: list[tuple[str, str]], dry_run: bool) -> None:
    scene_dirs = find_scene_dirs(scene_num)
    if not scene_dirs:
        print(f"  ! No iconography directory found for scene {scene_num}", file=sys.stderr)
        sys.exit(1)
    print(f"Scene {scene_num} directories: {[str(d.relative_to(ROOT)) for d in scene_dirs]}\n")

    renames: list[tuple[Path, Path]] = []  # (old_path, new_path)

    for old_prefix, new_prefix in mapping:
        images = find_images_with_prefix(scene_dirs, old_prefix)
        if not images:
            print(f"  ! _{old_prefix}_* : no file found — skipped")
            continue
        for img in images:
            new_name = f"_{new_prefix}_" + img.name[6:]   # replace _XXXX_ prefix
            new_path = img.parent / new_name
            renames.append((img, new_path))
            action = "DRY" if dry_run else "mv "
            print(f"  [{action}] {img.relative_to(ROOT)}")
            print(f"        → {new_path.relative_to(ROOT)}")

    if not renames:
        print("Nothing to rename.")
        return

    # ── tex updates ───────────────────────────────────────────────────────────
    tex_changes: list[tuple[Path, str, str]] = []  # (file, old_str, new_str)
    for old_path, new_path in renames:
        old_name = old_path.name
        new_name = new_path.name
        for tex in tex_files():
            content = tex.read_text(encoding="utf-8")
            if old_name in content:
                tex_changes.append((tex, old_name, new_name))
                action = "DRY" if dry_run else "tex"
                print(f"  [{action}] {tex.relative_to(ROOT)} : {old_name} → {new_name}")

    if dry_run:
        print("\n(dry run — no changes made)")
        return

    # ── apply renames ─────────────────────────────────────────────────────────
    for old_path, new_path in renames:
        if new_path.exists():
            print(f"  ! {new_path.name} already exists — skipped", file=sys.stderr)
            continue
        old_path.rename(new_path)

    # ── apply tex updates ─────────────────────────────────────────────────────
    for tex, old_name, new_name in tex_changes:
        content = tex.read_text(encoding="utf-8")
        tex.write_text(content.replace(old_name, new_name), encoding="utf-8")

    print(f"\nDone: {len(renames)} file(s) renamed, {len(tex_changes)} tex reference(s) updated.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", type=int, required=True, help="global scene number")
    parser.add_argument("--map",   type=Path, required=True, help="mapping file")
    parser.add_argument("--dry-run", action="store_true",   help="preview only")
    args = parser.parse_args()

    if not args.map.exists():
        print(f"Mapping file not found: {args.map}", file=sys.stderr)
        sys.exit(1)

    mapping = load_mapping(args.map)
    if not mapping:
        print("Empty mapping — nothing to do.")
        return

    print(f"{'(DRY RUN) ' if args.dry_run else ''}Scene {args.scene} — {len(mapping)} rename(s) from {args.map.name}\n")
    apply(args.scene, mapping, args.dry_run)


if __name__ == "__main__":
    main()
