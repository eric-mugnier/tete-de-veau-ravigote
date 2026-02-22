#!/usr/bin/env python3
"""
check_ltex.py — Vérifie les fichiers LaTeX sous actes/ avec ltex-cli-plus,
en reprenant la configuration LTeX+ du projet (.vscode/).

Usage : python3 check_ltex.py [fichier_ou_dossier ...]
        (par défaut : actes/)
"""

import json, re, subprocess, sys, tempfile, os
from pathlib import Path

BASE   = Path(__file__).parent
VSCODE = BASE / '.vscode'
LTEX   = (Path.home() / '.vscode/extensions'
          / 'ltex-plus.vscode-ltex-plus-15.6.1'
          / 'lib/ltex-ls-plus-18.6.1/bin/ltex-cli-plus')

# ── Lecture des fichiers de configuration ────────────────────────────────────

def read_lines(path):
    """Lit un fichier texte, ignore les lignes vides et les commentaires #."""
    if not path.exists():
        return []
    return [l.strip() for l in path.read_text(encoding='utf-8').splitlines()
            if l.strip() and not l.strip().startswith('#')]

def read_false_positives(path):
    """Lit les faux-positifs masqués (un JSON par ligne)."""
    if not path.exists():
        return []
    result = []
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line:
            try:
                result.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return result

def load_settings_jsonc(path):
    """Charge un fichier JSONC (JSON avec commentaires // et /* */)."""
    text = path.read_text(encoding='utf-8')
    # Supprime les commentaires // (hors strings)
    text = re.sub(r'//[^\n]*', '', text)
    # Supprime les commentaires /* ... */
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return json.loads(text)

# ── Construction de la configuration client ───────────────────────────────────

settings = load_settings_jsonc(VSCODE / 'settings.json')

dict_words   = read_lines(VSCODE / 'ltex-dictionary-fr.txt')
disabled_fr  = (read_lines(VSCODE / 'ltex.disabledRules.fr.txt')
                + settings.get('ltex.disabledRules', {}).get('fr', []))
hidden_fr    = read_false_positives(VSCODE / 'ltex.hiddenFalsePositives.fr.txt')

client_cfg = {
    'ltex.language': 'fr',
    'ltex.dictionary': {
        'fr': dict_words,
    },
    'ltex.disabledRules': {
        'fr': list(dict.fromkeys(disabled_fr)),   # déduplique
    },
    'ltex.hiddenFalsePositives': {
        'fr': hidden_fr,
    },
    'ltex.latex.commands':      settings.get('ltex.latex.commands', {}),
    'ltex.latex.environments':  settings.get('ltex.latex.environments', {}),
    'ltex.additionalRules.enablePickyRules': False,
    'ltex.additionalRules.motherTongue': 'fr',
}

# ── Lancement de ltex-cli-plus ────────────────────────────────────────────────

targets = sys.argv[1:] or [str(BASE / 'actes')]

with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                 delete=False, encoding='utf-8') as f:
    json.dump(client_cfg, f, ensure_ascii=False, indent=2)
    cfg_path = f.name

try:
    result = subprocess.run(
        [str(LTEX), f'--client-configuration={cfg_path}'] + targets,
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        cwd=str(BASE),
    )
finally:
    os.unlink(cfg_path)

# ── Parsing et affichage des diagnostics ──────────────────────────────────────

errors_found = False

for line in result.stdout.splitlines():
    line = line.strip()
    if not line:
        continue
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        continue

    # ltex-cli émet des objets {"uri":..., "diagnostics":[...]}
    if 'diagnostics' not in data:
        continue

    uri  = data.get('uri', '')
    diags = data['diagnostics']
    if not diags:
        continue

    # Chemin relatif pour l'affichage
    try:
        rel = Path(uri.replace('file://', '')).relative_to(BASE)
    except ValueError:
        rel = uri

    print(f'\n{rel}  ({len(diags)} erreur(s))')
    print('─' * 70)
    for d in diags:
        r    = d.get('range', {})
        line_no = r.get('start', {}).get('line', '?')
        msg  = d.get('message', '')
        rule = d.get('code', '')
        print(f'  l.{line_no+1 if isinstance(line_no, int) else line_no}  [{rule}]  {msg}')
    errors_found = True

if not errors_found:
    print('✓  Aucune erreur LTeX+ détectée.')

if result.returncode not in (0, 1):
    print('\n[stderr]', result.stderr[-500:] if result.stderr else '(vide)')
