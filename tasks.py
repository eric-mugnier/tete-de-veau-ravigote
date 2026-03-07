"""
tasks.py  —  invoke build tasks for *Tête de veau ravigote*

Usage : inv build | inv notes | inv diffs | inv epub | inv clean
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
        BUILD / f"{BASE}_diff.pdf",
        ROOT  / f"{BASE}.epub",
        ROOT  / f"{BASE}_COMPLET.pdf",
    ]
    for p in candidates:
        if p.exists():
            print(f"  {p.stat().st_size / 1024:>8.0f} KB  {p.relative_to(ROOT)}")


# ─── tasks ────────────────────────────────────────────────────────────────────

@task
def build(c):
    """Build main PDF and sommaire (always run first; pre-task for diffs/epub/notes)."""
    print("=== git hash ===")
    result = c.run("git log -1 --format=%h", hide=True)
    (ROOT / f"{BASE}.gitinfo").write_text(result.stdout.strip())

    print("=== svg → pdf ===")
    _svg_to_pdf(c)

    print("=== 1/4  main PDF ===")
    _lmk(c, BASE)

    print("=== 2/4  sommaire PDF ===")
    _lmk(c, f"{BASE}_sommaire")

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
        f" -jobname={BASE}"
        f' "{tex_cmd}"'
    )

    # Pass 1: first compilation (builds .ent, resolves refs for the first time)
    c.run(lualatex)
    # Pass 2: second compilation (cross-references stabilise, .ent fully populated)
    c.run(lualatex)

    # 1. Roman annoté : inline note numbers, no endnotes appended at the end
    shutil.copy(ROOT / f"{BASE}.pdf", BUILD / f"{BASE}_annote.pdf")
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
def clean(c):
    """Remove root-level temp files and latexmk aux files from build/."""
    # Root-level files not managed by latexmk:
    #   .gitinfo  — written at build start, not needed after
    #   .pdf      — annotated build artefact; canonical PDF lives in build/
    #   .ent      — endnotes register, regenerated on every notes build
    for name in [f"{BASE}.gitinfo", f"{BASE}.pdf", f"{BASE}.ent"]:
        (ROOT / name).unlink(missing_ok=True)
    # build/.ent — written by latexmk restore pass; not a standard aux file
    #              so latexmk -c doesn't remove it
    (BUILD / f"{BASE}.ent").unlink(missing_ok=True)

    # latexmk aux files in root (produced by the two direct lualatex passes in notes)
    c.run(f"latexmk -c -outdir=. {BASE}.tex", warn=True)

    # latexmk aux files in build/ (produced by all latexmk-managed compilations)
    for stem in [BASE, f"{BASE}_sommaire", f"{BASE}_notes", f"{BASE}_illustrations"]:
        c.run(f"latexmk -c -outdir=build {stem}.tex", warn=True)
