#!/usr/bin/env python3
"""
verify_articles.py — Pre-commit validation for Masakanku articles

Run before `git commit` to catch common issues:
- Duplicate h2 headings in article
- Broken "Baca Juga" links (point to non-existent slugs)
- Missing ad scripts / footer links
- "lo"/"gue" style violations
- Sitemap duplicate entries
- Index.html card mismatches (duplicate slugs, ## in gradient)

Usage:
    python3 verify_articles.py slug1 slug2 ...
    python3 verify_articles.py --all  # checks all article HTML files

Exit codes: 0 = ALL GOOD, 1 = issues found
"""

import sys, os, re, glob, json
from pathlib import Path

REPO = Path('/tmp/masakanku')
EXCLUDE = {'index', 'contact', 'privacy-policy', 'copyright', 'dmca'}

def load_slugs():
    slugs = set()
    for f in REPO.glob('*.html'):
        name = f.stem
        if name not in EXCLUDE:
            slugs.add(name)
    return slugs

EXISTING_SLUGS = load_slugs()

def check_article(slug):
    issues = []
    path = REPO / f"{slug}.html"
    if not path.exists():
        return [f"{slug}: file not found"]

    html = path.read_text(encoding='utf-8')

    # 1. Duplicate h2
    h2s = re.findall(r'<h2>(.*?)</h2>', html)
    if len(h2s) != len(set(h2s)):
        dupes = [h for h in h2s if h2s.count(h) > 1]
        issues.append(f"{slug}: duplicate h2 headings: {set(dupes)}")

    # 2. Baca Juga links valid
    baca_juga = re.findall(r'<a href="/([^"]+)"', html)
    baca_juga = [u for u in baca_juga if u != '/' and not u.startswith('http') and u not in ('contact','privacy-policy','copyright','dmca','sitemap.xml')]
    for link in baca_juga:
        if link not in EXISTING_SLUGS:
            issues.append(f"{slug}: broken Baca Juga link -> /{link} (not in repo)")

    # 3. Ad scripts present (2 containers)
    if html.count('ad-container') < 2:
        issues.append(f"{slug}: missing ad-container (expected 2, found {html.count('ad-container')})")

    # 4. Footer links present
    required_footer = ['contact', 'privacy-policy', 'copyright', 'dmca']
    for link in required_footer:
        if f'href="/{link}"' not in html:
            issues.append(f"{slug}: missing footer link /{link}")

    # 5. Style violations: lo/gue
    for word in [' lo ', ' gue ', ' elo ']:
        if word in html:
            issues.append(f"{slug}: style violation — contains '{word.strip()}' (use neutral/kamu)")

    # 6. Schema.org Recipe markup
    if 'ld+json' not in html:
        issues.append(f"{slug}: missing Schema.org Recipe JSON-LD (run inject-recipe-schema.py)")

    return issues

def check_index():
    issues = []
    path = REPO / 'index.html'
    html = path.read_text()

    # a. ## in gradient (double hash bug)
    if '##' in html:
        # Only flag in gradient context
        gradients = re.findall(r'linear-gradient\(135deg,#[A-F0-9]{6},#[A-F0-9]{6}\)', html)
        for g in gradients:
            if '##' in g:
                issues.append(f"index.html: double hash in gradient: {g}")

    # b. Duplicate card slugs
    card_slugs = re.findall(r'href="/([a-z0-9-]+)"', html)
    card_slugs = [s for s in card_slugs if s not in EXCLUDE and not s.startswith('http')]
    if len(card_slugs) != len(set(card_slugs)):
        dupes = {s for s in card_slugs if card_slugs.count(s) > 1}
        issues.append(f"index.html: duplicate cards for slugs: {dupes}")

    # c. dojo.cc script
    if 'dojo.cc' in html:
        issues.append("index.html: contains dojo.cc/124.js script (injects line numbers in header)")

    return issues

def check_sitemap():
    issues = []
    path = REPO / 'sitemap.xml'
    if not path.exists():
        return ['sitemap.xml not found']

    content = path.read_text()
    urls = re.findall(r'<loc>https://masakanku\.online/([^<]+)</loc>', content)
    urls = [u.rstrip('/') for u in urls]
    if len(urls) != len(set(urls)):
        dupes = {u for u in urls if urls.count(u) > 1}
        issues.append(f"sitemap.xml: duplicate entries: {dupes}")

    return issues

def main():
    if '--all' in sys.argv:
        slugs = sorted(EXISTING_SLUGS)
    else:
        slugs = [s for s in sys.argv[1:] if s != '--all']

    if not slugs:
        print("Usage: python3 verify_articles.py slug1 slug2 ...  OR  python3 verify_articles.py --all")
        sys.exit(1)

    all_issues = []

    # Check individual articles
    for slug in slugs:
        issues = check_article(slug)
        all_issues.extend(issues)

    # Always check index.html and sitemap
    all_issues.extend(check_index())
    all_issues.extend(check_sitemap())

    if all_issues:
        print("❌ ISSUES FOUND:")
        for issue in all_issues:
            print(f"  - {issue}")
        print(f"\nTotal: {len(all_issues)} issue(s)")
        sys.exit(1)
    else:
        print("✅ ALL GOOD. Safe to commit.")
        sys.exit(0)

if __name__ == '__main__':
    main()