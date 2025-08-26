#!/usr/bin/env python3
"""
Generate simple client-side search indices for 2015 and 2025 documents.
Each index entry includes boosted fields and a short snippet for preview.
"""
from __future__ import annotations
import json
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(ROOT, "data/json")
OUT_DIR = os.path.join(ROOT, "data/search")


def load_doc(year: str) -> dict:
    path = os.path.join(JSON_DIR, f"{year}.json")
    if not os.path.exists(path):
        return {"version": year, "sections": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def block_text(block) -> str:
    t = block.get("type")
    if t == "p":
        return block.get("text", "")
    if t == "list":
        return "\n".join(block.get("items") or [])
    if t == "table":
        rows = block.get("rows") or []
        return "\n".join([" ".join(map(str, r)) for r in rows])
    if t == "ref":
        return block.get("text", "")
    return ""


def build_index(doc: dict) -> dict:
    entries = []
    for s in doc.get("sections", []):
        content_blocks = s.get("content") or []
        text = "\n".join(block_text(b) for b in content_blocks).strip()
        snippet = text[:240] + ("…" if len(text) > 240 else "")
        entries.append({
            "version": doc.get("version"),
            "id": s.get("id"),
            "anchor": s.get("anchor"),
            "title": s.get("title"),
            "path": s.get("path"),
            "tags": s.get("tags") or [],
            "snippet": snippet,
        })
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "version": doc.get("version"),
        "entries": entries,
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for year in ("2015", "2025"):
        doc = load_doc(year)
        idx = build_index(doc)
        out_path = os.path.join(OUT_DIR, f"{year}.index.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(idx, f, ensure_ascii=False, indent=2)
        print(f"Wrote {out_path}")
    # Optional merged index (lightweight concat)
    merged = {"generated_at": datetime.utcnow().isoformat() + "Z", "entries": []}
    for year in ("2015", "2025"):
        p = os.path.join(OUT_DIR, f"{year}.index.json")
        with open(p, "r", encoding="utf-8") as f:
            merged["entries"].extend(json.load(f)["entries"])
    merged_path = os.path.join(OUT_DIR, "merged.index.json")
    with open(merged_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"Wrote {merged_path}")


if __name__ == "__main__":
    main()

