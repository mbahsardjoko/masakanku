import json

with open('/tmp/recipe_data.json', 'r') as f:
    data = json.load(f)

slug_map = {item['slug']: item for item in data}
target_slugs = [
    'resep-sayur-asem-jakarta',
    'resep-empal-gepuk',
    'resep-ayam-rica-rica-manado'
]

for slug in target_slugs:
    if slug not in slug_map:
        print(f"Missing: {slug}")
    else:
        print(f"Found: {slug} - {slug_map[slug]['recipe_name']}")