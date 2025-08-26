Scripts overview

- init_scaffold.py: Creates the folder structure and placeholder JSON/TOC/diff files per AGENTS.md contracts. Run before implementing extraction/structuring.

Usage

1) Ensure you are at the repo root.
2) Run: `python3 scripts/init_scaffold.py`
3) You should see:
   - data/json/2015.json and 2025.json (skeletons)
   - data/toc/2015.toc.json and 2025.toc.json (placeholders)
   - data/diff/diff.json (placeholder)

Next steps

- Implement an extraction step to create `data/json/<year>.raw.json` from the PDFs.
- Implement a structuring step to convert raw → canonical schema defined in AGENTS.md.
- Implement a diff step to emit `data/diff/diff.json` and summaries.
- Generate search indices into `data/search/`.

