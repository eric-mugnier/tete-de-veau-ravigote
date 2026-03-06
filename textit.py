#!/usr/bin/env python3
"""
Find \textit{...} that are NOT inside \nf{...} in LaTeX files matching acte_\d\d.tex
"""

import re
import sys
from pathlib import Path

# Pattern for \textit{...} (excluding \textit{Source)
TEXTIT_PATTERN = re.compile(r'\\textit\{(?!Source)[^}]*\}')
# File pattern
FILE_PATTERN = re.compile(r'acte_\d\d\.tex$')


def mask_nf_blocks(line: str) -> str:
    """Replace all \nf{...} (with nested braces) with empty string."""
    result = []
    i = 0
    while i < len(line):
        if line[i:].startswith(r'\nf{'):
            # Find the matching closing brace, counting nesting
            depth = 0
            j = i + 3  # position of the opening '{'
            while j < len(line):
                if line[j] == '{':
                    depth += 1
                elif line[j] == '}':
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            i = j  # skip the entire \nf{...}
        else:
            result.append(line[i])
            i += 1
    return ''.join(result)


def find_bare_textit(filepath: Path):
    """Return list of (line_no, match_str) for \textit not inside \nf."""
    results = []
    with open(filepath, encoding='utf-8') as f:
        for line_no, line in enumerate(f, 1):
            masked = mask_nf_blocks(line)
            for m in TEXTIT_PATTERN.finditer(masked):
                results.append((line_no, m.group()))
    return results


def scan_directory(root: str):
    root_path = Path(root)
    files = sorted(p for p in root_path.rglob('*.tex') if FILE_PATTERN.search(p.name))

    if not files:
        print(f"No files matching acte_\\d\\d.tex found under {root}")
        return

    total = 0
    for filepath in files:
        hits = find_bare_textit(filepath)
        if hits:
            print(f"\n{'='*60}")
            print(f"  {filepath}")
            print(f"{'='*60}")
            for line_no, match in hits:
                print(f"  line {line_no:4d}: {match}")
            total += len(hits)

    print(f"\n→ {total} bare \\textit found across {len(files)} file(s).")


if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    scan_directory(directory)