from pathlib import Path

# Root directory containing product folders
ROOT_DIR = Path("knowledge_base/catalog/products")

# New product.yaml template
TEMPLATE = """schema_version: 1

product_id:
slug:

name:
  bn:
  en:

category:
subcategory:

status: active
visibility: public

origin:
  region:
  country: Bangladesh

availability:
  seasonal: false

pricing:
  currency: BDT

languages_supported:
  - bn
  - en
  - banglish

aliases: []

tags: []

embedding_context: ""

retrieval:
  priority: 0.90
  business_critical: true
  boost_terms: []

content_defaults:
  primary_language: bn
  fallback_language: en

updated_at:
"""

# TEMPLATE2 = """product_id:

# name:
#   bn:
#   en:

# category:

# visibility: public

# origin:
#   region:
#   country: Bangladesh

# availability:
#   seasonal: false

# pricing:
#   currency: BDT

# languages_supported:
#   - bn
#   - en
#   - banglish

# aliases: []

# retrieval:
#   priority: 0.90
#   business_critical: true
# """


# Find all product.yaml files recursively
yaml_files = ROOT_DIR.rglob("product.yaml")

updated_count = 0

for yaml_file in yaml_files:
    try:
        yaml_file.write_text(TEMPLATE, encoding="utf-8")
        print(f"[UPDATED] {yaml_file}")
        updated_count += 1

    except Exception as e:
        print(f"[FAILED] {yaml_file} -> {e}")

print(f"\nDone. Updated {updated_count} product.yaml files.")