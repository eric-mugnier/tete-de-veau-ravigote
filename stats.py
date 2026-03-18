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
BUILD     = ROOT / "build"
OUT_FILE  = ROOT / "stats.md"

TOC_MAIN   = BUILD / "tete_de_veau_ravigote.toc"
TOC_TOTALE = BUILD / "tete_de_veau_ravigote_LA_TOTALE.toc"
LOG_MAIN   = BUILD / "tete_de_veau_ravigote.log"
LOG_TOTALE = BUILD / "tete_de_veau_ravigote_LA_TOTALE.log"

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

# Actes excluded from all totals and forecasts (rows still displayed)
UNILLUSTRATED = {9}

_ROMAN_VALS = [
    (1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),(90,"XC"),
    (50,"L"),(40,"XL"),(10,"X"),(9,"IX"),(5,"V"),(4,"IV"),(1,"I"),
]

def to_roman(n: int) -> str:
    result = ""
    for value, numeral in _ROMAN_VALS:
        while n >= value:
            result += numeral
            n -= value
    return result


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


def count_dialogue_words(text: str) -> int:
    """Count words inside all \\begin{dialogue}...\\end{dialogue} blocks."""
    blocks = re.findall(r'\\begin\{dialogue\}(.*?)\\end\{dialogue\}', text, re.DOTALL)
    return count_words("".join(blocks))


def count_illus(text: str) -> int:
    total = 0

    # \iconographiedouble contains 2 images
    total += 2 * len(re.findall(r"\\iconographiedouble\b", text))

    # \iconographietex{file}: count \bwimage occurrences inside the referenced file
    for m in re.finditer(r"\\iconographietex\{([^}]+)\}", text):
        fig_path = ROOT / m.group(1)
        if fig_path.exists():
            total += len(re.findall(r"\\bwimage\b", fig_path.read_text(encoding="utf-8")))
        else:
            total += 1  # fallback if file not found

    # single-image commands count as 1 each
    for cmd in [r"\iconographiewrapfig", r"\iconographieinlineblock", r"\iconographieimg"]:
        total += len(re.findall(re.escape(cmd) + r"\b", text))

    return total


def _parse_toc_pages(toc_path: Path) -> list[int]:
    """Return start pages for each \\chapternumberline entry, in document order."""
    if not toc_path.exists():
        return []
    pattern = re.compile(
        r'\\contentsline\s*\{chapter\}\{\\chapternumberline\s*\{\d+\}[^}]*\}\{(\d+)\}'
    )
    return [int(m.group(1)) for m in pattern.finditer(toc_path.read_text(encoding="utf-8"))]


def _pdf_total_pages(log_path: Path) -> int | None:
    """Extract total page count from a LaTeX .log file."""
    if not log_path.exists():
        return None
    m = re.search(r'Output written on .+\((\d+) pages?',
                  log_path.read_text(encoding="utf-8", errors="ignore"))
    return int(m.group(1)) if m else None


def _page_ranges(start_pages: list[int], total_pages: int | None) -> list[tuple[int, int | None]]:
    """Convert a list of chapter start pages to (start_page, num_pages) pairs."""
    result = []
    for i, start in enumerate(start_pages):
        if i + 1 < len(start_pages):
            count = start_pages[i + 1] - start
        elif total_pages is not None:
            count = total_pages - start + 1
        else:
            count = None
        result.append((start, count))
    return result


def _pct(n: int, total: int) -> str:
    return f"{n / total * 100:.2f}%" if total else "—"


def _fmt(n: int) -> str:
    return f"{n:,}".replace(",", "\u202f")  # narrow no-break space


def _load_acte(acte_num: int) -> str:
    """Read and pre-process all source files for an acte."""
    text = "\n".join(
        (ACTES_DIR / f).read_text(encoding="utf-8") for f in ACTES[acte_num]
    )
    return "\n".join(
        ln for ln in text.splitlines()
        if not ln.lstrip().startswith("%%%")
    )


def compute():
    """One row per acte (original chapter structure)."""
    rows = []
    for acte_num in ACTES:
        text  = _load_acte(acte_num)
        rows.append((acte_num, count_words(text), count_notes(text), count_illus(text), count_dialogue_words(text)))
    return rows


def compute_split():
    """One row per segment delimited by \\startnewchapter (split chapter structure)."""
    rows = []
    for acte_num in ACTES:
        text = _load_acte(acte_num)
        # Split line-by-line: only trigger on \startnewchapter not preceded by % on same line
        segments = []
        current: list[str] = []
        for line in text.splitlines(keepends=True):
            if re.match(r"\s*\\startnewchapter\b", line):
                segments.append("".join(current))
                current = []
            else:
                current.append(line)
        segments.append("".join(current))
        acte_label = ROMAN[acte_num]
        for i, seg in enumerate(segments):
            chap_label = acte_label if len(segments) == 1 else acte_label + chr(ord('a') + i)
            rows.append((chap_label, acte_label,
                         count_words(seg), count_notes(seg), count_illus(seg),
                         count_dialogue_words(seg)))
    return rows


def _md_table(rows: list, page_ranges: list | None = None) -> str:
    counted = [r for r in rows if r[0] not in UNILLUSTRATED]
    total_words = sum(r[1] for r in counted)
    total_notes = sum(r[2] for r in counted)
    total_illus = sum(r[3] for r in counted)
    has_pages = bool(page_ranges)

    page_cols = " p. | pp. |" if has_pages else ""
    page_sep  = "---:|----:|" if has_pages else ""
    lines = [
        "# Statistiques par acte\n",
        "Mots = texte original uniquement (hors contenu des notes `\\nf{}`).",
        "% notes et % illustrations = rapport au nombre de mots.\n",
        f"| Acte |{page_cols} Mots | % livre | Notes | % mots | Illustrations | % mots | % dial. |",
        f"|-----:|{page_sep}-----:|--------:|------:|-------:|--------------:|-------:|--------:|",
    ]
    for i, (acte_num, words, notes, illus, dial) in enumerate(rows):
        illus_str = _fmt(illus) if illus else "—"
        illus_pct = _pct(illus, words) if illus else "—"
        if has_pages:
            start_p, num_p = page_ranges[i]
            p_str  = str(start_p) if start_p is not None else "—"
            pp_str = str(num_p)   if num_p  is not None else "—"
            page_part = f" {p_str:>3} | {pp_str:>3} |"
        else:
            page_part = ""
        lines.append(
            f"| {ROMAN[acte_num]:<5}|{page_part} {_fmt(words):>7} | {_pct(words, total_words):>7} "
            f"| {notes:>5} | {_pct(notes, words):>6} "
            f"| {illus_str:>13} | {illus_pct:>6} | {_pct(dial, words):>7} |"
        )
    total_dial = sum(r[4] for r in counted)
    lines.append(
        f"| **Total** |{'  |  |' if has_pages else ''} **{_fmt(total_words)}** | **100%** | **{total_notes}** "
        f"| **{_pct(total_notes, total_words)}** "
        f"| **{_fmt(total_illus)}** | **{_pct(total_illus, total_words)}** "
        f"| **{_pct(total_dial, total_words)}** |"
    )
    return "\n".join(lines) + "\n"


def _md_table_split(rows: list, page_ranges: list | None = None) -> str:
    excl = {ROMAN[n] for n in UNILLUSTRATED}
    counted = [r for r in rows if r[1] not in excl]
    total_words = sum(r[2] for r in counted)
    total_notes = sum(r[3] for r in counted)
    total_illus = sum(r[4] for r in counted)
    has_pages = bool(page_ranges)

    page_cols = " p. | pp. |" if has_pages else ""
    page_sep  = "---:|----:|" if has_pages else ""
    lines = [
        "# Statistiques par chapitre (après découpage)\n",
        "Mots = texte original uniquement (hors contenu des notes `\\nf{}`).",
        "% notes et % illustrations = rapport au nombre de mots.\n",
        f"| Chap. | Acte |{page_cols} Mots | % livre | Notes | % mots | Illustrations | % mots | % dial. |",
        f"|------:|-----:|{page_sep}-----:|--------:|------:|-------:|--------------:|-------:|--------:|",
    ]
    for i, (chap_label, acte_label, words, notes, illus, dial) in enumerate(rows):
        illus_str = _fmt(illus) if illus else "—"
        illus_pct = _pct(illus, words) if illus else "—"
        if has_pages:
            start_p, num_p = page_ranges[i]
            p_str  = str(start_p) if start_p is not None else "—"
            pp_str = str(num_p)   if num_p  is not None else "—"
            page_part = f" {p_str:>3} | {pp_str:>3} |"
        else:
            page_part = ""
        lines.append(
            f"| {chap_label:<6}| {acte_label:<5}|{page_part} {_fmt(words):>7} | {_pct(words, total_words):>7} "
            f"| {notes:>5} | {_pct(notes, words):>6} | {illus_str:>13} | {illus_pct:>6} | {_pct(dial, words):>7} |"
        )
    total_dial = sum(r[5] for r in counted)
    lines.append(
        f"| **Total** | |{'  |  |' if has_pages else ''} **{_fmt(total_words)}** | **100%** | **{total_notes}** "
        f"| **{_pct(total_notes, total_words)}** "
        f"| **{_fmt(total_illus)}** | **{_pct(total_illus, total_words)}** "
        f"| **{_pct(total_dial, total_words)}** |"
    )
    return "\n".join(lines) + "\n"


def _illus_forecast(rows_orig) -> str:
    """Estimate remaining illustration work based on completed actes."""
    counted = [r for r in rows_orig if r[0] not in UNILLUSTRATED]
    with_illus = [(words, illus) for _, words, _, illus, _ in counted if illus > 0]
    if not with_illus:
        return ""

    ratio = sum(i for _, i in with_illus) / sum(w for w, _ in with_illus)

    total_words = sum(r[1] for r in counted)
    total_illus = sum(r[3] for r in counted)
    estimated   = round(ratio * total_words)
    remaining   = max(0, estimated - total_illus)
    pct_done    = total_illus / estimated * 100 if estimated else 0

    n_done  = len(with_illus)
    n_total = len(counted)

    return (
        f"\n## Estimation illustrations restantes\n\n"
        f"Ratio sur les **{n_done}/{n_total}** actes illustrés : "
        f"**1 illustration tous les {round(1/ratio):.0f} mots**.  \n"
        f"Extrapolé à l'ensemble ({_fmt(total_words)} mots) : "
        f"**{estimated}** illustrations estimées.  \n"
        f"Actuellement **{total_illus}** — "
        f"il en manque **{remaining}** — "
        f"**{pct_done:.1f} %** réalisé.\n"
    )


def _print_rows(rows_orig, rows_split):
    for acte_num, words, notes, illus, dial in rows_orig:
        print(f"     Acte {ROMAN[acte_num]:<4} {_fmt(words):>8} mots  "
              f"{notes:>4} notes ({_pct(notes, words)})  "
              f"{illus:>3} illus ({_pct(illus, words)})  "
              f"dial. {_pct(dial, words)}")
    total_words = sum(r[1] for r in rows_orig)
    total_notes = sum(r[2] for r in rows_orig)
    total_illus = sum(r[3] for r in rows_orig)
    total_dial  = sum(r[4] for r in rows_orig)
    print(f"     {'Total':<9} {_fmt(total_words):>8} mots  "
          f"{total_notes:>4} notes ({_pct(total_notes, total_words)})  "
          f"{total_illus:>3} illus ({_pct(total_illus, total_words)})  "
          f"dial. {_pct(total_dial, total_words)}")

    if len(rows_split) != len(rows_orig):
        print()
        for chap_label, acte_label, words, notes, illus, dial in rows_split:
            print(f"     Chap. {chap_label:<5}(acte {acte_label}) {_fmt(words):>8} mots  "
                  f"{notes:>4} notes ({_pct(notes, words)})  "
                  f"{illus:>3} illus ({_pct(illus, words)})  "
                  f"dial. {_pct(dial, words)}")


def main():
    rows_orig  = compute()
    rows_split = compute_split()

    pages_main   = _parse_toc_pages(TOC_MAIN)
    pages_totale = _parse_toc_pages(TOC_TOTALE)
    pr_orig  = _page_ranges(pages_main,   _pdf_total_pages(LOG_MAIN))   if pages_main   else None
    pr_split = _page_ranges(pages_totale, _pdf_total_pages(LOG_TOTALE)) if pages_totale else None

    # Sanity check: warn if TOC chapter count doesn't match row count
    if pr_orig  and len(pr_orig)  != len(rows_orig):
        print(f"  ! pages_main mismatch: {len(pr_orig)} toc entries vs {len(rows_orig)} rows")
        pr_orig = None
    if pr_split and len(pr_split) != len(rows_split):
        print(f"  ! pages_totale mismatch: {len(pr_split)} toc entries vs {len(rows_split)} rows")
        pr_split = None

    md = (_md_table(rows_orig, pr_orig) + "\n"
          + _md_table_split(rows_split, pr_split)
          + _illus_forecast(rows_orig))
    OUT_FILE.write_text(md, encoding="utf-8")
    print(f"  → {OUT_FILE.relative_to(ROOT)}")
    _print_rows(rows_orig, rows_split)
    forecast = _illus_forecast(rows_orig)
    if forecast:
        print(forecast)


if __name__ == "__main__":
    main()
