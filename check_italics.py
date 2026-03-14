#!/usr/bin/env python3
"""
Check that titles found inside \\nf{\\textit{...}} are also italicized
wherever they appear as plain prose in the same file.
"""

import re
import sys
from pathlib import Path

ACTES_DIR = Path(__file__).parent / "actes"

# Match \nf{  ...  \textit{TITLE}  ...
# Capture the title up to the first }, ~, ,, or (
NF_TEXTIT_RE = re.compile(r'\\nf\{[^}]*?\\textit\{([^}~,(]+)')


def find_plain_occurrences(title: str, text: str) -> list[int]:
    """Return line numbers where title appears NOT preceded by \\textit{."""
    results = []
    # Find all occurrences of the literal title string
    for m in re.finditer(re.escape(title), text):
        start = m.start()
        # Look back up to len("\\textit{") chars to see if it's preceded
        prefix_start = max(0, start - len(r'\textit{'))
        prefix = text[prefix_start:start]
        if not prefix.endswith(r'\textit{'):
            line_num = text.count('\n', 0, start) + 1
            results.append(line_num)
    return results


def check_file(path: Path) -> list[str]:
    issues = []
    text = path.read_text(encoding='utf-8')

    # Collect all titles referenced in \nf{\textit{...}}
    titles_seen = set()
    for m in NF_TEXTIT_RE.finditer(text):
        title = m.group(1).strip()
        if len(title) <= 3:
            continue
        titles_seen.add(title)

    for title in sorted(titles_seen):
        plain_lines = find_plain_occurrences(title, text)
        if plain_lines:
            for ln in plain_lines:
                issues.append(f'{path.name}:{ln}: "{title}" found without \\textit')

    return issues


def main():
    tex_files = sorted(ACTES_DIR.glob('*.tex'))
    if not tex_files:
        print(f'No .tex files found in {ACTES_DIR}', file=sys.stderr)
        sys.exit(1)

    all_issues = []
    for path in tex_files:
        all_issues.extend(check_file(path))

    for issue in all_issues:
        print(issue)

    print(f'\n{len(all_issues)} mismatch(es) found across {len(tex_files)} file(s).')


if __name__ == '__main__':
    main()
