"""Pre-commit verification for masakanku batch publish.

Run this from the repo root BEFORE `git commit`. It catches the most common
publish-blocking issues:

  1. New article HTML files don't have duplicate <h2> headings.
  2. All "Baca Juga" links point to slugs that actually exist in the repo.
  3. Ad scripts (jabturfembitter + atOptions) and dojo.cc are present.
  4. Footer links to remoteproduktif.online and fattan.my.id are intact.
  5. Bahasa: zero occurrences of "lo"/"gue" (style guide).
  6. Sitemap has entries for every new article, and no duplicates.
  7. Index cards inserted at least once per new article.

Usage:
    python3 scripts/verify_articles.py soto-bandung bakso-goreng-crispy ...

If slug args are omitted, the script verifies all HTML files present in the
repo that were NOT in the previous git HEAD (untracked + modified).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

REPO = "/tmp/masakanku"
AD_TOP = "jabturfembitter.com/fbf97f8372ae4f56ef2fbb64a6663968"
AD_BOTTOM = "atOptions="
DOJO = "dojo.cc/124.js"
REMOTEPRODUKTIF = "remoteproduktif.online"
FATTAN = "fattan.my.id"

# Slugs in masakanku.online that DO NOT use the "resep-" prefix. If you write
# "/resep-capcay-goreng" you get a 404. This is the verified non-prefix list
# at the time of writing — extend if you find more.
NO_PREFIX_SLUGS = frozenset({
    "ayam-beku-tahan-berapa-lama", "ayam-goreng-mangga-besar", "ayam-penyet",
    "bakso-sapi", "capcay-goreng",
    "cara-buat-ayam-goreng-berempah", "cara-memasak-ayam-goreng-lengkuas",
    "cara-membuat-jenang-sumsum", "cara-membuat-yogurt-dari-susu-sapi",
    "cara-membuat-zuppa-soup",
    "coto-makassar", "dendeng-balado", "gado-gado",
    "ikan-bakar-jimbaran", "ikan-patin-kuah-kuning",
    "kari-kambing", "kerak-telor", "kue-cubit",
    "masakan-padang-sederhana-jakarta", "masakan-rumahan-sederhana-enak",
    "mie-aceh", "mie-goreng", "nasi-bakar", "nasi-kebuli",
    "olahan-ayam-goreng-sisa", "olahan-ayam-kampung-agar-tidak-bosan",
    "olahan-ayam-kuah-pedas", "olahan-ayam-masakan-nusantara",
    "olahan-ayam-untuk-bekal", "olahan-ayam-yang-sehat",
    "rujak-cingur", "sate-ayam", "sate-lilit",
    "soto-ayam", "soto-lamongan", "tahu-tek",
    "tempe-mendoan", "tepung-ayam-goreng-sasa",
    "tinutuan-bubur-manado",
})


def existing_slugs() -> set[str]:
    return {f[:-5] for f in os.listdir(REPO) if f.endswith(".html")}


def new_slugs(args: list[str]) -> list[str]:
    if args:
        return args
    out = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=REPO, capture_output=True, text=True, check=True,
    )
    return [f[:-5] for f in out.stdout.splitlines() if f.endswith(".html")]


def check_one(slug: str, existing: set[str]) -> list[str]:
    path = os.path.join(REPO, f"{slug}.html")
    if not os.path.exists(path):
        return [f"{slug}: file missing"]
    with open(path, encoding="utf-8") as f:
        html = f.read()
    errors: list[str] = []

    # 1. duplicate <h2>
    h2 = re.findall(r"<h2>([^<]+)</h2>", html)
    seen: dict[str, int] = {}
    for heading in h2:
        seen[heading] = seen.get(heading, 0) + 1
    for h, c in seen.items():
        if c > 1:
            errors.append(f"duplicate <h2> '{h}' x{c}")

    # 2. baca juga links
    m = re.search(r"<h3>Baca Juga</h3>(.*?)</div>", html, re.S)
    if not m:
        errors.append("missing 'Baca Juga' block")
    else:
        for href in re.findall(r'href="(/([^"]+))"', m.group(1)):
            _, path_part = href
            if path_part not in existing:
                errors.append(f"broken baca-juga: /{path_part}")

    # 3. ad scripts + dojo
    if AD_TOP not in html:
        errors.append(f"missing top ad ({AD_TOP})")
    if AD_BOTTOM not in html:
        errors.append(f"missing bottom ad ({AD_BOTTOM})")
    if DOJO not in html:
        errors.append(f"missing dojo script ({DOJO})")

    # 4. footer links
    if REMOTEPRODUKTIF not in html:
        errors.append(f"missing footer link ({REMOTEPRODUKTIF})")
    if FATTAN not in html:
        errors.append(f"missing footer link ({FATTAN})")

    # 5. bahasa check (no "lo" / "gue")
    bad = re.findall(r"\b(lo|gue)\b", html)
    if bad:
        errors.append(f"contains 'lo'/'gue' x{len(bad)} — rephrase to neutral style")

    return errors


def check_sitemap(slugs: list[str]) -> list[str]:
    path = os.path.join(REPO, "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        sm = f.read()
    errors: list[str] = []
    for slug in slugs:
        needle = f"https://masakanku.online/{slug}"
        count = sm.count(needle)
        if count == 0:
            errors.append(f"sitemap: missing entry for {slug}")
        elif count > 1:
            errors.append(f"sitemap: duplicate entry for {slug} x{count}")
    return errors


def check_index_cards(slugs: list[str]) -> list[str]:
    path = os.path.join(REPO, "index.html")
    with open(path, encoding="utf-8") as f:
        idx = f.read()
    errors: list[str] = []
    for slug in slugs:
        needle = f'href="/{slug}"'
        if idx.count(needle) < 2:
            errors.append(f"index.html: card missing or weak for {slug}")
    return errors


def main(argv: list[str]) -> int:
    slugs = new_slugs(argv)
    if not slugs:
        print("No new article slugs to verify. Pass slugs as args, or run from repo with new files.")
        return 1
    print(f"Verifying {len(slugs)} articles: {', '.join(slugs)}")
    existing = existing_slugs()
    all_errors: list[str] = []
    for slug in slugs:
        for e in check_one(slug, existing):
            all_errors.append(f"{slug}: {e}")
    all_errors.extend(check_sitemap(slugs))
    all_errors.extend(check_index_cards(slugs))

    if all_errors:
        print("\nFAIL — fix these before committing:")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    print("\nALL GOOD. Safe to commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
