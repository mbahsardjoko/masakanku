#!/usr/bin/env python3
import json

# Load recipe data
with open('/tmp/recipe_data.json', 'r') as f:
    data = json.load(f)

slug_map = {item['slug']: item for item in data}

# Template constants from resep-garang-asem.html
CSS_BLOCK = '''    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; line-height: 1.8; color: #333; background: #fef9f4; }
        nav { background: #c0392b; padding: 1rem 0; position: sticky; top: 0; z-index: 100; }
        nav .container { max-width: 1100px; margin: auto; display: flex; justify-content: space-between; align-items: center; padding: 0 1.5rem; flex-wrap: wrap; }
        nav .logo { color: #fff; font-size: 1.5rem; font-weight: 700; text-decoration: none; }
        nav .logo span { color: #fdd835; }
        nav a { color: #fff; text-decoration: none; margin-left: 1.2rem; font-weight: 500; font-size: 0.95rem; }
        nav a:hover { color: #fdd835; }
        .container { max-width: 800px; margin: auto; padding: 2rem 1.5rem; }
        .breadcrumb { font-size: 0.9rem; color: #888; margin-bottom: 1rem; }
        .breadcrumb a { color: #c0392b; text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }
        .category-badge { display: inline-block; background: #f39c12; color: #fff; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; margin-bottom: 1rem; }
        h1 { font-size: 2rem; color: #222; margin-bottom: 0.5rem; line-height: 1.3; }
        .meta-desc { font-size: 1.1rem; color: #666; margin-bottom: 1.5rem; border-left: 4px solid #f39c12; padding-left: 1rem; }
        .article-img { width: 100%; border-radius: 12px; margin: 1.5rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .intro { font-size: 1.05rem; margin-bottom: 1.5rem; }
        h2 { font-size: 1.5rem; color: #f39c12; margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #f5edd0; }
        .ingredients, .steps { background: #fff; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 1.5rem; }
        .ingredients li, .steps li { margin-bottom: 0.6rem; padding-left: 0.5rem; }
        .ingredients ul, .steps ol { padding-left: 1.5rem; }
        .tips-box { background: #fff8e1; border-left: 4px solid #fdd835; padding: 1.2rem 1.5rem; border-radius: 8px; margin: 1.5rem 0; }
        .tips-box h3 { color: #f57f17; margin-bottom: 0.8rem; }
        .tips-box li { margin-bottom: 0.5rem; }
        .cta { text-align: center; background: #f39c12; color: #fff; padding: 1.5rem; border-radius: 12px; margin: 2rem 0; }
        .cta p { font-size: 1.1rem; margin-bottom: 0.5rem; }
        .related { background: #fff; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin: 2rem 0; }
        .related h3 { color: #f39c12; margin-bottom: 1rem; }
        .related a { color: #f39c12; text-decoration: none; display: block; margin-bottom: 0.5rem; }
        .related a:hover { text-decoration: underline; }
        footer { background: #2c2c2c; color: #ccc; padding: 2rem 0; text-align: center; margin-top: 3rem; }
        footer .container { max-width: 800px; margin: auto; padding: 0 1.5rem; }
        footer a { color: #fdd835; text-decoration: none; margin: 0 0.8rem; }
        footer a:hover { text-decoration: underline; }
        footer p { margin-top: 1rem; font-size: 0.9rem; }
        @media (max-width: 600px) {
            h1 { font-size: 1.5rem; }
            nav .container { flex-direction: column; gap: 0.5rem; }
            nav a { margin: 0 0.6rem; font-size: 0.85rem; }
        }
    </style>'''

print("Recipe generator ready")
print(f"Total recipes in data: {len(data)}")