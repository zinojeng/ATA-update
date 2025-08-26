# AGENTS.md

Purpose: orchestrate agents to build an interactive site that compares the 2015 and 2025 ATA thyroid nodule and cancer guidelines, using structured content extracted from the two PDFs and exposing rich navigation, search, and export features.

## Source Documents
- `2025 ATA thyroid nodule and cancer.pdf` (~4.3 MB)
- `2015 ATA thyroid nodule and cancer.pdf` (~1.6 MB)

Do not commit or redistribute copyrighted content beyond what the project license allows. Prefer storing derived, structured data (JSON) and only the minimal excerpts needed for comparison and fair-use quotations in exports.

## High-Level Pipeline
1) Ingest PDFs → extract text + layout signal
2) Normalize + segment into canonical sections
3) Build TOC and anchors
4) Compute 2015↔2025 diffs (section and line level)
5) Index for search (both years + merged)
6) Render UI (comparison modes, navigation, highlights)
7) Export reports (PDF/print/share URLs/citations)

## Roles and Responsibilities

### 1) Ingestion Agent
- Goal: convert the PDFs into structured text with page numbers and basic layout cues (headings, paragraphs, lists, tables, references).
- Inputs: two PDFs listed above.
- Outputs:
  - `data/json/2015.raw.json`
  - `data/json/2025.raw.json`
- Requirements:
  - Preserve reading order per page.
  - Detect headings (H1–H6) and capture page spans.
  - Detect lists (ordered/unordered) and tables where feasible.
  - Retain reference markers and figure/table captions as content blocks.

### 2) Structuring Agent
- Goal: transform raw extraction into a canonical document schema with stable section IDs and anchors.
- Inputs: `*.raw.json`
- Outputs:
  - `data/json/2015.json`
  - `data/json/2025.json`
  - `data/toc/2015.toc.json`
  - `data/toc/2025.toc.json`
- Canonical Section Schema (per section):
  ```json
  {
    "id": "<stable-id>",
    "path": "<hierarchy like 1.2.3 or R34>",
    "title": "<section title>",
    "level": 1,
    "anchor": "<kebab-case-title-or-path>",
    "page_start": 12,
    "page_end": 15,
    "content": [
      {"type": "p", "text": "..."},
      {"type": "list", "ordered": false, "items": ["...", "..."]},
      {"type": "table", "rows": [["..."],["..."]]},
      {"type": "ref", "text": "[12] ..."}
    ],
    "tags": ["diagnosis", "risk"],
    "references": ["...optional normalized refs..."]
  }
  ```
- Document Meta Schema:
  ```json
  {
    "version": "2015",
    "title": "ATA Thyroid Nodule and Cancer Guidelines",
    "source_file": "2015 ATA thyroid nodule and cancer.pdf",
    "generated_at": "<ISO8601>",
    "sections": [ /* Section objects */ ]
  }
  ```
- Conventions:
  - `id`: hash of `version + path + title` for stability.
  - `anchor`: slugified `path + title` for deep-linking.
  - Normalize whitespace, bullets, and em-dashes; unify numeric/bullet lists.

### 3) Diff Agent
- Goal: compute changes between 2015 and 2025 at two granularities:
  1) Section-level presence/matching
  2) Line/block-level text diffs within matched sections
- Inputs: `data/json/{2015.json,2025.json}`
- Output: `data/diff/diff.json`
- Change Types and Legend (UI colors):
  - New (2025-only): green (🟢 `#22c55e`)
  - Modified (both, with textual change): yellow (🟡 `#eab308`)
  - Removed (2015-only): red (🔴 `#ef4444`)
  - Unchanged (semantically equal): gray (⚪ `#9ca3af`)
- Diff Record Schema (per matched logical node):
  ```json
  {
    "key": "<path-or-title-key>",
    "status": "new|modified|removed|unchanged",
    "a": {"version": "2015", "id": "...", "anchor": "...", "title": "...", "content": [/* blocks */]},
    "b": {"version": "2025", "id": "...", "anchor": "...", "title": "...", "content": [/* blocks */]},
    "diff": [
      {"type": "equal|insert|delete|replace", "text": "...", "a_range": [start,end], "b_range": [start,end]}
    ]
  }
  ```
- Matching Heuristics:
  - Primary: normalized section path + title equality.
  - Secondary: fuzzy title similarity (≥0.85) and parent path consistency.
  - Tertiary: content similarity (token Jaccard ≥0.70) if titles changed.
  - Handle reordering: allow non-positional matches guided by IDs.
  - Consider sections with split/merge: record `relations: {split_from:[], merged_from:[]}` when detected.

### 4) Search Agent
- Goal: full-text search across both guidelines with filters and quick jumps.
- Inputs: `data/json/{2015.json,2025.json}`
- Outputs:
  - `data/search/2015.index.json`
  - `data/search/2025.index.json`
  - `data/search/merged.index.json` (optional)
- Index Fields:
  - `title` (boost x3)
  - `path` (boost x2)
  - `content` (paragraph text, lists)
  - `tags`
- Result Payload (per hit): `{version, id, anchor, title, path, snippet, score}`
- Features to support:
  - Full-text search with highlight snippets
  - Filter by section/topic (via `path` or `tags`)
  - Quick jump to sections (anchors)
  - Persist search history (local storage)

### 5) Navigation Agent
- Goal: generate a collapsible table of contents, breadcrumbs, bookmarks, and a quick access toolbar.
- Inputs: `data/json/*.json`
- Outputs: `data/toc/*.toc.json` and anchor map `data/toc/anchors.json`
- TOC Node Schema: `{title, path, anchor, level, children:[]}`
- Breadcrumbs: derive from `path` hierarchy.
- Bookmarks: client-side list of `{version, id, anchor, title, added_at}`.

### 6) UI Agent
- Goal: implement the website features.
- Comparison Modes:
  - Overview Mode: summary cards by section with counts of New/Modified/Removed.
  - Detailed Mode: side-by-side, line-by-line diffs with highlights.
  - Change-only Mode: filter view to exclude Unchanged blocks.
  - Version Toggle: quick swap between 2015-only and 2025-only views.
- Highlights: map change types to CSS classes
  - `.chg-new { background: #ecfdf5; border-left: 3px solid #22c55e; }`
  - `.chg-mod { background: #fffbeb; border-left: 3px solid #eab308; }`
  - `.chg-rem { background: #fef2f2; border-left: 3px solid #ef4444; }`
  - `.chg-same { background: #f3f4f6; border-left: 3px solid #9ca3af; }`
- Navigation:
  - Collapsible TOC sidebar + breadcrumb header.
  - Section bookmarks (persisted locally).
  - Quick access toolbar: search, mode toggle, copy link, export.
- Accessibility/UX:
  - Keyboard navigation for next/prev change.
  - High-contrast mode and color legend.
  - Preserve scroll position per pane.

### 7) Export Agent
- Goal: export comparison artifacts and shareable links.
- Outputs:
  - PDF report of diffs per selected scope: `export/report-<scope>.pdf`
  - Print-friendly HTML route (CSS print styles)
  - Share URLs with query params and hash anchors
  - Copyable citations
- Citation format (example):
  - "American Thyroid Association. (2025). Management guidelines for adult patients with thyroid nodules and differentiated thyroid cancer. Retrieved from <app-url>#/compare?path=<...>"

### 8) QA Agent
- Goal: validate data quality, UI correctness, and feature completeness.
- Checks:
  - Section counts across 2015 vs 2025; no missing roots.
  - Random sample of sections: anchors deep-link correctly.
  - Diff sanity: unchanged sections show zero edits; removed/new correctly classified.
  - Search returns expected hits; filters work.
  - Performance: initial payload < 2.5 MB compressed; route transitions < 200ms on mid hardware.
  - Accessibility: keyboard focus order and ARIA labels on diff panes.

### 9) Ops Agent
- Goal: maintain project structure, scripts, and deployment.
- Suggested filesystem layout:
  - `data/raw/` – original PDFs (if stored locally)
  - `data/json/` – canonical JSON (`2015.json`, `2025.json`)
  - `data/toc/` – generated TOC/anchor maps
  - `data/diff/` – `diff.json`
  - `data/search/` – search indices
  - `export/` – generated reports
  - `src/` – frontend app (components, routes, styles)
  - `public/` – static assets

## Website Features (to implement)
- Side-by-side View: show 2015 and 2025 concurrently
- Highlight Changes: color-coded legend
  - 🟢 Green: New in 2025
  - 🟡 Yellow: Modified recommendations
  - 🔴 Red: Removed/deprecated
  - ⚪ Gray: Unchanged
- Search: full-text across both, filters, quick jump, history
- Navigation: collapsible TOC, breadcrumbs, bookmarks, quick toolbar
- Comparison Modes: overview, detailed, change-only, version toggle
- Export: PDF reports, print-friendly, share URLs, copy citations

## Data and Diff Contracts
- `data/json/<year>.json` must follow the canonical schema above.
- `data/diff/diff.json` must only include serializable primitives and arrays.
- All anchors must be unique per version and resolvable via `#/compare?version=<year>&anchor=<anchor>`.

## URL and State Model
- Route: `#/compare`
- Query params:
  - `mode=overview|detailed|changes`
  - `left=2015&right=2025` (or toggle)
  - `anchor=<section-anchor>`
  - `q=<search-term>` and `filters=<csv>`
- Hash fragments map to section anchors for deep links.

## Implementation Notes
- Normalization:
  - Trim whitespace, unify list markers, preserve paragraph boundaries.
  - Normalize quotes/dashes; remove page headers/footers if repeated.
- Matching stability:
  - Prefer path-based keys; fall back to title + similarity.
  - Record split/merge relations when pathing changes across editions.
- Performance:
  - Lazy-load heavy sections; virtualize long lists of diffs.
  - Precompute diff summaries for overview mode.

## Acceptance Criteria
- Data:
  - Canonical JSON produced for both years; TOC present; no duplicate anchors.
  - Diff file classifies sections into New/Modified/Removed/Unchanged with <2% sampling error on manual spot-checks.
- UI:
  - All comparison modes available and stable.
  - Color-coding matches legend consistently.
  - Search finds expected sections and supports filters and history.
  - Navigation (TOC, breadcrumbs, bookmarks) functions and persists bookmarks locally.
  - Export produces readable reports and shareable links restore exact state.

## Non-Goals
- Medical interpretation of guideline content.
- Replicating page-perfect PDF layouts; focus on semantic structure.
- Building server-side search unless explicitly required; prefer client-side indices.

## Getting Started (suggested)
1) Place PDFs in `data/raw/` (or reference existing files in the repo root).
2) Build `*.raw.json` via your preferred PDF extraction (ensure headings/lists captured).
3) Transform to canonical `data/json/<year>.json` and generate TOC.
4) Run Diff Agent to emit `data/diff/diff.json` and overview summaries.
5) Generate search indices.
6) Implement UI routes and components using the contracts above.
7) Validate with QA checklist and iterate.

