#!/usr/bin/env python3
"""personnages_builder.py — Génère personnages_body.tex depuis personnages.md.

Règles de recherche :
  - terme de recherche = nom de famille (dernier mot significatif du nom en gras)
  - si le nom de famille est partagé par plusieurs personnages → prénom à la place
  - recherche case-sensitive + word-boundary
  - override manuel pour les cas irréductiblement ambigus

Usage : python3 personnages_builder.py
"""

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent

# Ordre narratif des fichiers actes (headlines exclus)
ACTE_FILES = [
    ("actes/acte_01.tex",    "I"),
    ("actes/acte_02.tex",    "II"),
    ("actes/acte_03.tex",    "III"),
    ("actes/acte_04.tex",    "IV"),
    ("actes/acte_05.tex",    "V"),
    ("actes/acte_06_1.tex",  "VI"),
    ("actes/acte_06_2.tex",  "VI"),
    ("actes/acte_07.tex",    "VII"),
    ("actes/acte_08.tex",    "VIII"),
    ("actes/acte_09_1.tex",  "IX"),
    ("actes/acte_09_2.tex",  "IX"),
    ("actes/acte_09_2b.tex", "IX"),
    ("actes/acte_09_3.tex",  "IX"),
    ("actes/acte_09_3b.tex", "IX"),
    ("actes/acte_09_4.tex",  "IX"),
]

# Titres à ignorer en tête de nom
TITLES = {
    "père", "mère", "docteur", "professeur", "monseigneur",
    "brigadier", "chef", "brigadier-chef",
    "comte", "comtesse", "le", "la",
}

# Particules à ignorer (ne constituent pas le nom propre)
PARTICLES = {"de", "du", "des", "d", "dit", "née", "von", "van"}

# Override : (file_index_dans_ACTE_FILES, acte_romain)
# Pour les cas où le terme de recherche matche un homonyme dans le texte
OVERRIDE = {
    # Clé = bold_name exact, valeur = (file_index, line_index, acte_romain)
    # Pour les cas où le terme de recherche matche un homonyme ou un mot étranger
    "Roman":              (12, 0, "IX"),  # "Roman Bozhko" dans acte VIII est un autre Roman
    "Samuel Girard":      ( 5, 0, "VI"),  # "Girard" matche un autre Girard en acte II
    "Lou De La Croix":    ( 9, 0, "IX"),  # "Croix" matche une référence en acte II
    "Virginie Beaugendre":( 2, 0, "III"), # "Virginie" matche l'état de Virginie (Jefferson) en acte I
}


# ─── parsing personnages.md ────────────────────────────────────────────────────

def split_at_first_comma(s):
    """Coupe au premier ',' hors parenthèses et guillemets."""
    depth = 0
    for i, c in enumerate(s):
        if c in "(«":
            depth += 1
        elif c in ")»":
            depth -= 1
        elif c == "," and depth == 0:
            return s[:i].rstrip(), s[i+1:].lstrip()
    return s, ""


def parse_entry(line):
    """Parse '**Nom** [suffix], description' → (bold_name, suffix, description) ou None."""
    m = re.match(r"\*\*(.+?)\*\*(.*)", line)
    if not m:
        return None
    bold_name = m.group(1).strip()
    rest      = m.group(2).strip()
    suffix, description = split_at_first_comma(rest)
    if not description:
        return None
    return bold_name, suffix.strip(), description.strip()


def load_entries():
    text = (ROOT / "personnages.md").read_text(encoding="utf-8")
    entries = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("|"):
            continue
        result = parse_entry(line)
        if result:
            entries.append(result)
    return entries


# ─── extraction du terme de recherche ─────────────────────────────────────────

def extract_name_parts(bold_name):
    """
    Retourne (prénom, nom_de_famille) en supprimant titres et particules.
    Si un seul mot reste, retourne (mot, mot).
    """
    # Tokenise en mots (gère les traits d'union composés)
    words = re.findall(r"[A-ZÀ-Öa-zà-öÙ-Üù-ü]+(?:-[A-ZÀ-Öa-zà-öÙ-Üù-ü]+)*", bold_name)
    # Supprime les titres en tête
    while words and words[0].lower() in TITLES:
        words.pop(0)
    # Garde seulement les mots significatifs (hors particules)
    meaningful = [w for w in words if w.lower() not in PARTICLES and len(w) > 1]
    if not meaningful:
        return bold_name, bold_name  # fallback
    if len(meaningful) == 1:
        return meaningful[0], meaningful[0]
    return meaningful[0], meaningful[-1]  # (prénom, nom_de_famille)


def build_search_terms(entries):
    """
    Pour chaque entrée, détermine le(s) terme(s) de recherche :
    - nom de famille seul si unique dans la liste
    - [prénom, nom_de_famille] (recherche AND sur même ligne) si nom partagé
    """
    last_names = [extract_name_parts(e[0])[1] for e in entries]
    counts = Counter(last_names)

    terms = []
    for bold_name, suffix, description in entries:
        first, last = extract_name_parts(bold_name)
        if counts[last] > 1:
            # Famille partagée : exiger prénom ET nom sur la même ligne
            terms.append([first, last])
        else:
            terms.append([last])
    return terms


# ─── recherche dans les actes ──────────────────────────────────────────────────

def strip_braced_cmd(text, cmd):
    """Supprime toutes les occurrences de \\cmd{...} (avec braces imbriquées)."""
    result = []
    i = 0
    marker = "\\" + cmd + "{"
    while i < len(text):
        if text[i:i+len(marker)] == marker:
            depth = 0
            j = i + len(marker) - 1  # pointe sur '{'
            while j < len(text):
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        i = j + 1
                        break
                j += 1
            else:
                i = j
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def preprocess(text):
    """Supprime les contenus qui ne font pas partie du récit principal."""
    # Footnotes et leurs sources
    text = strip_braced_cmd(text, "nf")
    # Commandes iconographie (arguments non narratifs)
    text = strip_braced_cmd(text, "iconographietex")
    text = strip_braced_cmd(text, "iconographieimg")
    return text


def _search(term_list, acte_files):
    """Cherche la première ligne contenant TOUS les termes (AND)."""
    patterns = [re.compile(r"\b" + re.escape(t) + r"\b") for t in term_list]
    for fi, (filepath, acte) in enumerate(acte_files):
        path = ROOT / filepath
        if not path.exists():
            continue
        clean = preprocess(path.read_text(encoding="utf-8"))
        for li, line in enumerate(clean.splitlines()):
            if re.match(r"^\s*\\(chapter|input|begin|end|iconographie)", line):
                continue
            if all(p.search(line) for p in patterns):
                return (fi, li, acte)
    return (9999, 9999, "?")


def find_first(term_list, acte_files):
    """
    Recherche AND sur tous les termes.
    Si non trouvé, fallback sur le premier terme seul (prénom).
    """
    pos = _search(term_list, acte_files)
    if pos[0] == 9999 and len(term_list) > 1:
        # Fallback : chercher le prénom seul
        pos = _search([term_list[0]], acte_files)
    return pos


# ─── conversion Markdown → LaTeX ──────────────────────────────────────────────

def md2tex(s):
    s = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", s)   # italique
    s = s.replace("&", r"\&")
    s = re.sub(r"\b(\d+)e\b", r"\1\\up{e}", s)      # 6e → 6\up{e}
    return s


def name_to_tex(bold_name):
    return r"\textsc{" + md2tex(bold_name) + "}"


def suffix_to_tex(suffix):
    return (" " + md2tex(suffix)) if suffix else ""


# ─── génération ───────────────────────────────────────────────────────────────

HEADER = r"""
Personnages par ordre d'apparition. Les références historiques ou culturelles
citées en notes de bas de page ne sont pas comptabilisées.

\bigskip
{\setlength{\parindent}{0pt}\setlength{\parskip}{0.4\onelineskip}
"""

FOOTER = "\n}\n"


def generate():
    entries    = load_entries()
    term_list  = build_search_terms(entries)

    ranked = []
    for (bold_name, suffix, description), terms in zip(entries, term_list):
        if bold_name in OVERRIDE:
            pos = OVERRIDE[bold_name]
        else:
            pos = find_first(terms, ACTE_FILES)
        ranked.append((pos, terms, bold_name, suffix, description))

    ranked.sort(key=lambda x: x[0])

    lines = [HEADER]
    for pos, term, bold_name, suffix, description in ranked:
        fi, li, acte = pos
        name_tex   = name_to_tex(bold_name)
        suffix_tex = suffix_to_tex(suffix)
        desc_tex   = md2tex(description)
        lines.append(rf"\noindent{name_tex}{suffix_tex}, {desc_tex}" + "\n")
    lines.append(FOOTER)

    out = ROOT / "personnages_body.tex"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  → {out}  ({len(ranked)} personnages)")

    not_found = [(b, t) for (fi, _, _), t, b, _, _ in ranked if fi == 9999]
    if not_found:
        print("  ⚠ introuvables dans les actes :")
        for b, t in not_found:
            print(f"      {b!r}  (termes : {t!r})")


if __name__ == "__main__":
    generate()
