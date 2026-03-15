"""
stats.py — Word / note / illustration counts per acte.

Writes stats.md at the project root.
Run standalone:  python3 stats.py
Or via invoke:   inv stats
"""

import re
from pathlib import Path

ROOT      = Path(__file__).parent
ACTES_DIR = ROOT / "actes"
OUT_FILE  = ROOT / "stats.md"

# Acte number → list of source files (relative to ACTES_DIR)
ACTES = {
    1: ["acte_01.tex"],
    2: ["acte_02.tex"],
    3: ["acte_03.tex"],
    4: ["acte_04.tex"],
    5: ["acte_05.tex"],
    6: ["acte_06_1.tex", "acte_06_2.tex"],
    7: ["acte_07.tex"],
    8: ["acte_08.tex"],
    9: ["acte_09_1.tex", "acte_09_2.tex", "acte_09_2b.tex",
        "acte_09_3.tex", "acte_09_3b.tex", "acte_09_4.tex"],
}

ROMAN = {1:"I", 2:"II", 3:"III", 4:"IV", 5:"V",
         6:"VI", 7:"VII", 8:"VIII", 9:"IX"}

ILLUS_CMDS = [
    r"\iconographiewrapfig",
    r"\iconographieinlineblock",
    r"\iconographietex",
    r"\iconographiedouble",
    r"\iconographieimg",
]


def _remove_balanced(text: str, cmd: str) -> str:
    """Remove all occurrences of cmd{...} handling nested braces."""
    result = []
    i = 0
    pattern = cmd + "{"
    while i < len(text):
        idx = text.find(pattern, i)
        if idx == -1:
            result.append(text[i:])
            break
        result.append(text[i:idx])
        j = idx + len(pattern)  # character after the opening {
        depth = 1
        while j < len(text) and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        i = j
    return "".join(result)


def count_words(text: str) -> int:
    """Strip note and illustration content, then count words in plain prose."""
    text = _remove_balanced(text, r"\nf")
    text = _remove_balanced(text, r"\source")
    for cmd in [r"\iconographiewrapfig", r"\iconographieinlineblock",
                r"\iconographietex",    r"\iconographiedouble",
                r"\iconographieimg",    r"\bwimage",
                r"\nfimg",             r"\nfimgblock"]:
        text = _remove_balanced(text, cmd)
    text = re.sub(r"\\[a-zA-Z]+\*?\{[^}]*\}", " ", text)   # simple {arg} commands
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)             # bare commands
    text = re.sub(r"%.*", "", text)                          # TeX comments
    text = re.sub(r"[{}~]", " ", text)
    return len(re.findall(r"[a-zA-ZÀ-ÿ'\u2019\-]{2,}", text))


def count_notes(text: str) -> int:
    return len(re.findall(r"\\nf\{", text))


def count_illus(text: str) -> int:
    return sum(
        len(re.findall(re.escape(cmd) + r"\b", text))
        for cmd in ILLUS_CMDS
    )


def _pct(n: int, total: int) -> str:
    return f"{n / total * 100:.2f}%" if total else "—"


def _fmt(n: int) -> str:
    return f"{n:,}".replace(",", "\u202f")  # narrow no-break space


def compute():
    rows = []
    for acte_num, files in ACTES.items():
        text = "\n".join(
            (ACTES_DIR / f).read_text(encoding="utf-8") for f in files
        )
        # Drop commented-out lines (%%%)
        text = "\n".join(
            ln for ln in text.splitlines()
            if not ln.lstrip().startswith("%%%")
        )
        words = count_words(text)
        notes = count_notes(text)
        illus = count_illus(text)
        rows.append((acte_num, words, notes, illus))

    return rows


def _md_table(rows: list) -> str:
    total_words = sum(r[1] for r in rows)
    total_notes = sum(r[2] for r in rows)
    total_illus = sum(r[3] for r in rows)

    lines = [
        "# Statistiques par acte\n",
        "Mots = texte original uniquement (hors contenu des notes `\\nf{}`).",
        "% notes et % illustrations = rapport au nombre de mots.\n",
        "| Acte | Mots | Notes | % mots | Illustrations | % mots |",
        "|-----:|-----:|------:|-------:|--------------:|-------:|",
    ]
    for acte_num, words, notes, illus in rows:
        illus_str = _fmt(illus)  if illus else "—"
        illus_pct = _pct(illus, words) if illus else "—"
        lines.append(
            f"| {ROMAN[acte_num]:<5}| {_fmt(words):>7} | {notes:>5} | {_pct(notes, words):>6} "
            f"| {illus_str:>13} | {illus_pct:>6} |"
        )
    lines.append(
        f"| **Total** | **{_fmt(total_words)}** | **{total_notes}** "
        f"| **{_pct(total_notes, total_words)}** "
        f"| **{_fmt(total_illus)}** | **{_pct(total_illus, total_words)}** |"
    )
    return "\n".join(lines) + "\n"


def main():
    rows = compute()
    md = _md_table(rows)
    OUT_FILE.write_text(md, encoding="utf-8")
    print(f"  → {OUT_FILE.relative_to(ROOT)}")
    for acte_num, words, notes, illus in rows:
        print(f"     Acte {ROMAN[acte_num]:<4} {_fmt(words):>8} mots  "
              f"{notes:>4} notes ({_pct(notes, words)})  "
              f"{illus:>3} illus ({_pct(illus, words)})")
    total_words = sum(r[1] for r in rows)
    total_notes = sum(r[2] for r in rows)
    total_illus = sum(r[3] for r in rows)
    print(f"     {'Total':<9} {_fmt(total_words):>8} mots  "
          f"{total_notes:>4} notes ({_pct(total_notes, total_words)})  "
          f"{total_illus:>3} illus ({_pct(total_illus, total_words)})")


if __name__ == "__main__":
    main()
