#!/usr/bin/env python3
import sys, re, os

def check_slugs(proposed_slugs):
    """Check if proposed slugs already exist in HTML files"""
    existing = set()
    for f in os.listdir('/tmp/masakanku'):
        if f.endswith('.html') and f not in ('index.html', 'contact.html', 'privacy-policy.html', 'copyright.html', 'dmca.html'):
            existing.add(f.replace('.html', ''))
    
    duplicates = []
    for slug in proposed_slugs:
        if slug in existing:
            duplicates.append(slug)
    
    if duplicates:
        print(f"❌ SLUG COLLISION DETECTED:")
        for dup in duplicates:
            print(f"   - {dup}.html ALREADY EXISTS")
        sys.exit(1)
    else:
        print(f"✅ All {len(proposed_slugs)} proposed slugs are new.")
        sys.exit(0)

if __name__ == '__main__':
    if '--check' in sys.argv:
        slugs = [arg for arg in sys.argv[2:] if arg != '--check']
        check_slugs(slugs)
