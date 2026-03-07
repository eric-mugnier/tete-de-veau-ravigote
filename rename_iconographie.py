#!/usr/bin/env python3
"""
rename_iconographie.py  —  Prefix manually curated images in iconographie_zero/
with note_NNN_ by matching filename to note subjects in the notes PDF.

Usage:
    python rename_iconographie.py           # dry-run (shows proposed renames)
    python rename_iconographie.py --apply   # actually rename
"""

import argparse
import re
from pathlib import Path

import pdfplumber
from slugify import slugify
from urllib.parse import unquote

ICONS_DIR = Path("iconographie_zero")
PDF_PATH  = Path("build/tete_de_veau_ravigote_notes.pdf")

# ── Extract notes from PDF ────────────────────────────────────────────────────

def extract_notes(pdf_path):
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text(layout=False) or ""
            pages_text.append(t)
    raw = "\n".join(pages_text).replace("\r", "\n")

    re_chapter = re.compile(r"^Acte\s*([IVX]+)\s*$", re.IGNORECASE)
    re_note    = re.compile(r"^(\d+)\.\s+(.*)")
    re_source  = re.compile(r"^Source\s*[:\s]+(\S+)", re.IGNORECASE)

    notes = []
    sequential = 0
    in_note, note_lines, note_src = False, [], ""

    def flush():
        nonlocal in_note, note_lines, note_src, sequential
        if not in_note:
            return
        sequential += 1
        subject = _subject(" ".join(note_lines).strip(), note_src)
        notes.append({"num": sequential, "subject": subject})
        in_note, note_lines, note_src = False, [], ""

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if re_chapter.match(line):
            flush()
            continue
        m = re_source.match(line)
        if m:
            note_src = m.group(1)
            continue
        m = re_note.match(line)
        if m:
            flush()
            in_note, note_lines = True, [m.group(2)]
            continue
        if in_note:
            note_lines.append(line)
    flush()
    return notes


def _subject(text, source_url):
    if source_url:
        m = re.search(r"/wiki/([^/?#]+)", source_url)
        if m:
            title = unquote(m.group(1)).replace("_", " ")
            title = re.sub(r"\s*\([^)]{1,40}\)$", "", title).strip()
            if len(title) >= 3:
                return title
    spaced = re.sub(r"([a-zàâäéèêëïîôùûü])([A-ZÀÂÄÉÈÊËÏÎ])", r"\1 \2", text)
    spaced = re.sub(r"\s+", " ", spaced).strip()
    m2 = re.match(r"^([^(,.\n]{3,80}?)[\s]*[(\n,.]", spaced)
    if m2:
        s = m2.group(1).strip().rstrip(".")
        if len(s) >= 3:
            return s
    return spaced[:60].rsplit(" ", 1)[0].rstrip(".,;:")


# ── Match filename to note ────────────────────────────────────────────────────

def normalize(s):
    """Lowercase slug for fuzzy matching."""
    return slugify(s, separator=" ")


def find_match(filename_stem, notes_index):
    """
    Try to match a filename stem to a note subject.
    Returns the note dict or None.
    """
    # Clean up the stem
    stem = re.sub(r"\s*-\s*\d+$", "", filename_stem)   # trailing " - 02"
    stem = re.sub(r"\([^)]*\)", "", stem)               # drop parentheticals
    stem = re.sub(r"([a-z])([A-Z])", r"\1 \2", stem)   # CamelCase → words
    needle = normalize(re.sub(r"[-_]+", " ", stem))

    # 1. exact match
    if needle in notes_index:
        return notes_index[needle]

    # 2. needle contains a note key, or note key contains needle
    for key, note in notes_index.items():
        if key in needle or needle in key:
            return note

    # 3. word overlap (≥ 2 significant words in common, or 1 rare long word)
    STOPWORDS = {"company", "group", "order", "saint", "black", "white",
                 "national", "international", "royal", "grand", "great"}
    needle_words = set(w for w in needle.split() if len(w) > 3 and w not in STOPWORDS)
    n_needle = len(needle_words)
    best, best_score = None, 0
    for key, note in notes_index.items():
        key_words = set(w for w in key.split() if len(w) > 3)
        common = needle_words & key_words
        if not common:
            continue
        max_len   = max(len(w) for w in common)
        n_common  = len(common)
        score     = sum(len(w) for w in common)
        # stricter when needle has many words (avoid single generic word match)
        min_common = 2 if n_needle >= 3 else 1
        if n_common >= min_common or max_len >= 7:
            if score > best_score:
                best, best_score = note, score

    return best


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename files (default: dry-run)")
    args = parser.parse_args()

    print(f"Extracting notes from {PDF_PATH} …")
    notes = extract_notes(PDF_PATH)
    notes_index = {normalize(n["subject"]): n for n in notes}
    print(f"{len(notes)} notes loaded.\n")

    IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".tif", ".tiff"}

    # Files without note_NNN_ prefix
    candidates = sorted(
        f for f in ICONS_DIR.iterdir()
        if f.is_file()
        and f.suffix.lower() in IMAGE_EXTS
        and not re.match(r"note_\d{3}_", f.name)
    )
    print(f"{len(candidates)} files to process:\n")

    renamed, skipped = 0, 0
    for f in candidates:
        stem = re.sub(r"\.[^.]+$", "", f.name)
        note = find_match(stem, notes_index)
        if note:
            slug     = slugify(note["subject"], max_length=60)
            new_name = f"note_{note['num']:03d}_{slug}{f.suffix}"
            new_path = f.parent / new_name
            print(f"  {f.name!r:55s} → {new_name}")
            if args.apply:
                f.rename(new_path)
            renamed += 1
        else:
            print(f"  {f.name!r:55s} → NO MATCH — skipped")
            skipped += 1

    print(f"\n{'Renamed' if args.apply else 'Would rename'}: {renamed}  |  Skipped: {skipped}")
    if not args.apply and renamed:
        print("Run with --apply to perform the renames.")


if __name__ == "__main__":
    main()
