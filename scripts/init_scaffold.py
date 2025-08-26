#!/usr/bin/env python3
"""
Initialize project scaffolding for the ATA guideline comparison.

Creates the data/ directories and writes minimal JSON templates for
2015 and 2025 if they don't exist yet. This script does not parse PDFs;
it only prepares structure following AGENTS.md contracts.
"""
from __future__ import annotations
import json
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIRS = [
    "data/raw",
    "data/json",
    "data/diff",
    "data/toc",
    "data/search",
    "export",
]

PDFS = [
    ("2015", "2015 ATA thyroid nodule and cancer.pdf"),
    ("2025", "2025 ATA thyroid nodule and cancer.pdf"),
]


def ensure_dirs():
    for d in DATA_DIRS:
        path = os.path.join(ROOT, d)
        os.makedirs(path, exist_ok=True)


def write_json_if_absent(year: str, source_name: str):
    out_path = os.path.join(ROOT, "data/json", f"{year}.json")
    if os.path.exists(out_path):
        return
    template = {
        "version": year,
        "title": "ATA Thyroid Nodule and Cancer Guidelines",
        "source_file": source_name,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "sections": [],
        "notes": "Placeholder file. Populate via Structuring Agent after extraction.",
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)


def write_toc_placeholder(year: str):
    out_path = os.path.join(ROOT, "data/toc", f"{year}.toc.json")
    if os.path.exists(out_path):
        return
    placeholder = {
        "version": year,
        "nodes": [],
        "notes": "Placeholder TOC. Generate after sections are structured.",
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(placeholder, f, ensure_ascii=False, indent=2)


def write_diff_placeholder():
    out_path = os.path.join(ROOT, "data/diff", "diff.json")
    if os.path.exists(out_path):
        return
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "pairs": [],
            "summary": {"new": 0, "modified": 0, "removed": 0, "unchanged": 0},
            "notes": "Placeholder diff file. Compute after structuring both years.",
        }, f, ensure_ascii=False, indent=2)


def main():
    ensure_dirs()
    for year, pdf in PDFS:
        write_json_if_absent(year, pdf)
        write_toc_placeholder(year)
    write_diff_placeholder()
    print("Scaffold initialized. Edit data/json/*.json once extraction is ready.")


if __name__ == "__main__":
    main()

