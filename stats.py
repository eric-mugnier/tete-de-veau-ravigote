"""
stats.py — Word / note / illustration counts per acte.

Writes stats.md at the project root.
Run standalone:  python3 stats.py
Or via invoke:   inv stats
"""

import argparse
import re
from pathlib import Path

ROOT      = Path(__file__).parent
ACTES_DIR = ROOT / "actes"
BUILD     = ROOT / "build"
OUT_FILE  = ROOT / "stats.md"

ILLUS_TARGET = 417  # target: 1 illustration every N words (overridable via --target)

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


def first_words(text: str, n: int = 7) -> str:
    """Return the first n prose words of a segment, stripped of LaTeX."""
    text = _remove_balanced(text, r"\nf")
    text = _remove_balanced(text, r"\source")
    # Strip optional [...] args immediately before { so cmd[...]{...} becomes cmd{...}
    text = re.sub(r"\[[^\]]*\](?=\s*\{)", "", text)
    for cmd in [r"\iconographiewrapfig", r"\iconographieinlineblock",
                r"\iconographietex",    r"\iconographiedouble",
                r"\iconographieimg",    r"\bwimage",
                r"\nfimg",             r"\nfimgblock"]:
        text = _remove_balanced(text, cmd)
    # Strip all remaining brace groups iteratively (handles orphaned multi-arg command args)
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"\{[^{}]*\}", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"[{}~«»]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    matches = list(re.finditer(r"[a-zA-ZÀ-ÿ'\u2019\-]+", text))
    if not matches:
        return ""
    if len(matches) <= n:
        return text[:matches[-1].end()].strip()
    return text[:matches[n - 1].end()].strip() + "…"


def count_notes(text: str) -> int:
    return len(re.findall(r"\\nf\{", text))


def count_dialogue_words(text: str) -> int:
    """Count words inside all \\begin{dialogue}...\\end{dialogue} blocks."""
    blocks = re.findall(r'\\begin\{dialogue\}(.*?)\\end\{dialogue\}', text, re.DOTALL)
    return count_words("".join(blocks))


def count_illus(text: str) -> int:
    total = 0

    # \iconographiedouble contains 2 images, \iconographietriple contains 3
    total += 2 * len(re.findall(r"\\iconographiedouble\b", text))
    total += 3 * len(re.findall(r"\\iconographietriple\b", text))

    # \iconographietex{file} and \iconographietexpair{file1}{file2}:
    # count \bwimage occurrences inside each referenced file
    for m in re.finditer(r"\\iconographietex(?:pair)?\{([^}]+)\}(?:\{([^}]+)\})?", text):
        for path_str in filter(None, [m.group(1), m.group(2)]):
            fig_path = ROOT / path_str
            if fig_path.exists():
                fig_text = fig_path.read_text(encoding="utf-8")
                total += len(re.findall(r"\\bwimage\b", fig_text))
                total += len(re.findall(r"\\includegraphics\b", fig_text))
            else:
                total += 1  # fallback if file not found

    # single-image commands count as 1 each
    for cmd in [r"\iconographiewrapfig", r"\iconographieinlineblock", r"\iconographieimg"]:
        total += len(re.findall(re.escape(cmd) + r"\b", text))

    # bare \bwimage not inside an \iconographie* command
    for line in text.splitlines():
        if re.search(r"\\bwimage\b", line) and not re.search(r"\\iconographi\w+", line):
            total += len(re.findall(r"\\bwimage\b", line))

    return total


def _parse_toc_pages(toc_path: Path) -> list[int]:
    """Return start pages for each \\chapternumberline entry (scenes), in document order."""
    if not toc_path.exists():
        return []
    pattern = re.compile(
        r'\\contentsline\s*\{chapter\}\{\\chapternumberline\s*\{\d+\}[^}]*\}\{(\d+)\}'
    )
    return [int(m.group(1)) for m in pattern.finditer(toc_path.read_text(encoding="utf-8"))]


def _parse_toc_scene_pages(toc_path: Path) -> list[int]:
    """Return start pages for each Scène~ section entry (scenes) in document order.
    Scenes are recorded as {section} entries only in the LA_TOTALE build (no SANSSCENES)."""
    if not toc_path.exists():
        return []
    pattern = re.compile(
        r'\\contentsline\s*\{section\}\{Scène~[^}]*\}\{(\d+)\}'
    )
    return [int(m.group(1)) for m in pattern.finditer(toc_path.read_text(encoding="utf-8"))]


def _parse_toc_acte_pages(toc_path: Path) -> list[int]:
    """Return start pages for each Acte~ chapter entry (actes), in document order."""
    if not toc_path.exists():
        return []
    pattern = re.compile(
        r'\\contentsline\s*\{chapter\}\{Acte~[^}]*\}\{(\d+)\}'
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
    # Strip TeX comments: anything from an unescaped % to end of line
    return re.sub(r'(?<!\\)%.*', '', text)


def compute():
    """One row per acte (original chapter structure)."""
    rows = []
    for acte_num in ACTES:
        text  = _load_acte(acte_num)
        rows.append((acte_num, count_words(text), count_notes(text), count_illus(text), count_dialogue_words(text)))
    return rows


def compute_split():
    """One row per segment delimited by \\scene (split scene structure)."""
    rows = []
    scene_counter = 0  # global, never resets between acts
    for acte_num in ACTES:
        text = _load_acte(acte_num)
        # Split line-by-line: only trigger on \scene not preceded by % on same line
        segments = []
        current: list[str] = []
        for line in text.splitlines(keepends=True):
            if re.match(r"\s*\\scene\b", line):
                segments.append("".join(current))
                current = []
            else:
                current.append(line)
        segments.append("".join(current))
        acte_label = ROMAN[acte_num]
        for i, seg in enumerate(segments):
            scene_counter += 1
            chap_label = f"{acte_label}.{scene_counter}"
            rows.append((chap_label, acte_label,
                         count_words(seg), count_notes(seg), count_illus(seg),
                         count_dialogue_words(seg), first_words(seg)))
    return rows


def _md_table(rows: list, page_ranges: list | None = None) -> str:
    counted = rows
    total_words = sum(r[1] for r in counted)
    total_notes = sum(r[2] for r in counted)
    total_illus = sum(r[3] for r in counted)
    has_pages = bool(page_ranges)

    page_cols = " p. | pp. |" if has_pages else ""
    page_sep  = "---:|----:|" if has_pages else ""
    lines = [
        "# Statistiques par acte (avant découpage)\n",
        "Mots = texte original uniquement (hors contenu des notes `\\nf{}`).",
        "% notes et % illustrations = rapport au nombre de mots.\n",
        f"| Acte |{page_cols} Mots | %\u00a0livre | Notes | %\u00a0mots | Illustrations | %\u00a0mots |",
        f"|-----:|{page_sep}-----:|--------:|------:|-------:|--------------:|-------:|",
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
            f"| {illus_str:>13} | {illus_pct:>6} |"
        )
    total_dial = sum(r[4] for r in counted)
    lines.append(
        f"| **Total** |{'  |  |' if has_pages else ''} **{_fmt(total_words)}** | **100%** | **{total_notes}** "
        f"| **{_pct(total_notes, total_words)}** "
        f"| **{_fmt(total_illus)}** | **{_pct(total_illus, total_words)}** |"
    )
    return "\n".join(lines) + "\n"


def _md_table_split(rows: list, page_ranges: list | None = None) -> str:
    counted = rows
    total_words = sum(r[2] for r in counted)
    total_notes = sum(r[3] for r in counted)
    total_illus = sum(r[4] for r in counted)
    has_pages = bool(page_ranges)

    page_cols = " p. | pp. |" if has_pages else ""
    page_sep  = "---:|----:|" if has_pages else ""
    lines = [
        "# Statistiques par scène\n",
        "Mots = texte original uniquement (hors contenu des notes `\\nf{}`).",
        "% notes et % illustrations = rapport au nombre de mots.\n",
        f"| Acte.Scène | Début |{page_cols} Mots | %\u00a0livre | %\u00a0dial. | Notes | %\u00a0mots | Illustrations | %\u00a0mots |",
        f"|----------:|:------|{page_sep}-----:|--------:|--------:|------:|-------:|--------------:|-------:|",
    ]
    for i, (chap_label, acte_label, words, notes, illus, dial, debut) in enumerate(rows):
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
            f"| {chap_label} | {debut} |{page_part} {_fmt(words):>7} | {_pct(words, total_words):>7} | {_pct(dial, words):>7} "
            f"| {notes:>5} | {_pct(notes, words):>6} | {illus_str:>13} | {illus_pct:>6} |"
        )
    total_dial = sum(r[5] for r in counted)
    lines.append(
        f"| **Total** | |{'  |  |' if has_pages else ''} **{_fmt(total_words)}** | **100%** | **{_pct(total_dial, total_words)}** | **{total_notes}** "
        f"| **{_pct(total_notes, total_words)}** "
        f"| **{_fmt(total_illus)}** | **{_pct(total_illus, total_words)}** |"
    )
    return "\n".join(lines) + "\n"


def _png_illus_chart(rows_split: list) -> str:
    """Generate a Marimekko bar chart where bar width ∝ scene word count."""
    if not rows_split:
        return ""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return ""

    scene_labels = [r[0] for r in rows_split]
    acte_labels  = [r[1] for r in rows_split]
    values       = [round(r[4] / r[2] * 1000, 2) if r[2] else 0.0 for r in rows_split]
    words        = [r[2] for r in rows_split]

    total_words = sum(words)
    total_illus = sum(r[4] for r in rows_split)
    mean_val    = total_illus / total_words * 1000 if total_words else 0.0

    # Bar widths proportional to word count, scaled so total width = number of scenes
    scale      = len(rows_split)
    rel_widths = [w / total_words * scale for w in words]
    lefts      = [sum(rel_widths[:i]) for i in range(len(rel_widths))]
    centers    = [l + w / 2 for l, w in zip(lefts, rel_widths)]

    fig, ax = plt.subplots(figsize=(22, 8))
    gap    = 0.15          # fixed inter-bar gap in scale units
    offset = gap / 2       # half-gap margin before first bar and after last bar
    bar_widths = [max(w - gap, gap * 0.5) for w in rel_widths]
    # Shift all bars right by offset so first bar has gap/2 space from y-axis
    for l, v, bw, wc in zip(lefts, values, bar_widths, words):
        x_bar = l + offset
        ax.bar(x_bar, v, width=bw, align="edge", color="#89b8e8", alpha=0.85,
               zorder=2, edgecolor="white", linewidth=0.5)
        x_center = x_bar + bw / 2
        # ‰ value at top of bar (skip zeros)
        if v > 0:
            ax.text(x_center, v, f"{v:.1f}", ha="center", va="bottom",
                    fontsize=14, zorder=4)
        # word count in K, vertical, centred between y=0 and y=1
        ax.text(x_center, 0.5, f"{wc/1000:.1f}k", ha="center", va="center",
                fontsize=13, color="black", zorder=4)
    ax.axhline(mean_val, color="red", linewidth=3.0, zorder=3,
               label=f"moyenne {mean_val:.1f}‰")

    # Scene labels: drop roman prefix (acte shown below), horizontal, shifted
    short_labels = [lbl.split(".")[-1] for lbl in scene_labels]
    ax.set_xticks([c + offset for c in centers])
    ax.set_xticklabels(short_labels, rotation=0, ha="center", fontsize=20)

    # Acte separators (including left and right sentinels) + labels
    # Boundaries: 0, lefts[first-of-acte], …, scale+gap (right sentinel)
    trans = ax.get_xaxis_transform()
    y_line_top, y_line_bot, y_label = 1.0, -0.14, -0.15

    boundaries = [0.0]
    for i in range(1, len(acte_labels)):
        if acte_labels[i] != acte_labels[i - 1]:
            boundaries.append(lefts[i])   # = offset-shifted boundary midpoint
    boundaries.append(float(scale))        # right sentinel (gap/2 past last bar)

    actes_ordered = list(dict.fromkeys(acte_labels))  # unique, ordered

    for x_sep in boundaries:
        # Left sentinel overlaps y-axis: draw only the below-axes extension
        y_top = 0.0 if x_sep == 0.0 else y_line_top
        ax.plot([x_sep, x_sep], [y_top, y_line_bot], transform=trans,
                clip_on=False, color="#999", linewidth=1.0, linestyle="--", zorder=0)

    for k, acte in enumerate(actes_ordered):
        x_mid = (boundaries[k] + boundaries[k + 1]) / 2
        ax.annotate(acte, xy=(x_mid, y_label), xycoords=("data", "axes fraction"),
                    ha="center", va="top", fontsize=26, fontweight="bold",
                    annotation_clip=False)

    ax.set_xlim(0, scale + offset)
    ax.set_ylabel("‰ illus / mots", fontsize=28)
    ax.set_title("Illustrations par acte / scène (‰ des mots)", fontsize=32, pad=50)
    ax.annotate("largeur de chaque scène proportionnelle au nombre de mots",
                xy=(0.5, 1.0), xycoords="axes fraction",
                xytext=(0, 8), textcoords="offset points",
                ha="center", va="bottom", fontsize=18, fontstyle="italic",
                color="#555", annotation_clip=False)
    ax.tick_params(axis="y", labelsize=26)
    ax.legend(fontsize=26)

    ax.grid(axis="y", linewidth=0.5, color="#ddd", zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout(rect=[0, 0.08, 1, 1])

    import hashlib
    out = ROOT / "stats_illus_chart.jpg"
    fig.savefig(out, dpi=150, format="jpeg")
    plt.close(fig)
    digest = hashlib.md5(out.read_bytes()).hexdigest()[:8]
    return f"![Illustrations par scène](stats_illus_chart.jpg?v={digest})\n"


def _png_illus_chart_h(rows_split: list) -> str:
    """Generate a horizontal Marimekko bar chart where bar height ∝ scene word count."""
    if not rows_split:
        return ""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.transforms import blended_transform_factory
        from matplotlib.offsetbox import TextArea, HPacker, AnnotationBbox
    except ImportError:
        return ""

    scene_labels = [r[0] for r in rows_split]
    acte_labels  = [r[1] for r in rows_split]
    values       = [round(r[4] / r[2] * 1000, 2) if r[2] else 0.0 for r in rows_split]
    words        = [r[2] for r in rows_split]

    total_words = sum(words)
    total_illus = sum(r[4] for r in rows_split)
    mean_val    = total_illus / total_words * 1000 if total_words else 0.0

    scale       = len(rows_split)
    rel_heights = [w / total_words * scale for w in words]
    bottoms     = [sum(rel_heights[:i]) for i in range(len(rel_heights))]

    fig, ax = plt.subplots(figsize=(15, 18.2))
    gap    = 0.15
    offset = gap / 2
    bar_heights_actual = [max(h - gap, gap * 0.5) for h in rel_heights]

    trans_mixed = blended_transform_factory(ax.transAxes, ax.transData)

    # Column x positions (axes fraction, except # mots which is in data x)
    X_ACTE = -0.17   # acte Roman numeral — right-aligned
    X_SC   = -0.09   # scene number       — centre-aligned
    X_PROM = -0.02   # ‰ value            — right-aligned
    # # mots at data x = 0.5

    for b, v, bh, wc in zip(bottoms, values, bar_heights_actual, words):
        y_bot = b + offset
        y_ctr = y_bot + bh / 2
        ax.barh(y_bot, v, height=bh, align="edge", color="#89b8e8", alpha=0.85,
                zorder=2, edgecolor="white", linewidth=0.5)
        # ‰ value — own column, right of scene number, left of bar
        ax.annotate(f"{v:.1f}", xy=(X_PROM, y_ctr), xycoords=("axes fraction", "data"),
                    ha="right", va="center", fontsize=11, clip_on=False, zorder=4)
        # word count pinned at x=0.5 graduation
        ax.text(0.5, y_ctr, f"{wc/1000:.1f}k", ha="center", va="center",
                fontsize=10, color="black", zorder=4)

    ax.axvline(mean_val, color="red", linewidth=3.0, zorder=3)

    # Scene labels: manual annotations for precise x control; no default tick labels
    short_labels  = [lbl.split(".")[-1] for lbl in scene_labels]
    ytick_centers = [b + offset + bh / 2 for b, bh in zip(bottoms, bar_heights_actual)]
    ax.set_yticks(ytick_centers)
    ax.set_yticklabels([])
    ax.tick_params(axis="y", length=0)
    for sc_lbl, y_ctr in zip(short_labels, ytick_centers):
        ax.annotate(sc_lbl, xy=(X_SC, y_ctr), xycoords=("axes fraction", "data"),
                    ha="center", va="center", fontsize=16, clip_on=False, zorder=4)
    ax.set_ylim(0, scale + offset)
    ax.invert_yaxis()

    # Acte boundaries: horizontal separators + Roman numeral labels to the left
    x_left = -0.16

    boundaries = [0.0]
    for i in range(1, len(acte_labels)):
        if acte_labels[i] != acte_labels[i - 1]:
            boundaries.append(bottoms[i])
    boundaries.append(float(scale))

    actes_ordered = list(dict.fromkeys(acte_labels))

    for y_sep in boundaries:
        ax.plot([x_left, 1.0], [y_sep, y_sep], transform=trans_mixed,
                clip_on=False, color="#999", linewidth=1.0, linestyle="--", zorder=0)

    for k, acte in enumerate(actes_ordered):
        y_mid = (boundaries[k] + boundaries[k + 1]) / 2
        ax.annotate(acte, xy=(X_ACTE, y_mid), xycoords=("axes fraction", "data"),
                    ha="right", va="center", fontsize=22, fontweight="bold",
                    annotation_clip=False)

    # Column header row above the first separator
    hdr_y  = -0.25
    hdr_kw = dict(va="center", fontsize=13, fontweight="bold", color="#333",
                  clip_on=False, zorder=5)
    ax.annotate("acte",   xy=(X_ACTE, hdr_y), xycoords=("axes fraction", "data"),
                ha="right", annotation_clip=False, **hdr_kw)
    ax.annotate("sc.",    xy=(X_SC, hdr_y),   xycoords=("axes fraction", "data"),
                ha="center", annotation_clip=False, **hdr_kw)
    ax.annotate("‰",      xy=(X_PROM, hdr_y), xycoords=("axes fraction", "data"),
                ha="right", annotation_clip=False, **hdr_kw)
    ax.annotate("# mots", xy=(0.5, hdr_y),    xycoords=("data", "data"),
                ha="center", annotation_clip=False, **hdr_kw)
    _dash = TextArea("— ", textprops=dict(color="red",   fontsize=13, fontweight="bold"))
    _txt  = TextArea(f"moyenne {mean_val:.1f}‰",
                     textprops=dict(color="black", fontsize=13, fontweight="bold"))
    _box  = HPacker(children=[_dash, _txt], pad=0, sep=0)
    ax.add_artist(AnnotationBbox(
        _box, (mean_val, hdr_y), xycoords=("data", "data"),
        box_alignment=(0.5, 0.5), clip_on=False, zorder=5,
        bboxprops=dict(boxstyle="round,pad=0.4", facecolor="white",
                       edgecolor="#aaaaaa", linewidth=1.0, alpha=0.9)))

    ax.set_xlabel("‰ illustrations / mots", fontsize=22)
    ax.tick_params(axis="x", labelsize=18)

    ax.grid(axis="x", linewidth=0.5, color="#ddd", zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Titles centered on full figure width; subtitle offset to avoid overlap with main title
    fig.text(0.5, 0.988, "Illustrations par acte / scène (‰ des mots)",
             ha="center", va="top", fontsize=26)
    fig.text(0.5, 0.965, "hauteur de chaque scène proportionnelle au nombre de mots",
             ha="center", va="top", fontsize=14, fontstyle="italic", color="#555")

    plt.tight_layout(rect=[0.10, 0, 0.90, 0.950])

    import hashlib
    out = ROOT / "stats_illus_chart_h.jpg"
    fig.savefig(out, dpi=150, format="jpeg")
    plt.close(fig)
    digest = hashlib.md5(out.read_bytes()).hexdigest()[:8]
    return f"![Illustrations par scène (horizontal)](stats_illus_chart_h.jpg?v={digest})\n"


def _illus_forecast(rows_split) -> str:
    """Estimate remaining illustration work against a fixed target density."""
    counted = rows_split
    if not counted:
        return ""

    total_words = sum(r[2] for r in counted)
    total_illus = sum(r[4] for r in counted)
    estimated   = round(total_words / ILLUS_TARGET)
    remaining   = max(0, estimated - total_illus)
    pct_done    = total_illus / estimated * 100 if estimated else 0

    # Outlier scenes: actual vs expected illustrations at target density
    over, under = [], []
    for chap, _, words, _, illus, _, _ in counted:
        if words < ILLUS_TARGET / 2:   # too short to reliably flag
            continue
        expected = words / ILLUS_TARGET
        ratio    = illus / expected
        if ratio > 2.0:
            over.append(f"{chap} ({illus}/{expected:.1f})")
        elif ratio < 0.5:
            under.append(f"{chap} ({illus}/{expected:.1f})")

    lines = [
        f"\n## Estimation illustrations restantes\n",
        f"Cible : **1 illustration tous les {ILLUS_TARGET} mots** "
        f"({_fmt(total_words)} mots → **{estimated}** illustrations).  \n"
        f"Actuellement **{total_illus}** — il en manque **{remaining}** "
        f"— **{pct_done:.1f} %** réalisé.\n",
    ]
    if over:
        lines.append(f"Sur-illustrées (> 2× la cible) : {', '.join(over)}")
    if under:
        lines.append(f"Sous-illustrées (< 0.7× la cible) : {', '.join(under)}")
    return "\n".join(lines) + "\n"


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
        for chap_label, acte_label, words, notes, illus, dial, _debut in rows_split:
            print(f"     Scene {chap_label:<7} {_fmt(words):>8} mots  "
                  f"{notes:>4} notes ({_pct(notes, words)})  "
                  f"{illus:>3} illus ({_pct(illus, words)})  "
                  f"dial. {_pct(dial, words)}")


def main():
    global ILLUS_TARGET
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=ILLUS_TARGET,
                        help="1 illustration every N words (default: %(default)s)")
    ILLUS_TARGET = parser.parse_args().target

    rows_orig  = compute()
    rows_split = compute_split()

    total_pages        = _pdf_total_pages(LOG_MAIN)
    total_pages_totale = _pdf_total_pages(LOG_TOTALE)
    pages_actes  = _parse_toc_acte_pages(TOC_MAIN)
    pages_scenes = _parse_toc_scene_pages(TOC_TOTALE)  # section entries, LA_TOTALE build only
    pr_orig  = _page_ranges(pages_actes,  total_pages)        if pages_actes  else None
    pr_split = _page_ranges(pages_scenes, total_pages_totale) if pages_scenes else None

    # Sanity check: warn if TOC entry count doesn't match row count
    if pr_orig  and len(pr_orig)  != len(rows_orig):
        print(f"  ! pages_actes mismatch: {len(pr_orig)} toc entries vs {len(rows_orig)} rows")
        pr_orig = None
    if pr_split and len(pr_split) != len(rows_split):
        print(f"  ! pages_scenes mismatch: {len(pr_split)} toc entries vs {len(rows_split)} rows")
        pr_split = None

    md = (_md_table_split(rows_split, pr_split) + "\n"
          + _png_illus_chart_h(rows_split) + "\n"
          + _md_table(rows_orig, pr_orig)
          + _illus_forecast(rows_split))
    OUT_FILE.write_text(md, encoding="utf-8")
    print(f"  → {OUT_FILE.relative_to(ROOT)}")
    _print_rows(rows_orig, rows_split)
    forecast = _illus_forecast(rows_split)
    if forecast:
        print(forecast)


if __name__ == "__main__":
    main()
