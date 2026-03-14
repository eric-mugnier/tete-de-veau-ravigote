#!/usr/bin/env python3
"""
find_missing_notes.py
Scan all .tex files in actes/ and find cultural references that likely lack
an endnote (\nf{...}).

Detection passes:
  1. \\textit{Title} not followed by \\nf{ (films, books, operas, songs)
  2. Name (YYYY — person with birth/death year hint
  3. Known cultural markers (places, brands, anthems, orgs) without note
  4. Notable named people (composers, filmmakers, writers…) without note
  5. Guillemet citations that look like song/poem lyrics
"""

import re
from pathlib import Path

ACTES_DIR = Path("/Users/christophe.thiebaud/_Mugnier/actes")
OUTPUT_FILE = Path("/Users/christophe.thiebaud/_Mugnier/missing_notes.md")

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def build_nf_spans(text):
    """Return list of (start, end) ranges covered by \\nf{...} blocks."""
    spans = []
    for m in re.finditer(r'\\nf\{', text):
        nf_start = m.start()
        depth = 0
        j = m.end() - 1  # position of opening '{'
        while j < len(text):
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        spans.append((nf_start, j + 1))
    return spans


def inside_nf_block(pos, nf_spans):
    return any(s < pos < e for s, e in nf_spans)


def has_note_after(text, end_pos, window=35):
    """Return True if \\nf{ appears within `window` chars after position end_pos."""
    return r'\nf{' in text[end_pos: end_pos + window]


# ---------------------------------------------------------------------------
# Pass 1 — \\textit{Title} without note
# ---------------------------------------------------------------------------

EMPHASIS_WORDS = {
    'très', 'pas', 'si', 'non', 'oui', 'peu', 'trop', 'plus',
    'bien', 'mal', 'tout', 'rien', 'même', 'déjà', 'encore',
    'comme', 'mais', 'donc', 'or', 'ni', 'car', 'et', 'son',
    'sic', 'idem', 'ibid', 'op', 'cit', 'in', 'de', 'du',
    'le', 'la', 'les', 'un', 'une', 'des', 'au', 'aux',
    'the', 'of', 'at', 'for', 'to', 'by', 'and', 'or', 'not',
    'est', 'sont', 'fait', 'via', 'vs', 'per', 'se', 'ad', 'hoc',
    'surtout', 'alors', 'aussi', 'toujours', 'jamais', 'enfin',
    'certes', 'voire', 'notamment', 'sinon', 'pourtant',
    'kaijū', 'kaiju',
}


def strip_latex(content):
    """Strip LaTeX markup to get readable text."""
    s = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', content)
    s = re.sub(r'\\[a-zA-Z]+\s*', '', s)
    return s.strip()


def is_emphasis_only(content):
    raw = strip_latex(content).rstrip('.')
    words = raw.split()
    if not words:
        return True
    if len(words) == 1 and words[0].lower() in EMPHASIS_WORDS:
        return True
    if len(words) == 1 and len(words[0]) <= 2:
        return True
    if len(words) <= 2 and all(w[0].islower() for w in words):
        if all(w.lower().rstrip(',;.') in EMPHASIS_WORDS for w in words):
            return True
    return False


def guess_type_from_title(content):
    cl = content.lower()
    if any(w in cl for w in ['symphonie', 'sonate', 'concerto', 'opéra', 'opérette',
                              'requiem', 'messe', 'cantate', 'oratorio', 'chanson',
                              'quartet', 'quintet', 'jazz', 'blues', 'swing',
                              'nocturne', 'étude', 'ballade', 'suite musicale']):
        return 'musique'
    if any(w in cl for w in ['film', 'movie', 'cinéma', 'ciné', 'épisode']):
        return 'film'
    if any(w in cl for w in ['roman', 'livre', 'traité', 'essai', 'mémoire',
                              'poème', 'poésie', 'recueil', 'nouvelle', 'conte',
                              'encyclopédie', 'dictionnaire', 'histoire']):
        return 'livre'
    if re.search(r'\b(19|20)\d{2}\b', content):
        return 'film'
    words = content.split()
    if sum(1 for w in words if w and w[0].isupper()) / max(len(words), 1) >= 0.5 and len(words) >= 2:
        return 'livre'
    return 'autre'


def find_textit_titles(text, nf_spans):
    findings = []
    pattern = re.compile(r'\\textit\{((?:[^{}]|\{[^{}]*\})*)\}')
    for m in pattern.finditer(text):
        pos, content, end = m.start(), m.group(1), m.end()
        if inside_nf_block(pos, nf_spans):
            continue
        if has_note_after(text, end, 30):
            continue
        if is_emphasis_only(content):
            continue
        display = strip_latex(content)
        if not display or is_emphasis_only(display):
            continue
        ttype = guess_type_from_title(display)
        lineno = text[:pos].count('\n') + 1
        findings.append((lineno, f'*{display}*', ttype))
    return findings


# ---------------------------------------------------------------------------
# Pass 2 — Name (YYYY without note
# ---------------------------------------------------------------------------

def find_persons_with_year(text, nf_spans):
    findings = []
    pattern = re.compile(
        r'([A-Z\xc0-\xd6\xd8-\xde][A-Za-z\xc0-\xd6\xd8-\xde\xe0-\xf6\xf8-\xff\-]+'
        r'(?:\s+(?:de\s+|von\s+|van\s+|du\s+)?'
        r'[A-Z\xc0-\xd6\xd8-\xde][A-Za-z\xc0-\xd6\xd8-\xde\xe0-\xf6\xf8-\xff\-]+)*)'
        r'\s*\((\d{4})'
    )
    SKIP = {'Article', 'Chapitre', 'Tome', 'Volume', 'Note', 'Acte', 'Section'}
    for m in pattern.finditer(text):
        pos, name, end = m.start(), m.group(1).strip(), m.end()
        if inside_nf_block(pos, nf_spans):
            continue
        if has_note_after(text, end, 35):
            continue
        if name in SKIP or name.lower() in SKIP:
            continue
        words = name.split()
        if len(words) == 1 and name[0].islower():
            continue
        lineno = text[:pos].count('\n') + 1
        findings.append((lineno, name, 'personne'))
    return findings


# ---------------------------------------------------------------------------
# Pass 3 — Cultural markers (places, brands, anthems…)
# ---------------------------------------------------------------------------

CULTURAL_MARKERS = [
    # Parisian / French places
    (r'\bBoulevard des Capucines\b',   'lieu'),
    (r'\bVel.?\s*d.Hiv\b',             'lieu'),
    (r'\bMoulin Rouge\b',              'lieu'),
    (r'\bFolies[-\s]Berg[eè]re\b',     'lieu'),
    (r'\bLido\b(?!\s*[(-])',           'lieu'),
    (r'\bOp[eé]ra Garnier\b',          'lieu'),
    (r'\bPalais[-\s]Royal\b',          'lieu'),
    (r'\bP[eè]re[-\s]Lachaise\b',      'lieu'),
    (r'\bPigalle\b',                   'lieu'),
    # American venues
    (r'\bCarnegie Hall\b',             'lieu'),
    (r'\bApollo Theater\b',            'lieu'),
    (r'\bCotton Club\b',               'lieu'),
    (r'\bStoryville\b',                'lieu'),
    # Cigar brands used culturally (not just product mention)
    (r'\bCohiba\b',                    'autre'),
    (r'\bMontecristo\b(?!\s*\()',       'autre'),
    (r'\bDom P[eé]rignon\b',           'autre'),
    # Songs / anthems (proper noun form)
    (r"\bL'Internationale\b",          'musique'),
    (r'\bla Marseillaise\b',           'musique'),
    # Historical organisations
    (r'(?<!\w)SS(?!\w)(?!\s*[-\w])',   'autre'),   # SS as Nazi org (standalone)
    # Specific newspaper (with definite article = proper noun)
    (r'\bLe Figaro\b(?!\s*\()',        'autre'),
    # Historical sites / events (genocide / battle)
    (r'\bAuschwitz\b',                 'lieu'),
    (r'\bDachau\b',                    'lieu'),
    (r'\bTreblinka\b',                 'lieu'),
    (r'\bBuchenwald\b',                'lieu'),
    (r'\bVerdun\b',                    'lieu'),
    (r'\bWaterloo\b',                  'lieu'),
    # Vichy regime reference
    (r'\bVichy\b',                     'lieu'),
    # Resistance / Liberation only as historical proper nouns (capital R/L)
    (r'\bla Résistance\b',             'autre'),
    (r'\bla Libération\b',             'autre'),
]


def find_cultural_markers(text, nf_spans):
    findings = []
    for raw_pat, ttype in CULTURAL_MARKERS:
        flags = 0 if raw_pat[0] == '(' else re.IGNORECASE
        # Keep these case-sensitive (proper nouns, single-case markers)
        case_sensitive = {
            r"(?<!\w)SS(?!\w)(?!\s*[-\w])",
            r"\bL'Internationale\b",
            r'\bLe Figaro\b(?!\s*\()',
            r'\bla Résistance\b',
            r'\bla Libération\b',
        }
        if raw_pat in case_sensitive:
            flags = 0
        try:
            pattern = re.compile(raw_pat, flags)
        except re.error:
            continue
        for m in pattern.finditer(text):
            pos, end = m.start(), m.end()
            if inside_nf_block(pos, nf_spans):
                continue
            if has_note_after(text, end, 40):
                continue
            lineno = text[:pos].count('\n') + 1
            findings.append((lineno, m.group(0), ttype))
    return findings


# ---------------------------------------------------------------------------
# Pass 4 — Notable named people without notes
# ---------------------------------------------------------------------------

# (name, type) — only names that appear bare (no \\nf{} pattern near them)
NOTABLE_PEOPLE = [
    # Composers / musicians
    ('Wagner',          'personne'),
    ('Beethoven',       'personne'),
    ('Mozart',          'personne'),
    ('Bach',            'personne'),
    ('Brahms',          'personne'),
    ('Schubert',        'personne'),
    ('Chopin',          'personne'),
    ('Liszt',           'personne'),
    ('Debussy',         'personne'),
    ('Ravel',           'personne'),
    ('Satie',           'personne'),
    ('Mahler',          'personne'),
    ('Verdi',           'personne'),
    ('Puccini',         'personne'),
    ('Rossini',         'personne'),
    ('Bizet',           'personne'),
    ('Berlioz',         'personne'),
    ('Stravinsky',      'personne'),
    ('Coltrane',        'personne'),
    ('Mingus',          'personne'),
    ('Billie Holiday',  'personne'),
    ('Ella Fitzgerald', 'personne'),
    ('Sarah Vaughan',   'personne'),
    ('Gainsbourg',      'personne'),
    ('Brel',            'personne'),
    ('Brassens',        'personne'),
    ('Piaf',            'personne'),
    ('Montand',         'personne'),
    ('Aznavour',        'personne'),
    ('Nougaro',         'personne'),
    # Filmmakers
    ('Hitchcock',       'personne'),
    ('Kubrick',         'personne'),
    ('Bergman',         'personne'),
    ('Godard',          'personne'),
    ('Truffaut',        'personne'),
    ('Fellini',         'personne'),
    ('Antonioni',       'personne'),
    ('Visconti',        'personne'),
    ('Pasolini',        'personne'),
    ('Chaplin',         'personne'),
    # Writers
    ('Proust',          'personne'),
    ('Zola',            'personne'),
    ('Flaubert',        'personne'),
    ('Balzac',          'personne'),
    ('Stendhal',        'personne'),
    ('Baudelaire',      'personne'),
    ('Rimbaud',         'personne'),
    ('Verlaine',        'personne'),
    ('Apollinaire',     'personne'),
    ('Céline',          'personne'),
    ('Kafka',           'personne'),
    ('Borges',          'personne'),
    ('Dostoïevski',     'personne'),
    ('Tolstoï',         'personne'),
    ('Hemingway',       'personne'),
    ('Fitzgerald',      'personne'),
    ('Faulkner',        'personne'),
    # Visual artists
    ('Picasso',         'personne'),
    ('Matisse',         'personne'),
    ('Monet',           'personne'),
    ('Manet',           'personne'),
    ('Renoir',          'personne'),
    ('Cézanne',         'personne'),
    ('Van Gogh',        'personne'),
    ('Dali',            'personne'),
    ('Warhol',          'personne'),
    # Philosophers / thinkers
    ('Nietzsche',       'personne'),
    ('Freud',           'personne'),
    ('Jung',            'personne'),
    ('Marx',            'personne'),
    ('Voltaire',        'personne'),
    ('Rousseau',        'personne'),
]

# Words that look like a notable name but are used differently in context
NAME_FALSE_POSITIVE_CONTEXT = {
    # "Hemingway Short Story" is a cigar brand — keep it, it's a cultural ref
    # "Rousseau" as a wine cuvée or part of donor name — not the philosopher, skip
    'Rousseau': ['Rousseau Deslandes', 'Cuvée Rousseau', 'cuvée Rousseau',
                 'Antoine Rousseau', 'Antoine\xa0Rousseau'],
    # "Dylan" as a character first name — skip
    'Dylan': ['Dylan Passereau'],
    # "Leone" = Sierra Leone — skip
    'Leone': ['Sierra Leone'],
    # "Napoléon" as a cognac grade/brandy — skip
    'Napoléon': ['fine Napoléon', 'Napoléon du'],
    # "Chopin" when Rubinstein already gets a note immediately after
    'Chopin': ['Rubinstein'],
}


def find_notable_people(text, nf_spans):
    findings = []
    for name, ttype in NOTABLE_PEOPLE:
        pattern = re.compile(r'\b' + re.escape(name) + r'\b')
        skip_contexts = NAME_FALSE_POSITIVE_CONTEXT.get(name, [])
        for m in pattern.finditer(text):
            pos, end = m.start(), m.end()
            if inside_nf_block(pos, nf_spans):
                continue
            if has_note_after(text, end, 40):
                continue
            # Check if a note exists within 80 chars (person mentioned, note comes after)
            if has_note_after(text, end, 80):
                continue
            # Context check for false positives
            ctx = text[max(0, pos - 30): pos + 60]
            if any(fp in ctx for fp in skip_contexts):
                continue
            # Skip if this name also appears as a character name (all-caps in dialogue)
            # i.e. preceded by \\textsc{ which would mean it's a character
            pre = text[max(0, pos - 10): pos]
            if '\\textsc{' in pre or '\\textbf{' in pre:
                continue
            lineno = text[:pos].count('\n') + 1
            findings.append((lineno, name, ttype))
    return findings


# ---------------------------------------------------------------------------
# Pass 5 — Guillemet citations (song/poem lines)
# ---------------------------------------------------------------------------

LYRIC_WORDS = {
    'amour', 'coeur', 'cœur', 'âme', 'nuit', 'mort', 'vie', 'dieu',
    'soleil', 'lune', 'étoile', 'vent', 'sang', 'feu',
    'liberté', 'patrie', 'gloire', 'peuple', 'terre',
    'ciel', 'mer', 'pluie', 'joie', 'peine', 'espoir',
    'soir', 'matin', 'heure', 'chanson', 'chanter', 'chante',
    'beau', 'belle', 'fleur', 'printemps', 'hiver',
}

DIALOGUE_STARTERS = {
    'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
    'on', 'ce', 'ça', 'c', 'mon', 'ma', 'ton', 'ta', 'son',
    'quoi', 'pourquoi', 'comment', 'quand', 'où', 'mais',
    'non', 'oui', 'ah', 'oh', 'alors', 'donc', 'ben', 'eh',
    'tiens', 'voilà', 'voila',
}


def find_guillemet_citations(text, nf_spans):
    findings = []
    pattern = re.compile(r'«\s*~?\s*(.{15,150}?)\s*~?\s*»')
    for m in pattern.finditer(text):
        pos, end = m.start(), m.end()
        content = m.group(1).strip().rstrip('~').strip()
        if inside_nf_block(pos, nf_spans):
            continue
        if has_note_after(text, end, 60):
            continue
        words = [w.strip('~,;.!?') for w in content.split() if w.strip('~,;.!?')]
        if len(words) < 6:
            continue
        word_set = {w.lower() for w in words}
        if not (word_set & LYRIC_WORDS):
            continue
        first = words[0].lower() if words else ''
        if first in DIALOGUE_STARTERS:
            continue
        lineno = text[:pos].count('\n') + 1
        display = f'«~{content[:70]}{"…" if len(content) > 70 else ""}~»'
        findings.append((lineno, display, 'musique'))
    return findings


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def deduplicate(findings):
    seen = set()
    result = []
    for lineno, mention, ttype in findings:
        key = (lineno, mention.lower()[:50])
        if key not in seen:
            seen.add(key)
            result.append((lineno, mention, ttype))
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def scan_file(filepath):
    text = filepath.read_text(encoding='utf-8', errors='replace')
    nf_spans = build_nf_spans(text)

    findings = []
    findings += find_textit_titles(text, nf_spans)
    findings += find_persons_with_year(text, nf_spans)
    findings += find_cultural_markers(text, nf_spans)
    findings += find_notable_people(text, nf_spans)
    findings += find_guillemet_citations(text, nf_spans)

    findings = deduplicate(findings)
    findings.sort(key=lambda x: x[0])
    return findings


def main():
    tex_files = sorted(
        p for p in ACTES_DIR.iterdir()
        if p.suffix == '.tex' and not p.name.endswith('_headline.tex')
    )

    all_results = {}
    for f in tex_files:
        results = scan_file(f)
        if results:
            all_results[f.name] = results

    lines = [
        "# Références potentiellement sans note",
        "",
        "| fichier | ligne | mention | type | note? |",
        "|---|---|---|---|---|",
    ]

    total = 0
    for fname in sorted(all_results.keys()):
        entries = all_results[fname]
        for lineno, mention, ttype in entries:
            lines.append(f"| {fname} | {lineno} | {mention} | {ttype} | |")
            total += 1

    lines += [
        "",
        "---",
        f"*Total : {total} références potentiellement sans note, "
        f"dans {len(all_results)} fichier(s).*",
    ]

    OUTPUT_FILE.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f"\n{'='*60}")
    print(f"Résultats écrits dans : {OUTPUT_FILE}")
    print(f"{'='*60}")
    print(f"Total références sans note trouvées : {total}")
    print(f"Fichiers concernés : {len(all_results)}")
    print()
    for fname, entries in sorted(all_results.items()):
        print(f"  {fname}: {len(entries)} référence(s)")
    print()


if __name__ == '__main__':
    main()
