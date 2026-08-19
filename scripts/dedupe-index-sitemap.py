#!/usr/bin/env python3
"""Check for duplicate slugs before generating new articles."""
import sys
import os
import re

def get_existing_slugs(repo_path='/tmp/masakanku'):
    """Extract all existing article slugs from HTML files."""
    slugs = set()
    for f in os.listdir(repo_path):
        if f.endswith('.html') and f not in ('index.html', 'contact.html', 
                                               'privacy-policy.html', 'copyright.html', 
                                               'dmca.html'):
            slugs.add(f.replace('.html', ''))
    return slugs

def check_proposed_slugs(proposed_slugs):
    """Check if proposed slugs already exist."""
    existing = get_existing_slugs()
    duplicates = []
    for slug in proposed_slugs:
        if slug in existing:
            duplicates.append(slug)
    
    if duplicates:
        print(f"❌ DUPLICATE SLUGS FOUND:")
        for dup in duplicates:
            print(f"   - {dup}")
        return False
    else:
        print(f"✅ All {len(proposed_slugs)} proposed slugs are new.")
        return True

if __name__ == '__main__':
    if '--check' in sys.argv:
        idx = sys.argv.index('--check')
        proposed = sys.argv[idx+1:]
        if not proposed:
            print("Usage: python3 dedupe-index-sitemap.py --check slug1 slug2 ...")
            sys.exit(1)
        success = check_proposed_slugs(proposed)
        sys.exit(0 if success else 1)
    else:
        # Show existing count
        existing = get_existing_slugs()
        print(f"Found {len(existing)} existing articles")
