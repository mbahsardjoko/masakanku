#!/usr/bin/env python3
"""
dedupe-index-sitemap.py — Pre-batch cleanup + slug gate for masakanku repo.

Usage:
    python3 scripts/dedupe-index-sitemap.py                        # dedupe index.html + sitemap.xml
    python3 scripts/dedupe-index-sitemap.py --check SLUG1 SLUG2    # verify proposed slugs are NEW (no overwrite risk)

Why this exists:
    Session 2026-08-02: eyeballing the 200+ slug list caused 6/7 chosen recipes to already
    exist (resep-sop-buntut, resep-pecel, resep-sate-padang, resep-martabak-telur,
    resep-lumpia-semarang, resep-opor-ayam), and generation OVERWROTE the existing articles.
    verify_articles.py does NOT catch this (files are structurally valid).
    Run --check BEFORE generating any new article.

Also fixes: the fragile regex approach to rebuilding articleGrid (the old
`re.sub(r'(<div class="row g-3" id="articleGrid\">).*?(</div>\s*</div>\s*<script)')`
boundary fails to match on minified HTML). This uses split() on the grid marker
which is robust against minified layout.

Exit codes: 0 = OK, 1 = issue found (duplicate slug proposed / rebuild failed)
"""
import re, sys, os

REPO = '/tmp/masakanku'
EXCLUDE = {'index', 'contact', 'privacy-policy', 'copyright', 'dmca'}


def dedupe_index():
    path = os.path.join(REPO, 'index.html')
    with open(path, encoding='utf-8') as f:
        html = f.read()
    cards = re.findall(
        r'<div class="col-md-4 col-sm-6"><div class="card h-100">.*?</div></div></div>',
        html, re.DOTALL)
    seen = {}
    for c in cards:
        m = re.search(r'href="/(.*?)"', c)
        if m and m.group(1) not in seen:
            seen[m.group(1)] = c
    parts = html.split('id="articleGrid">')
    if len(parts) != 2 or '<script' not in parts[1]:
        print(f'ERROR: could not locate articleGrid boundaries (parts={len(parts)})')
        return len(cards), len(seen), False
    rest = parts[1].split('<script', 1)
    new_html = (parts[0] + 'id="articleGrid">\n'
                + '\n'.join(seen.values())
                + '\n</div></div>\n<script' + rest[1])
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    return len(cards), len(seen), True


def dedupe_sitemap():
    path = os.path.join(REPO, 'sitemap.xml')
    with open(path, encoding='utf-8') as f:
        s = f.read()
    entries = re.findall(r'  <url>.*?</url>', s, re.DOTALL)
    seen = {}
    for e in entries:
        m = re.search(r'<loc>https://masakanku\.online/([^<]+)</loc>', e)
        if m and m.group(1) not in seen:
            seen[m.group(1)] = e
    if '<url>' not in s:
        print('ERROR: no <url> entries in sitemap')
        return len(entries), len(seen), False
    s = s[:s.index('<url>')] + '\n'.join(seen.values()) + '\n</urlset>'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)
    return len(entries), len(seen), True


def check_slugs(slugs):
    existing = {f[:-5] for f in os.listdir(REPO)
                if f.endswith('.html') and f[:-5] not in EXCLUDE}
    dups = [s for s in slugs if s in existing]
    if dups:
        print('❌ SLUG ALREADY EXISTS — DO NOT OVERWRITE:')
        for s in dups:
            print(f'  /{s}')
        print('Pick different recipes. Overwriting destroys existing content.')
        print('If already committed, restore with: git checkout <slug>.html')
        return False
    print(f'✅ All {len(slugs)} proposed slugs are new.')
    return True


if __name__ == '__main__':
    if '--check' in sys.argv:
        i = sys.argv.index('--check')
        slugs = sys.argv[i + 1:]
        sys.exit(0 if check_slugs(slugs) else 1)
    n1, u1, ok1 = dedupe_index()
    print(f'index.html: {n1} -> {u1} unique cards')
    n2, u2, ok2 = dedupe_sitemap()
    print(f'sitemap.xml: {n2} -> {u2} unique URLs')
    sys.exit(0 if (ok1 and ok2) else 1)
