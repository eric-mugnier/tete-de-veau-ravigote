"""
tasks.py  —  invoke build tasks for *Tête de veau ravigote*

Usage : inv build | inv notes | inv diffs | inv epub | inv pers | inv clean
        inv diffs notes   → combine targets (main PDF built once, both extras run)
"""

import os
import re
import time
from functools import wraps
from pathlib import Path
import shutil

from invoke import task


def _timed(fn):
    """Decorator: print elapsed time after a task body completes."""
    @wraps(fn)
    def wrapper(c, *args, **kwargs):
        t0 = time.perf_counter()
        result = fn(c, *args, **kwargs)
        elapsed = time.perf_counter() - t0
        mins, secs = divmod(int(elapsed), 60)
        print(f"  → {fn.__name__} : {f'{mins}m ' if mins else ''}{secs}s")
        return result
    return wrapper

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


def _pandoc_body(c, src, dest):
    """Run pandoc src → build/dest (latex), then strip any \\section{}\\label{} header."""
    c.run(f"pandoc {src} -t latex -o {BUILD}/{dest}")
    body = (BUILD / dest).read_text()
    body = re.sub(r"\\section\{.*?\}\\label\{[^}]*\}", "", body, flags=re.DOTALL)
    (BUILD / dest).write_text(body)


def _lmk(c, *stems):
    """Run latexmk -g -lualatex on one or more .tex stems (output → build/ via .latexmkrc)."""
    for stem in stems:
        # Touch .toc so latexmk doesn't treat its absence as a fatal missing-input error
        (BUILD / f"{stem}.toc").touch(exist_ok=True)
        c.run(f"latexmk -g -lualatex -interaction=nonstopmode {stem}.tex", warn=True)


_OUTPUT_PDFS = [
    f"{BASE}.pdf",
    f"{BASE}_sommaire.pdf",
    f"{BASE}_annote.pdf",
    f"{BASE}_notes.pdf",
    f"{BASE}_LA_TOTALE.pdf",
    f"{BASE}_diff.pdf",
    "postface_claude.pdf",
    "postface_chatgpt.pdf",
    "ratiocinations.pdf",
    "personnages.pdf",
]


def _ls_outputs():
    """Print sizes of expected output files, silently skip missing ones."""
    candidates = [BUILD / name for name in _OUTPUT_PDFS] + [
        BUILD / f"{BASE}.epub",
        ROOT / f"{BASE}_COMPLET.pdf",
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
@_timed
def build(c):
    """Build main PDF and sommaire (always run first; pre-task for diffs/epub/notes)."""

    print("=== svg → pdf ===")
    _svg_to_pdf(c)

    _lmk(c, BASE)
    _ls_outputs()


@task(pre=[build])
@_timed
def sommaire(c):
    """Build sommaire PDF (uses .toc from build)."""
    _lmk(c, f"{BASE}_sommaire")
    _ls_outputs()


@task(pre=[build])
@_timed
def diffs(c):
    """Build diff PDF against the original (requires latexdiff + make_diff.py)."""
    print("=== 3/4  diff PDF ===")
    c.run("python3 -u diff_work/make_diff.py")
    # Copy diff PDF from diff_work/ to build/ alongside the other PDFs
    shutil.copy(
        ROOT / "diff_work" / f"{BASE}_diff.pdf",
        BUILD / f"{BASE}_diff.pdf",
    )


@task(pre=[build])
@_timed
def epub(c):
    """Build EPUB via pandoc."""
    print("=== epub ===")
    c.run(
        f"pandoc {BASE}.tex"
        f" -o {BUILD}/{BASE}.epub"
        f' --metadata title="Tête de veau ravigote"'
        f' --metadata author="Éric Mugnier"'
        f' --metadata lang="fr"'
    )


@task(pre=[build])
@_timed
def notes(c):
    """
    Build annotated PDF (inline note numbers) + standalone notes PDF.

    Sequence:
      1+2. Two direct lualatex passes with \\AVECNOTES + \\SANSNOTESFINALES
           → populates tete_de_veau_ravigote.ent (endnotes register)
      3.   Copy the annotated PDF to build/
      4.   Compile notes-only PDF  ← BEFORE restoring the roman (.ent still populated)
      5.   Restore clean main PDF (no inline note numbers)
    """
    print("=== NOTES : génération du .ent ===")

    # Double-braces {{ }} in the f-string produce literal { } for LaTeX
    tex_cmd = rf"\def\AVECNOTES{{}}\def\SANSNOTESFINALES{{}}\input{{{BASE}}}"
    lualatex = (
        f"lualatex -shell-escape -interaction=nonstopmode"
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

    # Restore the clean main PDF (without inline note numbers)
    _lmk(c, BASE)


@task(name="couv")
@_timed
def couverture(c):
    """Build tete_de_veau_ravigote_couverture_24bookprint.pdf via lualatex."""
    BUILD.mkdir(exist_ok=True)
    c.run(
        f"lualatex -interaction=nonstopmode"
        f" -output-directory={BUILD}"
        f" tete_de_veau_ravigote_couverture_24bookprint.tex"
    )
    print(f"  → {BUILD}/tete_de_veau_ravigote_couverture_24bookprint.pdf")


@task
@_timed
def ratiocinations(c):
    """Build ratiocinations.pdf from actes/ratiocinations.md via pandoc + lualatex."""
    BUILD.mkdir(exist_ok=True)
    c.run(
        "pandoc actes/ratiocinations.md"
        f" -o {BUILD}/ratiocinations.pdf"
        " --pdf-engine=lualatex"
        " -V geometry:margin=2cm"
        " -V lang=fr"
        ' -V mainfont="EB Garamond"'
        " -V fontsize=11pt"
    )
    print(f"  → {BUILD}/ratiocinations.pdf")


@task
@_timed
def pers(c):
    """Build personnages.pdf from personnages.tex + personnages_body.tex via lualatex."""
    _lmk(c, "personnages")


@task(name="postface")
@_timed
def postfaces(c):
    """Build postface_claude.pdf and postface_chatgpt.pdf via pandoc + lualatex."""
    BUILD.mkdir(exist_ok=True)
    _pandoc_opts = (
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
    for src, dest in [
        ("postface_claude.md",   "postface_claude.pdf"),
        ("postface-chatgpt.md",  "postface_chatgpt.pdf"),
    ]:
        c.run(f"pandoc {src} -o {BUILD}/{dest}{_pandoc_opts}")
        print(f"  → {BUILD}/{dest}")


@task(pre=[gitinfo])
@_timed
def total(c):
    """Build LA TOTALE : document unifié annoté + postface + notes + sommaire étendu + personnages."""
    print("=== svg → pdf ===")
    _svg_to_pdf(c)

    print("=== pandoc : postface ChatGPT body ===")
    _pandoc_body(c, "postface-chatgpt.md", "postface_chatgpt_body.tex")

    print("=== pandoc : postface Claude body ===")
    _pandoc_body(c, "postface_claude.md", "postface_claude_body.tex")

    print("=== LA TOTALE ===")
    _lmk(c, f"{BASE}_LA_TOTALE")
    _ls_outputs()

@task(pre=[build])
@_timed
def all_but_diffs(c):
    """Build everything except diffs: main, sommaire, notes, epub, pers, postfaces, total."""
    _lmk(c, f"{BASE}_sommaire")
    notes(c)
    epub(c)
    pers(c)
    postfaces(c)
    total(c)
    _ls_outputs()


@task(pre=[all_but_diffs])
@_timed
def all(c):
    """Build everything: all_but_diffs + diffs + clean."""
    c.run("python3 -u diff_work/make_diff.py")
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

    # build/ : keep only expected output files
    _keep_names = set(_OUTPUT_PDFS) | {f"{BASE}.epub"}
    if BUILD.exists():
        for f in BUILD.iterdir():
            if f.is_file() and f.name not in _keep_names:
                f.unlink()
