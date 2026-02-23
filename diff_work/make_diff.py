#!/usr/bin/env python3
"""
make_diff.py — Build a latexdiff PDF comparing the original manuscript
to the revised actes.

Directories:
  BASE      = /Users/christophe.thiebaud/_Mugnier
  WORK      = BASE/diff_work          ← this script lives here
  TMPDIR    = WORK/tmp                ← intermediate .tex fragments
  Output    = WORK/tete_de_veau_ravigote_diff.tex  (and .pdf)
"""

import os, subprocess, sys, re, glob

BASE   = '/Users/christophe.thiebaud/_Mugnier'
ACTES  = os.path.join(BASE, 'actes')
WORK   = os.path.join(BASE, 'diff_work')
TMPDIR = os.path.join(WORK, 'tmp')
os.makedirs(TMPDIR, exist_ok=True)

# ── Step 0: clean all intermediate files ────────────────────────────────────
print('Cleaning intermediate files...')
for f in glob.glob(os.path.join(TMPDIR, '*.tex')):
    os.remove(f)
for ext in ('aux', 'toc', 'log', 'out', 'fls', 'fdb_latexmk'):
    for f in glob.glob(os.path.join(WORK, f'*.{ext}')):
        os.remove(f)
diff_tex = os.path.join(WORK, 'tete_de_veau_ravigote_diff.tex')
if os.path.exists(diff_tex):
    os.remove(diff_tex)
print('  Done.\n')

# ── Step 1: parse original ──────────────────────────────────────────────────
with open(os.path.join(BASE, 'tete_de_veau_ravigote_original.tex'), encoding='utf-8') as f:
    orig_lines = f.readlines()

# ALL chapter header lines (1-based) — used for boundary detection only.
# Always keep the full list so each chapter is correctly bounded.
ALL_HEADERS = [72, 86, 130, 158, 189, 205, 227, 235, 251]

def get_chapter_content(header_line_1based):
    """Return lines of content for the chapter starting at header_line_1based."""
    start = header_line_1based + 1          # 1-based, skip blank after header
    idx   = ALL_HEADERS.index(header_line_1based)
    if idx + 1 < len(ALL_HEADERS):
        end = ALL_HEADERS[idx + 1] - 1      # up to next header (exclusive)
    else:
        end = len(orig_lines)               # last chapter: to EOF
    return orig_lines[start:end]

chapters = {}
for h in ALL_HEADERS:
    n = ALL_HEADERS.index(h) + 1
    chapters[n] = ''.join(get_chapter_content(h))

# ── Step 2: define chapter groups ──────────────────────────────────────────
# Set to a subset for testing; expand to all 9 when ready.
groups = [
    (1, [('acte_01_headline', 'acte_01')]),
    (2, [('acte_02_headline', 'acte_02')]),
    (3, [('acte_03_headline', 'acte_03')]),
    (4, [('acte_04_headline', 'acte_04')]),
    (5, [('acte_05_headline', 'acte_05')]),
    (6, [('acte_06_1_headline', 'acte_06_1'), ('acte_06_2_headline', 'acte_06_2')]),
    (7, [('acte_07_headline', 'acte_07')]),
    (8, [('acte_08_headline', 'acte_08')]),
    (9, [('acte_09_1_headline', 'acte_09_1'), ('acte_09_2_headline', 'acte_09_2'),
         ('acte_09_2b_headline', 'acte_09_2b'), ('acte_09_3_headline', 'acte_09_3'),
         ('acte_09_3b_headline', 'acte_09_3b'), ('acte_09_4_headline', 'acte_09_4')]),
]

def strip_document_tags(text):
    """Remove \\begin{document} / \\end{document} from a fragment."""
    text = re.sub(r'\\end\{document\}',   '', text)
    text = re.sub(r'\\begin\{document\}', '', text)
    return text

# Characters normalised in BOTH orig and new before diffing, so purely
# typographic variants don't generate noise in the diff output.
# Add or remove entries here as needed.
NORMALIZE_MAP = {
    '\u2019': "'",   # RIGHT SINGLE QUOTATION MARK → ASCII apostrophe
    '\u2018': "'",   # LEFT SINGLE QUOTATION MARK  → ASCII apostrophe
    '\u2013': '--',  # EN DASH                     → LaTeX --
    '\u2014': '---', # EM DASH                     → LaTeX ---
    '~---~': ' - ',  # ~---~ (LaTeX em-dash)       → ' - '
    '~--~':  ' - ',  # ~--~ (LaTeX en-dash)        → ' - '
    '~-- ':  ' - ',  # ~-- (LaTeX en-dash + space) → ' - '
    ' -- ':  ' - ',  # spaced en-dash              → ' - '
    ' --- ': ' - ',  # spaced em-dash              → ' - '
    '\u2026': '...',  # HORIZONTAL ELLIPSIS          → ...
    '\\ldots{}': '...',  # LaTeX ellipsis command   → ...
    '\\ldots ': '... ',  # \ldots followed by space → ...
    '\\ldots': '...',    # bare \ldots              → ...
    # ── Guillemets ──────────────────────────────────────────────────────────
    # Longer patterns first so they match before the bare « / » entries.
    '«~':      '"',  # « + LaTeX tilde (non-breaking space) → "
    '~»':      '"',  # LaTeX tilde + » → "
    '«\u00a0': '"',  # « + espace insécable → "
    '\u00a0»': '"',  # espace insécable + » → "
    '« ':      '"',  # « + espace ordinaire → "
    ' »':      '"',  # espace ordinaire + » → "
    '«':       '"',  # « seul → "
    '»':       '"',  # » seul → "
    '"':       '"',  # LEFT DOUBLE QUOTATION MARK  → "
    '"':       '"',  # RIGHT DOUBLE QUOTATION MARK → "
}

def normalize(text):
    """Normalise typographic variants so they don't appear as diff noise."""
    for src, dst in NORMALIZE_MAP.items():
        text = text.replace(src, dst)
    # LaTeX-style double quotes: ``text'' → "text"
    text = text.replace('``', '"')
    text = text.replace("''", '"')
    # Strip \textsc{...} → keep only the content (formatting change, not text change)
    text = re.sub(r'\\textsc\{([^}]*)\}', r'\1', text)
    return text

# ── Step 3: write orig and new fragments, run latexdiff ────────────────────
diff_bodies = {}

for chap_num, file_pairs in groups:
    orig_text = normalize(strip_document_tags(chapters[chap_num]).rstrip('\n') + '\n')

    new_parts = []
    for headline_name, content_name in file_pairs:
        hl_path = os.path.join(ACTES, headline_name + '.tex')
        ct_path = os.path.join(ACTES, content_name  + '.tex')
        with open(hl_path, encoding='utf-8') as f:
            new_parts.append(strip_document_tags(f.read()))
        with open(ct_path, encoding='utf-8') as f:
            new_parts.append(strip_document_tags(f.read()))
    new_text = normalize('\n'.join(new_parts))

    orig_path = os.path.join(TMPDIR, f'orig_{chap_num:02d}.tex')
    new_path  = os.path.join(TMPDIR, f'new_{chap_num:02d}.tex')
    diff_path = os.path.join(TMPDIR, f'diff_{chap_num:02d}.tex')

    with open(orig_path, 'w', encoding='utf-8') as f:
        f.write(orig_text)
    with open(new_path, 'w', encoding='utf-8') as f:
        f.write(new_text)

    print(f'Running latexdiff for Acte {chap_num}...')
    env = os.environ.copy()
    env['PERL_REGEXP_RECURSION_LIMIT'] = '200000'
    result = subprocess.run(
        ['latexdiff', '--encoding=utf8', '--flatten', orig_path, new_path],
        capture_output=True, env=env
    )
    if result.returncode != 0:
        print(f'  WARNING: latexdiff returned {result.returncode}')
        print(f'  stderr: {result.stderr.decode("utf-8", errors="replace")[:500]}')

    diff_text = result.stdout.decode('utf-8', errors='replace')
    with open(diff_path, 'w', encoding='utf-8') as f:
        f.write(diff_text)

    diff_bodies[chap_num] = diff_path
    print(f'  Done. Diff size: {len(diff_text)} chars')

# ── Step 4: extract preamble from main .tex ────────────────────────────────
with open(os.path.join(BASE, 'tete_de_veau_ravigote.tex'), encoding='utf-8') as f:
    main_tex = f.read()

preamble_end = main_tex.index(r'\begin{document}')
preamble     = main_tex[:preamble_end]

# Neutralise the gitinfo lines (require \jobname.gitinfo to exist)
preamble = re.sub(
    r'\\immediate\\write18\{git log.*?\}',
    r'% git log line removed for diff build',
    preamble
)
preamble = re.sub(
    r'\\CatchFileDef\{\\gitcommit\}\{\\jobname\.gitinfo\}\{[^}]*\}',
    r'\\newcommand{\\gitcommit}{unknown}',
    preamble
)

# Add latexdiff support macros
latexdiff_pkgs = r"""
% ─── LATEXDIFF MARKUP ────────────────────────────────────────────────────────
\usepackage{ulem}
\usepackage{color}
\providecommand{\DIFadd}[1]{{\color{blue}#1}}
\providecommand{\DIFdel}[1]{{\color{red}\sout{#1}}}
\providecommand{\DIFaddbegin}{}
\providecommand{\DIFaddend}{}
\providecommand{\DIFdelbegin}{}
\providecommand{\DIFdelend}{}
\providecommand{\DIFaddFL}[1]{\DIFadd{#1}}
\providecommand{\DIFdelFL}[1]{\DIFdel{#1}}
\providecommand{\DIFaddbeginFL}{}
\providecommand{\DIFaddendFL}{}
\providecommand{\DIFdelbeginFL}{}
\providecommand{\DIFdelendFL}{}
"""

# ── Step 5: extract front/back matter around \input{…_content.tex} ─────────
body_start   = main_tex.index(r'\begin{document}')
input_line   = r'\input{tete_de_veau_ravigote_content.tex}'
content_start = main_tex.index(input_line)
content_end   = content_start + len(input_line)

front_matter = main_tex[body_start + len(r'\begin{document}'):content_start]
back_matter  = main_tex[content_end:]

# ── Step 6: build chapter blocks from diff fragments ───────────────────────
chapter_names = ['I','II','III','IV','V','VI','VII','VIII','IX']
chapter_blocks = []

for chap_num, _ in groups:
    diff_path = diff_bodies[chap_num]
    with open(diff_path, encoding='utf-8') as f:
        diff_content = f.read()

    if r'\begin{document}' in diff_content:
        body_s    = diff_content.index(r'\begin{document}') + len(r'\begin{document}')
        body_e    = diff_content.rindex(r'\end{document}')
        diff_body = diff_content[body_s:body_e].strip()
    else:
        diff_body = diff_content.strip()

    roman = chapter_names[chap_num - 1]
    chapter_blocks.append(f'\\chapter{{Acte {roman}}}\n{diff_body}\n')

full_content = '\n'.join(chapter_blocks)

# ── Step 7: assemble full diff document ────────────────────────────────────
diff_doc = (
    preamble
    + latexdiff_pkgs
    + '\\begin{document}\n'
    + front_matter
    + full_content
    + back_matter
)

diff_tex_path = os.path.join(WORK, 'tete_de_veau_ravigote_diff.tex')
with open(diff_tex_path, 'w', encoding='utf-8') as f:
    f.write(diff_doc)

print(f'\nWrote {diff_tex_path}  ({os.path.getsize(diff_tex_path)} bytes)')

# ── Step 8: compile (two passes for TOC) ───────────────────────────────────
# TEXINPUTS: search BASE first (for version.tex, images/, etc.), then defaults
compile_env = os.environ.copy()
compile_env['TEXINPUTS'] = BASE + '::'

for pass_num in (1, 2):
    print(f'\nCompiling PDF (pass {pass_num})...')
    r = subprocess.run(
        ['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
         diff_tex_path],          # absolute path avoids TEXINPUTS confusion
        cwd=WORK, capture_output=True, env=compile_env
    )
    stdout = r.stdout.decode('latin-1', errors='replace')
    tail   = stdout[-3000:] if len(stdout) > 3000 else stdout
    print(tail)
    if r.returncode != 0:
        stderr = r.stderr.decode('latin-1', errors='replace')
        print('STDERR:', stderr[-1000:])
        print(f'Pass {pass_num} failed — check diff_work/tete_de_veau_ravigote_diff.log')
        sys.exit(1)

print(f'\nSUCCESS: {os.path.join(WORK, "tete_de_veau_ravigote_diff.pdf")} generated.')

# ── Step 9: update word_count.md ────────────────────────────────────────────

def update_word_count_md():
    """Re-compute Diffs / Diffs% columns from the freshly generated diff files."""

    def count_difdel_lines(diff_path):
        with open(diff_path, encoding='utf-8') as f:
            return sum(1 for ln in f if r'\DIFdel{' in ln)

    def parse_words(cell):
        return int(re.sub(r'[\s\u00a0\u202f]', '', cell.strip()))

    def fmt_pct(value):
        return f'{value:.2f}'.replace('.', ',') + ' %'

    wc_path = os.path.join(ACTES, 'word_count.md')
    with open(wc_path, encoding='utf-8') as f:
        raw_lines = f.readlines()

    # Collect word counts from the existing table
    file_words = {}
    for line in raw_lines:
        cells = line.split('|')
        if len(cells) < 5:
            continue
        fname = cells[2].strip()
        if not fname.startswith('acte_'):
            continue
        try:
            file_words[fname] = parse_words(cells[3])
        except ValueError:
            pass

    # Count DIFdel lines and build group metadata
    first_file_info = {}   # 'acte_XX.tex' → (diffs, group_words, starred)
    non_first_files = set()
    for chap_num, file_pairs in groups:
        diff_path = os.path.join(TMPDIR, f'diff_{chap_num:02d}.tex')
        diffs = count_difdel_lines(diff_path)
        group_words = sum(file_words.get(ct + '.tex', 0) for _, ct in file_pairs)
        first_ct = file_pairs[0][1] + '.tex'
        starred = len(file_pairs) > 1
        first_file_info[first_ct] = (diffs, group_words, starred)
        for i, (_, ct) in enumerate(file_pairs):
            if i > 0:
                non_first_files.add(ct + '.tex')

    total_diffs = sum(d for d, _, _ in first_file_info.values())
    total_words = sum(file_words.values())

    # Rewrite the table
    new_lines = []
    for line in raw_lines:
        cells = line.split('|')

        if len(cells) >= 9 and '**Total**' in cells[1]:
            pct = fmt_pct(total_diffs / total_words * 100)
            cells[6] = f' **{total_diffs}** '
            cells[7] = f' **{pct}** '
            new_lines.append('|'.join(cells))
            continue

        fname = cells[2].strip() if len(cells) >= 3 else ''

        if fname in non_first_files:
            cells[6] = '  '
            cells[7] = '  '
            new_lines.append('|'.join(cells))
            continue

        if fname in first_file_info:
            diffs, group_words, starred = first_file_info[fname]
            star = ' *' if starred else ''
            pct = fmt_pct(diffs / group_words * 100) if group_words else '0,00 %'
            cells[6] = f' {diffs}{star} '
            cells[7] = f' {pct}{star} '
            new_lines.append('|'.join(cells))
            continue

        new_lines.append(line)

    with open(wc_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f'\nUpdated {wc_path}')
    print(f'  Total Diffs : {total_diffs}  ({fmt_pct(total_diffs / total_words * 100)} sur {total_words} mots)')

update_word_count_md()
