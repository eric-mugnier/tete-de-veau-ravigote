#!/usr/bin/env python3
"""Find titles likely missing \\textit{} wrapping in LaTeX source.

A candidate is: 2–N consecutive words (first word starts uppercase)
that immediately precede \\nf{, are not already wrapped in \\textit{},
and are not inside a \\nf{} block.

Usage:
    python3 find_unwrapped_titles.py [--words N] [--names FILE] [file_or_dir ...]
    python3 find_unwrapped_titles.py --words 5 actes/*.tex
    python3 find_unwrapped_titles.py --names persons_or_not_titles.txt actes/

Defaults: --words 4, scans current directory recursively for *.tex

The --names file contains one name per line (exact match, case-sensitive).
Lines starting with # are ignored. Example:
    Sharon Stone
    Carlos Santana
    # this is a comment
"""

import argparse
import re
from pathlib import Path

# Word characters: letters (incl. accented), apostrophe/right-quote, hyphen
WORD       = r"[A-Za-zÀ-ÿ'\u2019\-]+"   # any word
FIRST_WORD = r"[A-ZÀ-Ö][A-Za-zÀ-ÿ'\u2019\-]*"  # word starting uppercase


# ── helpers ───────────────────────────────────────────────────────────────────

def nf_ranges(text: str) -> list[tuple[int, int]]:
    """Return (start, end) character spans of every \\nf{…} block."""
    spans, i, n = [], 0, len(text)
    while i < n:
        if text[i:i+4] == '\\nf{':
            depth, j = 1, i + 4
            while j < n and depth:
                depth += (text[j] == '{') - (text[j] == '}')
                j += 1
            spans.append((i, j))
            i = j
        else:
            i += 1
    return spans


def inside_any(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(s <= pos < e for s, e in spans)


def already_wrapped(text: str, title_start: int) -> bool:
    """True if the title is still inside an open \\textit{ on the same line."""
    line_start = text.rfind('\n', 0, title_start) + 1
    before = text[line_start:title_start]
    idx = before.rfind('\\textit{')
    if idx == -1:
        return False
    # count net braces after the opening { of \textit{
    depth = 0
    for ch in before[idx + len('\\textit{'):]:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
    return depth >= 0   # still open → title is wrapped


# Person footnotes always start with capitalized name(s) followed by a year:
#   \nf{John Adams (1735--1826), ...}
#   \nf{Wagner (1813--1883), ...}
# Title footnotes never start that way.
_PERSON_NF = re.compile(
    r'[A-ZÀ-Ö][A-Za-zÀ-ÿ\'\-]+'      # first capitalized word
    r'(?:\s+[A-ZÀ-Ö][A-Za-zÀ-ÿ\'\-]+)*'  # optional further capitalized words
    r'\s*\(\d{4}'                          # followed by (year
)

def is_person_name(text: str, match_end: int) -> bool:
    """True if the \\nf{} that follows looks like a person footnote."""
    j = match_end  # points just after the title, before \nf{
    while j < len(text) and text[j] in ' \t':
        j += 1
    if text[j:j+4] != '\\nf{':
        return False
    content = text[j + 4: j + 4 + 80]
    return bool(_PERSON_NF.match(content))


def load_names(path: Path) -> set[str]:
    """Load exclusion names from a plain-text file (one name per line).
    Lines starting with # are treated as comments and ignored.
    """
    names = set()
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            names.add(line)
    return names


def build_pattern(max_words: int) -> re.Pattern:
    # First word must start uppercase; subsequent words: any case.
    title = rf'{FIRST_WORD}(?:[ \t]+{WORD}){{1,{max_words - 1}}}'
    return re.compile(rf'(?P<title>{title})\s*\\nf\{{', re.UNICODE)


# ── scan ──────────────────────────────────────────────────────────────────────

def scan(path: Path, pat: re.Pattern, names: set[str]) -> list[tuple[int, str, str]]:
    text = path.read_text(encoding='utf-8')
    spans = nf_ranges(text)
    source_lines = text.splitlines()
    hits = []
    for m in pat.finditer(text):
        if inside_any(m.start(), spans):
            continue
        if already_wrapped(text, m.start()):
            continue
        if is_person_name(text, m.end() - len('\\nf{')):
            continue
        if m.group('title') in names:
            continue
        lineno = text[:m.start()].count('\n') + 1
        hits.append((lineno, m.group('title'), source_lines[lineno - 1].strip()))
    return hits


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        '--words', type=int, default=4,
        help='max number of words in a title (default: 4)',
    )
    ap.add_argument(
        '--names', type=Path, default=None, metavar='FILE',
        help='file of known person names to exclude (one per line)',
    )
    ap.add_argument(
        'files', nargs='*', default=['.'],
        help='files or directories to scan (*.tex, recursive)',
    )
    args = ap.parse_args()

    names: set[str] = load_names(args.names) if args.names else set()
    pat = build_pattern(args.words)

    paths: list[Path] = []
    for p in map(Path, args.files):
        paths += sorted(p.rglob('*.tex')) if p.is_dir() else [p]

    total = 0
    for path in paths:
        hits = scan(path, pat, names)
        if hits:
            print(f'\n── {path}')
            for lineno, title, line in hits:
                print(f'  {lineno:5d}: {title!r}')
                print(f'         {line[:120]}')
            total += len(hits)

    print(f'\n{total} candidate(s) found.' if total else '\nNo candidates found.')


if __name__ == '__main__':
    main()
