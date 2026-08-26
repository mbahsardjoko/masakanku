#!/usr/bin/env python3
import sys, re, os

def check_slugs(proposed):
    """Check if proposed slugs already exist in repo"""
    existing = set()
    for f in os.listdir('/tmp/masakanku'):
        if f.endswith('.html') and f not in ('index.html', 'contact.html', 'privacy-policy.html', 'copyright.html', 'dmca.html'):
            existing.add(f.replace('.html', ''))
    
    conflicts = []
    for slug in proposed:
        if slug in existing:
            conflicts.append(slug)
    
    if conflicts:
        print(f"❌ SLUG COLLISION DETECTED:")
        for s in conflicts:
            print(f"   - {s} ALREADY EXISTS")
        return False
    else:
        print(f"✅ All {len(proposed)} proposed slugs are new.")
        return True

if __name__ == '__main__':
    if '--check' in sys.argv:
        slugs = [s for s in sys.argv[1:] if s != '--check']
        if not slugs:
            print("Usage: python3 dedupe-index-sitemap.py --check slug1 slug2 ...")
            sys.exit(1)
        success = check_slugs(slugs)
        sys.exit(0 if success else 1)
