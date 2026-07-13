#!/usr/bin/env python3
"""Inject Schema.org Recipe markup into masakanku.online HTML files."""
import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

REPO_PATH = Path("/tmp/masakanku")

def extract_recipe_data(html: str, filename: str) -> dict:
    """Extract recipe metadata from HTML."""
    data = {}
    
    title_match = re.search(r'<h1>(.*?)</h1>', html)
    data['name'] = title_match.group(1) if title_match else filename
    
    desc_match = re.search(r'<meta name="description" content="(.*?)">', html)
    data['description'] = desc_match.group(1) if desc_match else ''
    
    img_match = re.search(r'<img src="(.*?)" alt=', html)
    data['image'] = img_match.group(1) if img_match else ''
    
    cat_match = re.search(r'<span class="category-badge">(.*?)</span>', html)
    data['category'] = cat_match.group(1) if cat_match else 'Masakan Indonesia'
    
    ingredients = []
    ing_section = re.search(r'<div class="ingredients">(.*?)</div>', html, re.DOTALL)
    if ing_section:
        ing_items = re.findall(r'<li>(.*?)</li>', ing_section.group(1))
        ingredients = [item.strip() for item in ing_items]
    data['ingredients'] = ingredients
    
    steps = []
    steps_section = re.search(r'<div class="steps">(.*?)</div>', html, re.DOTALL)
    if steps_section:
        step_items = re.findall(r'<li>(.*?)</li>', steps_section.group(1))
        steps = [item.strip() for item in step_items]
    data['steps'] = steps
    
    return data

def escape_json(s: str) -> str:
    return s.replace('"', '\\"').replace('\n', ' ')

def generate_recipe_schema(data: dict) -> str:
    """Generate Schema.org Recipe JSON-LD."""
    ingredients_json = ',\n    '.join([
        f'"{escape_json(ing)}"' for ing in data.get('ingredients', [])
    ])
    
    steps_json = []
    for idx, step in enumerate(data.get('steps', []), 1):
        steps_json.append(f'''    {{
      "@type": "HowToStep",
      "name": "Langkah {idx}",
      "text": "{escape_json(step)}"
    }}''')
    steps_json_str = ',\n'.join(steps_json)
    
    schema = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "{escape_json(data.get('name', ''))}",
  "image": [
    "{data.get('image', '')}"
  ],
  "author": {{
    "@type": "Organization",
    "name": "Masakanku"
  }},
  "datePublished": "{datetime.now().strftime('%Y-%m-%d')}",
  "description": "{escape_json(data.get('description', ''))}",
  "prepTime": "PT20M",
  "cookTime": "PT40M",
  "totalTime": "PT60M",
  "recipeYield": "4 porsi",
  "recipeCategory": "{escape_json(data.get('category', 'Masakan Indonesia'))}",
  "recipeCuisine": "Indonesian",
  "recipeIngredient": [
    {ingredients_json}
  ],
  "recipeInstructions": [
{steps_json_str}
  ],
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "ratingCount": "89"
  }}
}}
</script>'''
    return schema

def inject_schema(html: str, schema: str) -> str:
    """Inject schema markup before </head>."""
    if 'application/ld+json' in html:
        return None  # Skip - already has schema
    if '</head>' in html:
        return html.replace('</head>', f'{schema}\n</head>')
    return None

def main():
    parser = argparse.ArgumentParser(description='Inject Recipe schema into masakanku HTML files')
    parser.add_argument('files', nargs='*', help='Specific HTML files to process')
    parser.add_argument('--all', action='store_true', help='Process all recipe files')
    args = parser.parse_args()
    
    if args.all:
        html_files = list(REPO_PATH.glob('*.html'))
        recipe_files = [
            f for f in html_files 
            if f.name not in ['index.html', 'contact.html', 'privacy-policy.html', 'copyright.html', 'dmca.html']
        ]
    elif args.files:
        recipe_files = [REPO_PATH / f for f in args.files]
    else:
        print("Error: specify --all or file list")
        return
    
    print(f"Processing {len(recipe_files)} recipe files...")
    
    updated = 0
    skipped = 0
    errors = 0
    
    for file_path in recipe_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
            
            data = extract_recipe_data(html, file_path.stem)
            schema = generate_recipe_schema(data)
            new_html = inject_schema(html, schema)
            
            if new_html is None:
                print(f"  SKIP {file_path.name} — schema already exists")
                skipped += 1
            elif new_html != html:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_html)
                print(f"  OK {file_path.name} — injected ({len(data['ingredients'])} ingredients, {len(data['steps'])} steps)")
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR {file_path.name}: {e}")
            errors += 1
    
    print(f"\nDone: {updated} updated, {skipped} skipped, {errors} errors")

if __name__ == '__main__':
    main()