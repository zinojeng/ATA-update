#!/usr/bin/env python3
"""
Generate a preliminary diff between 2015 and 2025 JSON documents.
Matches sections primarily by `path+title` and summarizes change types.
If no content exists yet, it emits an empty but valid diff file.
"""
from __future__ import annotations
import json
import os
import sys
from datetime import datetime
from difflib import SequenceMatcher

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_2015 = os.path.join(ROOT, "data/json/2015.json")
JSON_2025 = os.path.join(ROOT, "data/json/2025.json")
OUT_DIFF = os.path.join(ROOT, "data/diff/diff.json")


def load_json(path: str) -> dict:
    if not os.path.exists(path):
        return {"version": os.path.basename(path).split(".")[0], "sections": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def section_key(sec: dict) -> str:
    path = (sec.get("path") or "").strip()
    title = (sec.get("title") or "").strip().lower()
    return f"{path}||{title}"


def stringify_content(blocks: list) -> str:
    parts = []
    for b in blocks or []:
        t = b.get("type")
        if t == "p":
            parts.append(b.get("text", ""))
        elif t == "list":
            items = b.get("items") or []
            parts.append("\n".join(items))
        elif t == "table":
            rows = b.get("rows") or []
            parts.append("\n".join(["\t".join(map(str, r)) for r in rows]))
        elif t == "ref":
            parts.append(b.get("text", ""))
    return "\n".join(parts)


def diff_text(a: str, b: str):
    sm = SequenceMatcher(a=a.splitlines(), b=b.splitlines())
    ops = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        ops.append({
            "type": {
                "equal": "equal",
                "replace": "replace",
                "delete": "delete",
                "insert": "insert",
            }[tag],
            "a_range": [i1, i2],
            "b_range": [j1, j2],
        })
    return ops


def main():
    doc_a = load_json(JSON_2015)
    doc_b = load_json(JSON_2025)

    a_map = {section_key(s): s for s in doc_a.get("sections", [])}
    b_map = {section_key(s): s for s in doc_b.get("sections", [])}

    keys = set(a_map.keys()) | set(b_map.keys())
    pairs = []
    summary = {"new": 0, "modified": 0, "removed": 0, "unchanged": 0}

    for k in sorted(keys):
        a_sec = a_map.get(k)
        b_sec = b_map.get(k)
        if a_sec and not b_sec:
            status = "removed"
            summary[status] += 1
            pairs.append({
                "key": k,
                "status": status,
                "a": {
                    "version": "2015",
                    "id": a_sec.get("id"),
                    "anchor": a_sec.get("anchor"),
                    "title": a_sec.get("title"),
                },
                "b": None,
                "diff": []
            })
        elif b_sec and not a_sec:
            status = "new"
            summary[status] += 1
            pairs.append({
                "key": k,
                "status": status,
                "a": None,
                "b": {
                    "version": "2025",
                    "id": b_sec.get("id"),
                    "anchor": b_sec.get("anchor"),
                    "title": b_sec.get("title"),
                },
                "diff": []
            })
        else:
            a_text = stringify_content(a_sec.get("content"))
            b_text = stringify_content(b_sec.get("content"))
            if a_text == b_text:
                status = "unchanged"
                summary[status] += 1
                diff_ops = []
            else:
                status = "modified"
                summary[status] += 1
                diff_ops = diff_text(a_text, b_text)
            pairs.append({
                "key": k,
                "status": status,
                "a": {
                    "version": "2015",
                    "id": a_sec.get("id"),
                    "anchor": a_sec.get("anchor"),
                    "title": a_sec.get("title"),
                },
                "b": {
                    "version": "2025",
                    "id": b_sec.get("id"),
                    "anchor": b_sec.get("anchor"),
                    "title": b_sec.get("title"),
                },
                "diff": diff_ops,
            })

    out = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "pairs": pairs,
        "summary": summary,
    }
    os.makedirs(os.path.dirname(OUT_DIFF), exist_ok=True)
    with open(OUT_DIFF, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUT_DIFF}")


if __name__ == "__main__":
    sys.exit(main())

