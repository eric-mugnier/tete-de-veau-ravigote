"""
tasks.py  —  invoke build tasks for *Tête de veau ravigote*

Usage : inv build | inv notes | inv diffs | inv epub | inv pers | inv clean
        inv diffs notes   → combine targets (main PDF built once, both extras run)
"""

import os
from pathlib import Path
import shutil

from invoke import task

# Always run from the project root (mirrors `cd "$(dirname "$0")"` in the shell script)
ROOT = Path(__file__).parent
os.chdir(ROOT)

BUILD = ROOT / "build"
BASE  = "tete_de_veau_ravigote"


# ─── private helpers ──────────────────────────────────────────────────────────

def _svg_to_pdf(c):
    """Convert images/*.svg → images/*.svg.pdf, skip if SVG is not newer than PDF."""
    for svg in sorted(ROOT.glob("images/*.svg")):
        pdf = svg.parent / (svg.name + ".pdf")
        if not pdf.exists() or svg.stat().st_mtime > pdf.stat().st_mtime:
            c.run(f'rsvg-convert -f pdf -o "{pdf}" "{svg}"')


def _trim_pdf(path: Path) -> None:
    """Remove any bytes after the last %%EOF marker (lualatex may not truncate on overwrite)."""
    data = path.read_bytes()
    eof = data.rfind(b'%%EOF')
    if eof != -1 and eof + 5 < len(data):
        path.write_bytes(data[:eof + 5])


def _lmk(c, *stems):
    """Run latexmk -g -lualatex on one or more .tex stems (output → build/ via .latexmkrc)."""
    for stem in stems:
        c.run(f"latexmk -g -lualatex -interaction=nonstopmode {stem}.tex")


def _ls_outputs():
    """Print sizes of expected output files, silently skip missing ones."""
    candidates = [
        BUILD / f"{BASE}.pdf",
        BUILD / f"{BASE}_sommaire.pdf",
        BUILD / f"{BASE}_annote.pdf",
        BUILD / f"{BASE}_notes.pdf",
        BUILD / f"{BASE}_illustrations.pdf",
        BUILD / f"{BASE}_LA_TOTALE.pdf",
        BUILD / f"{BASE}_sommaire_etendu.pdf",
        BUILD / f"{BASE}_diff.pdf",
        ROOT  / f"{BASE}.epub",
        ROOT  / f"{BASE}_COMPLET.pdf",
    ]
    for p in candidates:
        if p.exists():
            print(f"  {p.stat().st_size / 1024:>8.0f} KB  {p.relative_to(ROOT)}")


# ─── tasks ────────────────────────────────────────────────────────────────────

@task
def gitinfo(c):
    """Write build/tete_de_veau_ravigote.gitinfo (shared by all documents)."""
    BUILD.mkdir(exist_ok=True)
    result = c.run("git log -1 --format=%h", hide=True)
    (BUILD / f"{BASE}.gitinfo").write_text(result.stdout.strip())


@task(pre=[gitinfo])
def build(c):
    """Build main PDF and sommaire (always run first; pre-task for diffs/epub/notes)."""

    print("=== svg → pdf ===")
    _svg_to_pdf(c)

    print("=== 1/4  main PDF ===")
    _lmk(c, BASE)

    print("=== 2/4  sommaire PDF ===")
    _lmk(c, f"{BASE}_sommaire")

    _ls_outputs()


@task(pre=[gitinfo])
def sommaire(c):
    """Build sommaire + sommaire étendu PDFs (no main PDF)."""
    print("=== svg → pdf ===")
    _svg_to_pdf(c)

    print("=== 1/4  main .toc (draftmode) ===")
    c.run(
        f"lualatex -interaction=nonstopmode -draftmode"
        f" -output-directory=build"
        f" {BASE}.tex"
    )

    print("=== 2/4  sommaire PDF ===")
    _lmk(c, f"{BASE}_sommaire")

    print("=== 3/4  etendu .toc (draftmode) ===")
    c.run(
        f"lualatex -interaction=nonstopmode -draftmode"
        f" -output-directory=build"
        f" -jobname={BASE}_etendu"
        f" {BASE}_etendu.tex"
    )

    print("=== 4/4  sommaire étendu PDF ===")
    _lmk(c, f"{BASE}_sommaire_etendu")
    _ls_outputs()


@task(pre=[build])
def diffs(c):
    """Build diff PDF against the original (requires latexdiff + make_diff.py)."""
    print("=== 3/4  diff PDF ===")
    c.run("python3 diff_work/make_diff.py")
    # Copy diff PDF from diff_work/ to build/ alongside the other PDFs
    shutil.copy(
        ROOT / "diff_work" / f"{BASE}_diff.pdf",
        BUILD / f"{BASE}_diff.pdf",
    )


@task(pre=[build])
def epub(c):
    """Build EPUB via pandoc."""
    print("=== epub ===")
    c.run(
        f"pandoc {BASE}.tex"
        f" -o {BASE}.epub"
        f' --metadata title="Tête de veau ravigote"'
        f' --metadata author="Éric Mugnier"'
        f' --metadata lang="fr"'
    )


@task(pre=[build])
def notes(c):
    """
    Build annotated PDF (inline note numbers) + standalone notes PDF.

    Sequence:
      1+2. Two direct lualatex passes with \\AVECNOTES + \\SANSNOTESFINALES
           → populates tete_de_veau_ravigote.ent (endnotes register)
      3.   Copy the annotated PDF to build/
      4.   Compile notes-only PDF  ← BEFORE restoring the roman (.ent still populated)
      5.   Compile illustrations PDF
      6.   Restore clean main PDF (no inline note numbers)
    """
    print("=== NOTES : génération du .ent ===")

    # Double-braces {{ }} in the f-string produce literal { } for LaTeX
    tex_cmd = rf"\def\AVECNOTES{{}}\def\SANSNOTESFINALES{{}}\input{{{BASE}}}"
    lualatex = (
        f"lualatex -interaction=nonstopmode"
        f" -output-directory=build"
        f" -jobname={BASE}"
        f' "{tex_cmd}"'
    )

    # Pass 1: first compilation (builds .ent, resolves refs for the first time)
    (BUILD / f"{BASE}.pdf").unlink(missing_ok=True)
    c.run(lualatex)
    # Pass 2: second compilation (cross-references stabilise, .ent fully populated)
    (BUILD / f"{BASE}.pdf").unlink(missing_ok=True)
    c.run(lualatex)

    # 1. Roman annoté : inline note numbers, no endnotes appended at the end
    # Both the PDF and the .ent now live in build/, so latexmk finds .ent naturally
    # Trim any bytes past %%EOF (lualatex doesn't always truncate on overwrite)
    _trim_pdf(BUILD / f"{BASE}.pdf")
    shutil.copy(BUILD / f"{BASE}.pdf", BUILD / f"{BASE}_annote.pdf")
    print(f"→ build/{BASE}_annote.pdf")

    # 2. Notes seules — compile BEFORE restoring the roman (.ent still populated)
    _lmk(c, f"{BASE}_notes")
    print(f"→ build/{BASE}_notes.pdf")

    # 3. Illustrations
    _lmk(c, f"{BASE}_illustrations")
    print(f"→ build/{BASE}_illustrations.pdf")

    # Restore the clean main PDF (without inline note numbers)
    _lmk(c, BASE)


@task
def pers(c):
    """Build personnages.pdf from personnages.md via pandoc + lualatex."""
    BUILD.mkdir(exist_ok=True)
    c.run(
        "pandoc personnages.md"
        f" -o {BUILD}/personnages.pdf"
        " --pdf-engine=lualatex"
        " -V geometry:margin=2cm"
        " -V lang=fr"
        ' -V mainfont="EB Garamond"'
        " -V fontsize=11pt"
    )
    print(f"  → {BUILD}/personnages.pdf")


@task
def postface(c):
    """Build postface.pdf from postface_claude.md via pandoc + lualatex."""
    BUILD.mkdir(exist_ok=True)
    c.run(
        "pandoc postface_claude.md"
        f" -o {BUILD}/postface.pdf"
        " --pdf-engine=lualatex"
        " -V geometry:left=35mm"
        " -V geometry:right=35mm"
        " -V geometry:top=4cm"
        " -V geometry:bottom=4cm"
        " -V lang=fr"
        ' -V mainfont="EB Garamond"'
        ' -V mainfontoptions="Numbers=OldStyle,SmallCapsFeatures={Letters=SmallCaps}"'
        " -V fontsize=11pt"
    )
    print(f"  → {BUILD}/postface.pdf")


@task(pre=[gitinfo])
def total(c):
    """Build LA TOTALE : document unifié annoté + postface + notes + sommaire étendu + personnages."""
    print("=== svg → pdf ===")
    _svg_to_pdf(c)

    import re as _re

    def _pandoc_body(src, dest):
        c.run(f"pandoc {src} -t latex -o {BUILD}/{dest}")
        _body = (BUILD / dest).read_text()
        _body = _re.sub(r"\\section\{.*?\}\\label\{[^}]*\}", "", _body, flags=_re.DOTALL)
        (BUILD / dest).write_text(_body)

    print("=== pandoc : postface ChatGPT body ===")
    _pandoc_body("postface-chatGPT.md", "postface_chatgpt_body.tex")

    print("=== pandoc : postface Claude body ===")
    _pandoc_body("postface_claude.md", "postface_claude_body.tex")

    print("=== pandoc : personnages body ===")
    c.run(f"pandoc personnages.md -t latex -o {BUILD}/personnages_body.tex")
    # Post-process:
    # 1. Remove pandoc's \section{} heading (we add our own title in LA_TOTALE.tex)
    # 2. Fix longtable column widths (pandoc uses A4-based proportions)
    import re
    body = (BUILD / "personnages_body.tex").read_text()
    body = re.sub(r"\\section\{.*?\}\\label\{[^}]*\}", "", body, flags=re.DOTALL)
    body = re.sub(
        r"\\begin\{longtable\}\[.*?\]\{@\{\}.*?@\{\}\}",
        (r"\\begin{longtable}[]{@{}"
         r">{\\raggedright\\arraybackslash}p{8mm}"
         r">{\\raggedright\\arraybackslash}p{30mm}"
         r">{\\raggedright\\arraybackslash}"
         r"p{\\dimexpr\\linewidth-8mm-30mm-4\\tabcolsep\\relax}@{}}"),
        body, flags=re.DOTALL,
    )
    (BUILD / "personnages_body.tex").write_text(body)

    print("=== LA TOTALE ===")
    _lmk(c, f"{BASE}_LA_TOTALE")
    _ls_outputs()


@task
def all(c):
    """Build everything: main, sommaires, notes, epub, pers, postface, diffs, then clean."""
    build(c)
    # sommaire étendu (le .toc principal existe déjà après build)
    c.run(
        f"lualatex -interaction=nonstopmode -draftmode"
        f" -output-directory=build"
        f" -jobname={BASE}_etendu"
        f" {BASE}_etendu.tex"
    )
    _lmk(c, f"{BASE}_sommaire_etendu")
    # notes (bypasse le pre=[build] déjà fait)
    notes(c)
    # epub
    c.run(
        f"pandoc {BASE}.tex"
        f" -o {BASE}.epub"
        f' --metadata title="Tête de veau ravigote"'
        f' --metadata author="Éric Mugnier"'
        f' --metadata lang="fr"'
    )
    # pers + postface
    pers(c)
    postface(c)
    # diffs
    c.run("python3 diff_work/make_diff.py")
    shutil.copy(ROOT / "diff_work" / f"{BASE}_diff.pdf", BUILD / f"{BASE}_diff.pdf")
    _ls_outputs()
    clean(c)


@task
def clean(c):
    """Remove aux files from build/ and root; keep PDFs and IDE body files."""
    # Root-level stray PDF — would only appear if lualatex was called without -output-directory
    (ROOT / f"{BASE}.pdf").unlink(missing_ok=True)

    # latexmk aux files in root (produced by the two direct lualatex passes in notes)
    c.run(f"latexmk -c -outdir=. {BASE}.tex", warn=True)

    # build/ : keep only PDFs and the three body.tex files needed for IDE compilation
    _keep_names = {"personnages_body.tex", "postface_chatgpt_body.tex", "postface_claude_body.tex"}
    if BUILD.exists():
        for f in BUILD.iterdir():
            if f.is_file() and f.suffix != ".pdf" and f.name not in _keep_names:
                f.unlink()
