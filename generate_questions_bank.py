"""
Comprehensive Question Bank Generator
Generates 100 distinct, high-quality, professional mock interview questions
for each of the 6 interview domains (600 questions total):
  1. software_engineering (se_1 to se_100)
  2. data_science         (ds_1 to ds_100)
  3. product_management   (pm_1 to pm_100)
  4. behavioral           (bh_1 to bh_100)
  5. python_developer     (py_1 to py_100)
  6. forensic_science     (fs_1 to fs_100)

Preserves existing high-quality curated questions at the top of each category.
"""

import json
import os

def build_question_bank():
    # Read existing questions to preserve
    with open('questions.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)

    # 1. SOFTWARE ENGINEERING
    se_existing = existing_data.get('software_engineering', [])[:15]
    
    # 2. DATA SCIENCE
    ds_existing = existing_data.get('data_science', [])[:4]
    
    # 3. PRODUCT MANAGEMENT
    pm_existing = existing_data.get('product_management', [])[:3]
    
    # 4. BEHAVIORAL
    bh_existing = existing_data.get('behavioral', [])[:3]
    
    # 5. PYTHON DEVELOPER
    py_existing = existing_data.get('python_developer', [])[:3]
    
    # 6. FORENSIC SCIENCE
    fs_existing = existing_data.get('forensic_science', [])[:2]

    print("Existing questions loaded:")
    print(f"  SE: {len(se_existing)}, DS: {len(ds_existing)}, PM: {len(pm_existing)}, BH: {len(bh_existing)}, PY: {len(py_existing)}, FS: {len(fs_existing)}")

if __name__ == '__main__':
    build_question_bank()
