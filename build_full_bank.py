"""
build_full_bank.py
Assembles 100 high-quality questions for each of the 6 interview categories:
- software_engineering (100)
- data_science (100)
- product_management (100)
- behavioral (100)
- python_developer (100)
- forensic_science (100)
Total: 600 questions
"""

import json
import os
import shutil

from question_data.se_builder import get_se_questions
from question_data.ds_builder import get_ds_questions
from question_data.pm_builder import get_pm_questions
from question_data.bh_builder import get_bh_questions
from question_data.py_builder import get_py_questions
from question_data.fs_builder import get_fs_questions

def build():
    json_path = "questions.json"
    backup_path = "questions.json.bak"
    
    if os.path.exists(json_path) and not os.path.exists(backup_path):
        shutil.copyfile(json_path, backup_path)
        print(f"Backed up original questions to {backup_path}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        existing_data = json.load(f)

    # 1. Software Engineering: se_1..se_15 + se_16..se_100
    base_se = [q for q in existing_data.get("software_engineering", []) if int(q["id"].split("_")[1]) <= 15]
    new_se = get_se_questions()
    full_se = base_se + new_se

    # 2. Data Science: ds_1..ds_4 + ds_5..ds_100
    base_ds = [q for q in existing_data.get("data_science", []) if int(q["id"].split("_")[1]) <= 4]
    new_ds = get_ds_questions()
    full_ds = base_ds + new_ds

    # 3. Product Management: pm_1..pm_3 + pm_4..pm_100
    base_pm = [q for q in existing_data.get("product_management", []) if int(q["id"].split("_")[1]) <= 3]
    new_pm = get_pm_questions()
    full_pm = base_pm + new_pm

    # 4. Behavioral: bh_1..bh_3 + bh_4..bh_100
    base_bh = [q for q in existing_data.get("behavioral", []) if int(q["id"].split("_")[1]) <= 3]
    new_bh = get_bh_questions()
    full_bh = base_bh + new_bh

    # 5. Python Developer: py_1..py_3 + py_4..py_100
    base_py = [q for q in existing_data.get("python_developer", []) if int(q["id"].split("_")[1]) <= 3]
    new_py = get_py_questions()
    full_py = base_py + new_py

    # 6. Forensic Science: fs_1..fs_2 + fs_3..fs_100
    base_fs = [q for q in existing_data.get("forensic_science", []) if int(q["id"].split("_")[1]) <= 2]
    new_fs = get_fs_questions()
    full_fs = base_fs + new_fs

    new_database = {
        "software_engineering": full_se,
        "data_science": full_ds,
        "product_management": full_pm,
        "behavioral": full_bh,
        "python_developer": full_py,
        "forensic_science": full_fs
    }

    # Strict Validation
    total_count = 0
    print("\n--- Question Bank Validation ---")
    for category, q_list in new_database.items():
        count = len(q_list)
        total_count += count
        prefix = q_list[0]["id"].split("_")[0]
        ids = [q["id"] for q in q_list]
        expected_ids = [f"{prefix}_{i}" for i in range(1, 101)]
        
        assert count == 100, f"Category {category} has {count} questions, expected 100!"
        assert ids == expected_ids, f"Category {category} IDs do not match sequence 1..100! (Found: {ids[:3]} ... {ids[-3:]})"
        
        # Check text uniqueness
        texts = [q["text"].strip().lower() for q in q_list]
        assert len(set(texts)) == 100, f"Category {category} has duplicate question texts!"
        
        # Check schema validity
        for q in q_list:
            assert "id" in q and q["id"], "Missing or empty id"
            assert "text" in q and len(q["text"]) > 10, f"Invalid text in {q['id']}"
            assert q.get("difficulty") in ["Easy", "Medium", "Hard"], f"Invalid difficulty in {q['id']}"
            assert isinstance(q.get("keywords"), list) and len(q["keywords"]) >= 2, f"Keywords invalid in {q['id']}"
            assert "tips" in q and len(q["tips"]) > 5, f"Tips missing in {q['id']}"
            assert "model_answer" in q and len(q["model_answer"]) > 15, f"Model answer missing in {q['id']}"

        diffs = {}
        for q in q_list:
            d = q["difficulty"]
            diffs[d] = diffs.get(d, 0) + 1
        print(f"[OK] {category:<22}: {count} questions | Diff breakdown: Easy={diffs.get('Easy', 0)}, Med={diffs.get('Medium', 0)}, Hard={diffs.get('Hard', 0)}")

    print(f"\nTotal questions assembled: {total_count} / 600")

    # Write out
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(new_database, f, indent=2, ensure_ascii=False)
    
    file_size_kb = os.path.getsize(json_path) / 1024
    print(f"Successfully wrote {json_path} ({file_size_kb:.1f} KB)")

if __name__ == "__main__":
    build()
