"""
note_urls.py - list all \\source{} URLs that are not in the fr.wikipedia domain.
Writes the result to note_urls.md, sorted alphabetically.
"""

import re, glob, os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_MD = os.path.join(ROOT, "note_urls.md")

SOURCE_RE = re.compile(r'\\source\{([^}]+)\}')

def is_fr_wikipedia(url):
    return "fr.wikipedia.org" in url

urls = set()
for filepath in sorted(glob.glob(os.path.join(ROOT, "actes", "*.tex"))):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    for m in SOURCE_RE.finditer(content):
        url = m.group(1).strip()
        if not is_fr_wikipedia(url):
            urls.add(url)

def to_real_url(latex_url):
    """Strip LaTeX escaping and prepend https:// to produce a clickable URL."""
    u = latex_url.replace(r'\_', '_').replace(r'\%', '%').replace(r'\&', '&')
    if not u.startswith("http"):
        u = "https://" + u
    return u

sorted_urls = sorted(urls, key=str.casefold)

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write(f"# Source URLs outside fr.wikipedia ({len(sorted_urls)})\n\n")
    for url in sorted_urls:
        f.write(f"- [{url}]({to_real_url(url)})\n")

print(f"Written {len(sorted_urls)} URLs to note_urls.md")
