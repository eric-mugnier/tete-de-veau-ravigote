"""
check_illus_notes.py — Check that illustration filenames match the notes they reference.

Convention:
  _0000_name  → no note reference (skipped)
  _NNNN_name  where NNNN % 10 == 0  → refers to note #NNNN/10 in the scene
  _NNNN_name  where NNNN % 10 != 0  → between notes, no specific note (skipped)

Source of truth: build/extrait.pdf (notes appear after each scene).

Run:
  python3 check_illus_notes.py [--scene N] [--no-ok] [--suggest-renames]
"""

import argparse
import re
import subprocess
from pathlib import Path

ROOT        = Path(__file__).parent
DEFAULT_PDF = ROOT / "build" / "extrait.pdf"
ICONOGRAPHY = ROOT / "iconography"

STOPWORDS = {
    "de", "du", "la", "le", "les", "et", "en", "un", "une", "des",
    "au", "aux", "sur", "par", "pour", "dans", "avec", "the", "of",
    "von", "van", "der", "dit", "dite",
}

NUM_RE   = re.compile(r'_(\d{4})_')
SCENE_RE = re.compile(r'scene_(\d+)')


# ── PDF extraction ────────────────────────────────────────────────────────────

def extract_text(pdf: Path) -> str:
    return subprocess.run(
        ["pdftotext", str(pdf), "-"],
        capture_output=True, text=True, check=True
    ).stdout


# ── Notes parsing ─────────────────────────────────────────────────────────────

def parse_notes(text: str) -> dict[int, dict[int, str]]:
    """Return {scene_num: {note_num: note_text}}."""
    scene_notes: dict[int, dict[int, str]] = {}

    header_re = re.compile(r'[\f\n]+(\d+)\n\nNotes\n')
    headers   = list(header_re.finditer(text))

    for i, m in enumerate(headers):
        scene_num   = int(m.group(1))
        block_start = m.end()
        block_end   = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        block       = text[block_start:block_end]

        note_re = re.compile(r'(?m)^(\d+)\.\s')
        parts   = note_re.split(block)
        notes: dict[int, str] = {}
        for j in range(1, len(parts) - 1, 2):
            num     = int(parts[j])
            content = parts[j + 1]
            content = re.sub(r'\n\d+\n', ' ', content)
            content = re.sub(r'\s+', ' ', content).strip()
            notes[num] = content

        scene_notes[scene_num] = notes

    return scene_notes


# ── Keyword helpers ───────────────────────────────────────────────────────────

def keywords_from_name(name: str) -> list[str]:
    stem = NUM_RE.sub('', Path(name).stem).strip('-_')
    return [
        w.lower() for w in re.split(r'[-_()\s]+', stem)
        if len(w) > 2 and w.lower() not in STOPWORDS
    ]


def find_matching_notes(name: str, notes: dict[int, str]) -> list[int]:
    """Return all note numbers whose text contains a keyword from the filename."""
    kws = keywords_from_name(name)
    matches = []
    for note_num, note_text in notes.items():
        note_lower = note_text.lower()
        if any(kw in note_lower for kw in kws):
            matches.append(note_num)
    return sorted(matches)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf",             type=Path, default=DEFAULT_PDF)
    parser.add_argument("--scene",           type=int,  default=None,
                        help="restrict to a single scene number")
    parser.add_argument("--no-ok",           action="store_true",
                        help="hide OK results")
    parser.add_argument("--suggest-renames", action="store_true",
                        help="for CHECK entries search all notes and suggest mv commands")
    args = parser.parse_args()

    print(f"Extracting text from {args.pdf.name} …")
    text        = extract_text(args.pdf)
    scene_notes = parse_notes(text)
    print(f"  {len(scene_notes)} scenes with notes found.\n")

    results = []

    for img in sorted(ICONOGRAPHY.rglob("*")):
        if img.suffix.lower() not in {".jpg", ".jpeg", ".png"} or not img.is_file():
            continue

        num_m = NUM_RE.search(img.name)
        if not num_m:
            continue
        nnnn = int(num_m.group(1))
        if nnnn == 0 or nnnn % 10 != 0:
            continue

        note_num  = nnnn // 10
        scene_m   = SCENE_RE.search(str(img))
        if not scene_m:
            continue
        scene_num = int(scene_m.group(1))

        if args.scene is not None and scene_num != args.scene:
            continue

        if scene_num not in scene_notes:
            results.append((scene_num, note_num, img, "", "SCENE NOT FOUND", []))
            continue

        notes = scene_notes[scene_num]
        if note_num not in notes:
            results.append((scene_num, note_num, img, "", "NOTE NOT FOUND", []))
            continue

        note_text = notes[note_num]
        kws       = keywords_from_name(img.name)
        matched   = [kw for kw in kws if kw in note_text.lower()]
        status    = "OK" if matched else "CHECK"
        results.append((scene_num, note_num, img, note_text, status, []))

    # ── Report ────────────────────────────────────────────────────────────────
    ok        = sum(1 for r in results if r[4] == "OK")
    check     = sum(1 for r in results if r[4] == "CHECK")
    not_found = sum(1 for r in results if r[4] not in {"OK", "CHECK"})

    W = 100
    print("─" * W)
    print(f"  {len(results)} images checked  |  {ok} OK  |  {check} CHECK  |  {not_found} NOT FOUND")
    print("─" * W)

    rename_cmds = []

    for scene_num, note_num, img, note_text, status, _ in results:
        if args.no_ok and status == "OK":
            continue

        marker = "" if status == "OK" else " ◀"
        print(f"\n[{status}]{marker}")
        print(f"  scene {scene_num:2d}  note {note_num:3d}  {img.name}")
        if status != "OK":
            print(f"  note : {note_text[:200]}")

        if args.suggest_renames and status == "CHECK":
            notes      = scene_notes.get(scene_num, {})
            candidates = find_matching_notes(img.name, notes)
            if len(candidates) == 1:
                new_num  = candidates[0] * 10
                new_name = NUM_RE.sub(f"_{new_num:04d}_", img.name)
                new_path = img.parent / new_name
                print(f"  → rename to note {candidates[0]}  :  {new_name}")
                rename_cmds.append(f"mv '{img}' '{new_path}'")
            elif len(candidates) > 1:
                print(f"  → multiple candidates: notes {candidates} — manual decision needed")
            else:
                print(f"  → no keyword match found in any note — manual decision needed")

    if rename_cmds:
        print(f"\n{'─' * W}")
        print(f"# Suggested renames for scene {args.scene} — review before running:\n")
        for cmd in rename_cmds:
            print(cmd)


if __name__ == "__main__":
    main()
