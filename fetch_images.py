#!/usr/bin/env python3
"""
fetch_images.py  —  Fetch one image per annotated note in tete_de_veau_ravigote_notes.pdf

Usage:
    python fetch_images.py
    python fetch_images.py --pdf build/tete_de_veau_ravigote_notes.pdf
    python fetch_images.py --dry-run   # extract notes only, no fetch
"""

import argparse
import csv
import re
import sys
import time
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote

import pdfplumber
import requests
from PIL import Image
from slugify import slugify

# ── Credentials (not committed) ───────────────────────────────────────────────
try:
    import config
    GOOGLE_API_KEY = getattr(config, "GOOGLE_API_KEY", None)
    GOOGLE_CX      = getattr(config, "GOOGLE_CX", None)
except ImportError:
    GOOGLE_API_KEY = None
    GOOGLE_CX      = None

# ── Constants ─────────────────────────────────────────────────────────────────
PDF_PATH        = Path("build/tete_de_veau_ravigote_notes.pdf")
IMAGES_DIR      = Path("iconographie")
LOG_PATH        = Path("fetch_log.csv")

GOOGLE_QUOTA    = 100     # max Google API calls per run
_GOOGLE_DISABLED = False  # set True at runtime if credentials rejected
GOOGLE_DELAY    = 1.0     # seconds between Google requests
WIKIMEDIA_DELAY = 2.0     # seconds between Wikimedia requests
MIN_WIDTH       = 800     # minimum acceptable image width (px)
MIN_RATIO       = 0.4     # min width/height (exclude extreme panoramas)
MAX_RATIO       = 2.5     # max width/height (exclude extreme banners)
BAD_FORMATS     = {".svg", ".gif", ".webp", ".bmp", ".ico"}  # skip these
TIMEOUT         = 10      # HTTP timeout (seconds)

LOG_FIELDS = [
    "note_number", "chapter", "subject",
    "status", "source", "image_url", "local_path", "width", "height",
]

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": (
        "TeteDeVeauRavigote-ImageFetcher/1.0 "
        "(academic; github.com/eric-mugnier/tete-de-veau-ravigote)"
    ),
    "Referer": "https://commons.wikimedia.org/",
})


# ── Note extraction ────────────────────────────────────────────────────────────

def extract_notes(pdf_path: Path) -> list[dict]:
    """
    Extract all notes from the notes PDF.

    The PDF format (per page text via pdfplumber) is:
        ActeI
        1. TextBodyMaybeWithoutSpaces
        Source: fr.wikipedia.org/wiki/Title
        2. AnotherNote
        Source: ...

    Note counters reset per chapter, so we use our own sequential numbering.
    Subject is taken from the Wikipedia URL when available (cleanest label),
    otherwise from the first phrase of the note text.

    Returns list of dicts:
        note_number (int, sequential 1..N)
        chapter     (str, e.g. "Acte I")
        full_text   (str)
        source_url  (str or "")
        subject     (str)
    """
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text(layout=False) or ""
            pages_text.append(t)
    raw = "\n".join(pages_text)

    # Normalise line endings
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")

    # Split into raw note blocks.
    # A block starts at "N." at the beginning of a line (after optional whitespace).
    # Chapter headers look like "ActeI", "ActeII", "ActeIII" etc.
    # We process line by line, tracking the current chapter.

    def _roman_to_int(s):
        vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
        s, result = s.upper(), 0
        for i, c in enumerate(s):
            v = vals.get(c, 0)
            result += v if i + 1 == len(s) or vals.get(s[i+1], 0) <= v else -v
        return result

    notes = []
    current_chapter    = ""
    current_chapter_n  = 0   # arabic chapter number (1-based)
    chapter_note_count = 0   # per-chapter note counter
    sequential         = 0   # global unique ID

    # State machine: accumulate lines belonging to the current note
    in_note       = False
    note_lines    = []
    note_src_url  = ""

    def flush_note():
        nonlocal in_note, note_lines, note_src_url, sequential, chapter_note_count
        if not in_note:
            return
        sequential        += 1
        chapter_note_count += 1
        full_text = " ".join(note_lines).strip()
        full_text = re.sub(r"\s*Source\s*[:\s]+\S+\s*$", "", full_text).strip()
        subject = _subject(full_text, note_src_url)
        notes.append({
            "note_number":       sequential,
            "chapter":           current_chapter,
            "chapter_n":         current_chapter_n,
            "chapter_note_n":    chapter_note_count,
            "full_text":         full_text,
            "source_url":        note_src_url,
            "subject":           subject,
        })
        in_note      = False
        note_lines   = []
        note_src_url = ""

    # Patterns
    re_chapter = re.compile(r"^Acte\s*([IVX]+)\s*$", re.IGNORECASE)
    re_note    = re.compile(r"^(\d+)\.\s+(.*)")
    re_source  = re.compile(r"^Source\s*[:\s]+(\S+)", re.IGNORECASE)

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        # Chapter header?
        m_ch = re_chapter.match(line)
        if m_ch:
            flush_note()
            current_chapter    = f"Acte {m_ch.group(1).upper()}"
            current_chapter_n  = _roman_to_int(m_ch.group(1))
            chapter_note_count = 0
            continue

        # Source URL?
        m_src = re_source.match(line)
        if m_src:
            note_src_url = m_src.group(1)
            continue

        # New note?
        m_note = re_note.match(line)
        if m_note:
            flush_note()
            in_note    = True
            note_lines = [m_note.group(2)]
            continue

        # Continuation of current note body
        if in_note:
            note_lines.append(line)

    flush_note()  # last note
    return notes


def _subject(text: str, source_url: str) -> str:
    """
    Return the best searchable label for a note.

    Priority:
    1. Wikipedia article title extracted from the Source URL
       e.g. "fr.wikipedia.org/wiki/Marquis_de_Sade" → "Marquis de Sade"
    2. First phrase of the note text (up to first comma, parenthesis, or period)
    """
    # 1. Wikipedia URL title
    if source_url:
        m = re.search(r"/wiki/([^/?#]+)", source_url)
        if m:
            raw = unquote(m.group(1))
            title = raw.replace("_", " ")
            # Strip disambiguation suffix like "(film)" or "(homme d'État)"
            title = re.sub(r"\s*\([^)]{1,40}\)$", "", title).strip()
            if len(title) >= 3:
                return title

    # 2. First phrase of text
    # Text may lack spaces due to pdfplumber extraction of ligature-heavy fonts.
    # Insert a space before capital letters that follow lowercase (CamelCase fix).
    spaced = re.sub(r"([a-zàâäéèêëïîôùûü])([A-ZÀÂÄÉÈÊËÏÎ])", r"\1 \2", text)
    spaced = re.sub(r"\s+", " ", spaced).strip()
    # Take up to first (, ,, or .
    m2 = re.match(r"^([^(,.\n]{3,80}?)[\s]*[(\n,.]", spaced)
    if m2:
        subject = m2.group(1).strip().rstrip(".")
        if len(subject) >= 3:
            return subject

    # Last resort: first 60 characters trimmed at a word boundary
    if len(spaced) <= 60:
        return spaced
    return spaced[:60].rsplit(" ", 1)[0].rstrip(".,;:")


# ── Image fetching ─────────────────────────────────────────────────────────────

def _get(url: str, **kwargs):
    """GET with timeout. Retries on network errors and 429; immediate fail on other HTTP errors."""
    wait = 30  # initial backoff for 429
    for attempt in range(4):
        try:
            r = SESSION.get(url, timeout=TIMEOUT, **kwargs)
            if r.status_code == 429:
                print(f"      ~ 429 rate-limit — waiting {wait}s …")
                time.sleep(wait)
                wait *= 2
                continue
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as exc:
            # Other HTTP errors (4xx/5xx) are definitive — no retry
            print(f"      ✗ {exc}")
            return None
        except requests.RequestException as exc:
            # Network errors — retry once
            if attempt == 0:
                time.sleep(2)
            else:
                print(f"      ✗ {exc}")
                return None


def _image_dims(data: bytes) -> tuple:
    try:
        img = Image.open(BytesIO(data))
        return img.size  # (width, height)
    except Exception:
        return (0, 0)


def fetch_google(subject: str) -> tuple:
    """
    Try up to 2 queries on Google Custom Search Images.
    Pass 1 : imgType=lineart (drawings, engravings, line art)
    Pass 2 : no imgType restriction (any image, fallback)
    Returns (url, width, height, calls_used) or (None, 0, 0, calls_used).
    """
    global _GOOGLE_DISABLED
    if not GOOGLE_API_KEY or not GOOGLE_CX or _GOOGLE_DISABLED:
        return None, 0, 0, 0

    passes = [
        {"imgType": "lineart"},   # prefer drawings / engravings
        {},                        # fallback: no type restriction
    ]

    calls = 0
    for extra in passes:
        r = _get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key":           GOOGLE_API_KEY,
                "cx":            GOOGLE_CX,
                "searchType":    "image",
                "imgSize":       "LARGE",
                "imgColorType":  "gray",
                "num":           5,
                "q":             subject,
                **extra,
            },
        )
        calls += 1
        if r is None:
            # HTTP error (403/401) or network error — disable Google for this run
            _GOOGLE_DISABLED = True
            print("      ! Google API disabled for this run")
            return None, 0, 0, calls
        for item in r.json().get("items", []):
            info = item.get("image", {})
            w    = info.get("width", 0)
            h    = info.get("height", 0)
            url  = item.get("link", "")
            ext  = "." + url.split("?")[0].rsplit(".", 1)[-1].lower() if "." in url else ""
            if not url or w < MIN_WIDTH:
                continue
            if ext in BAD_FORMATS:
                continue
            if h and not (MIN_RATIO <= w / h <= MAX_RATIO):
                continue
            return url, w, h, calls
        time.sleep(GOOGLE_DELAY)

    return None, 0, 0, calls


def _wikimedia_search_one(query: str) -> str | None:
    """Run a Wikimedia file search and return the title of the first result, or None."""
    r = _get(
        "https://commons.wikimedia.org/w/api.php",
        params={
            "action":      "query",
            "list":        "search",
            "srnamespace": "6",
            "srsearch":    query,
            "srlimit":     1,
            "format":      "json",
        },
    )
    if r is None:
        return None
    results = r.json().get("query", {}).get("search", [])
    return results[0]["title"] if results else None


def fetch_wikimedia(subject: str) -> tuple:
    """
    Search Wikimedia Commons for an image of the given subject.
    Pass 1 : subject + deepcat B&W filter (prefer genuine B&W images).
    Pass 2 : subject only, no color filter (fallback if nothing found).
    Downloads the result once and returns bytes directly (no re-fetch in caller).
    Returns (url, width, height, img_bytes) or (None, 0, 0, None).
    """
    bw_filter = '(deepcat:"Black and white" OR deepcat:"Monochrome photographs")'
    title = _wikimedia_search_one(f"{subject} {bw_filter}")
    if title is None:
        time.sleep(WIKIMEDIA_DELAY)
        title = _wikimedia_search_one(subject)   # fallback: no color filter
    if title is None:
        return None, 0, 0, None

    time.sleep(WIKIMEDIA_DELAY)
    r2 = _get(
        "https://commons.wikimedia.org/w/api.php",
        params={
            "action":     "query",
            "titles":     title,
            "prop":       "imageinfo",
            "iiprop":     "url|size",
            "iiurlwidth": 1200,
            "format":     "json",
        },
    )
    if r2 is None:
        return None, 0, 0, None

    for page in r2.json().get("query", {}).get("pages", {}).values():
        info = (page.get("imageinfo") or [{}])[0]
        url  = info.get("thumburl") or info.get("url")
        w    = info.get("thumbwidth") or info.get("width", 0)
        h    = info.get("thumbheight") or info.get("height", 0)
        if not url:
            return None, 0, 0, None
        ext = "." + url.split("?")[0].rsplit(".", 1)[-1].lower()
        if ext in BAD_FORMATS:
            return None, 0, 0, None
        img_r = _get(url)
        if img_r is None:
            return None, 0, 0, None
        return url, int(w), int(h), img_r.content

    return None, 0, 0, None


def download_image(url: str, dest: Path) -> tuple:
    """Download image to dest. Returns (w, h) or (0, 0) on failure."""
    r = _get(url)
    if r is None:
        return 0, 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(r.content)
    return _image_dims(r.content)


# ── CSV log ────────────────────────────────────────────────────────────────────

def load_log(log_path: Path) -> set:
    """Return set of already-processed note_numbers."""
    done = set()
    if not log_path.exists():
        return done
    with log_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            done.add(int(row["note_number"]))
    return done


def append_log(log_path: Path, row: dict) -> None:
    write_header = not log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if write_header:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in LOG_FIELDS})


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fetch one image per note in the annotated notes PDF."
    )
    parser.add_argument(
        "--pdf", default=str(PDF_PATH),
        help=f"Path to the notes PDF (default: {PDF_PATH})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Extract and print notes only; do not fetch images.",
    )
    args = parser.parse_args()

    pdf = Path(args.pdf)
    if not pdf.exists():
        sys.exit(f"PDF not found: {pdf}")

    # ── Extract ───────────────────────────────────────────────────────────────
    print(f"Extracting notes from {pdf} …")
    notes = extract_notes(pdf)
    print(f"Found {len(notes)} notes.\n")

    if args.dry_run:
        for n in notes:
            print(f"  [{n['note_number']:>3}]  {n['chapter']:<8}  {n['subject']}")
        sys.exit(0)

    # ── First-run preview + confirmation ──────────────────────────────────────
    first_run = not LOG_PATH.exists()
    if first_run:
        print("First 10 extracted subjects:\n")
        for n in notes[:10]:
            print(f"  [{n['note_number']:>3}]  {n['chapter']:<8}  {n['subject']!r}")
        print()
        answer = input("Proceed with fetching? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)
        print()

    # ── Fetch loop ────────────────────────────────────────────────────────────
    IMAGES_DIR.mkdir(exist_ok=True)
    done          = load_log(LOG_PATH)
    google_calls  = 0
    total         = len(notes)
    counts        = {"OK": 0, "FAILED": 0, "SKIPPED": 0}
    sources_count = {"google": 0, "wikimedia": 0}

    for note in notes:
        num     = note["note_number"]
        chapter = note["chapter"]
        subject = note["subject"]
        label   = f"[{num:03d}/{total}] {subject!r}"

        # Already logged?
        if num in done:
            counts["SKIPPED"] += 1
            continue

        # Quota check
        if google_calls >= GOOGLE_QUOTA:
            print("\nDaily quota reached — run again tomorrow.")
            break

        # Destination path
        slug      = slugify(subject, max_length=60)
        ch_n      = note["chapter_n"]
        ch_note_n = note["chapter_note_n"]
        dest = IMAGES_DIR / f"acte_{ch_n:02d}_note_{ch_note_n:03d}_{slug}.jpg"

        # File already on disk?
        if dest.exists():
            print(f"  {label}  → SKIPPED (file exists)")
            append_log(LOG_PATH, {
                "note_number": num, "chapter": chapter, "subject": subject,
                "status": "SKIPPED", "source": "", "image_url": "",
                "local_path": str(dest), "width": "", "height": "",
            })
            counts["SKIPPED"] += 1
            done.add(num)
            continue

        # ── Try Google ────────────────────────────────────────────────────────
        url, w, h, calls_used = fetch_google(subject)
        google_calls += calls_used
        source = "google" if url else None
        img_bytes = None  # Google: bytes fetched later by download_image

        # ── Try Wikimedia fallback ─────────────────────────────────────────────
        if url is None:
            url, w, h, img_bytes = fetch_wikimedia(subject)
            source = "wikimedia" if url else None
            time.sleep(WIKIMEDIA_DELAY)

        # ── No result ─────────────────────────────────────────────────────────
        if url is None:
            print(f"  {label}  → FAILED (no result)")
            append_log(LOG_PATH, {
                "note_number": num, "chapter": chapter, "subject": subject,
                "status": "FAILED", "source": "", "image_url": "",
                "local_path": "", "width": "", "height": "",
            })
            counts["FAILED"] += 1
            done.add(num)
            continue

        # ── Download (or write already-fetched bytes) ─────────────────────────
        if img_bytes is not None:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(img_bytes)
            rw, rh = _image_dims(img_bytes)
        else:
            rw, rh = download_image(url, dest)
        if rw == 0:
            print(f"  {label}  → FAILED (download error)")
            append_log(LOG_PATH, {
                "note_number": num, "chapter": chapter, "subject": subject,
                "status": "FAILED", "source": source, "image_url": url,
                "local_path": "", "width": "", "height": "",
            })
            counts["FAILED"] += 1
        else:
            print(f"  {label}  → OK {source} {rw}×{rh}px")
            append_log(LOG_PATH, {
                "note_number": num, "chapter": chapter, "subject": subject,
                "status": "OK", "source": source, "image_url": url,
                "local_path": str(dest), "width": rw, "height": rh,
            })
            sources_count[source] += 1
            counts["OK"] += 1

        done.add(num)

    # ── Final report ───────────────────────────────────────────────────────────
    print()
    print("─" * 52)
    print(f"  OK       : {counts['OK']}")
    print(f"  FAILED   : {counts['FAILED']}")
    print(f"  SKIPPED  : {counts['SKIPPED']}")
    print(f"  Sources  : Google={sources_count['google']}  "
          f"Wikimedia={sources_count['wikimedia']}")
    print(f"  Google API calls this run : {google_calls}")
    print("─" * 52)


if __name__ == "__main__":
    main()
