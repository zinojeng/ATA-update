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

## Governance & Compliance
- Content usage: 僅以結構化資料與必要片段（fair use）呈現，不批量再散佈完整原文。
- PII/敏感資訊: 不預期存在；若抽取到個資，需在 structuring 階段移除或匿名化。
- 版控策略: 原始 PDF 不必進 git；建議存放於 `data/raw/` 並在 .gitignore 排除。
- 版權標示: 匯出與引用時附上來源與年份，避免誤導醫療建議。

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

- Classification Policy (edge cases):
  - Text-only rewording → Modified（若語義近似但字詞變動，仍標示 Modified）。
  - 位置變更（重排）但內容相同 → Unchanged（關聯由 ID 或相似度維持）。
  - 表格欄位調整/新增刪除 → Modified；若整段表格被移除 → Removed。
  - 大幅拆分/合併 → Modified 並在 `relations` 記錄來源或目標。

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

- Ranking/Tokenization（建議）:
  - Tokenize: 空白/標點分詞 + 小寫正規化；可考慮 bigram 提升中文/英文混合。
  - Field boosts: title×3, path×2, content×1, tags×2。
  - Snippet: 就近擷取 1–2 行命中區段，並以 <mark> 包裹高亮（前端）。

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
  - ARIA: 為主要容器與互動元件加上適當 `role` 與 `aria-*`。

### 7) Export Agent
- Goal: export comparison artifacts and shareable links.
- Outputs:
  - PDF report of diffs per selected scope: `export/report-<scope>.pdf`
  - Print-friendly HTML route (CSS print styles)
  - Share URLs with query params and hash anchors
  - Copyable citations
- Citation format (example):
  - "American Thyroid Association. (2025). Management guidelines for adult patients with thyroid nodules and differentiated thyroid cancer. Retrieved from <app-url>#/compare?path=<...>"

- Print/PDF（建議）:
  - 採用 print 專用 CSS 隱藏互動元素，保留標題、變更標示、頁眉頁腳與引用。
  - 大型附錄與表格允許分頁斷行，避免內容截斷。

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

### Anchors & IDs
- Stability: `id` 基於 `version+path+title` 派生（或額外引入作者定義 ID 以橫跨版本穩定）。
- Collision: 若 slug 重複（同名節點），在 anchor 後附加短雜湊 `-<hash6>`。
- Redirects: 如節點重命名，保留 `redirect_from:[]` 以維護舊連結。

## URL and State Model
- Route: `#/compare`
- Query params:
  - `mode=overview|detailed|changes`
  - `left=2015&right=2025` (or toggle)
  - `anchor=<section-anchor>`
  - `q=<search-term>` and `filters=<csv>`
- Hash fragments map to section anchors for deep links.

### Share URL Examples
- `#/compare?mode=detailed&left=2015&right=2025&anchor=1-1-recommendation-a-initial-evaluation`
- `#/compare?mode=overview`

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

### Error Handling & Logging
- Extraction: 逐頁記錄解析錯誤（頁碼、原因、信心分數）。
- Structuring: 回報未匹配標題層級或缺失頁碼範圍的節點。
- Diff: 產出未匹配清單與對應嘗試策略（title 相似度、內容相似度）。
- 前端：在 UI 顯示可理解的錯誤訊息並允許重試載入。

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

### KPIs & Sampling
- 抽樣 50 個節點驗證 Diff 類型準確率 ≥ 95%。
- 搜尋前 10 名結果命中率：基準查詢集平均 NDCG@10 ≥ 0.8。
- 首屏載入（壓縮後）≤ 2.5 MB；互動延遲 < 200ms（中階硬體）。

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

## Versioning & Releases
- Artifacts: `data/json/*`, `data/diff/diff.json`, `data/search/*.json` 使用資料版號（例如 `vYYYY.MM.DD`）於 release asset 或檔名尾碼。
- UI: 使用 semver；標註相容之資料版（compat matrix）。
- Changelog: 針對資料與 UI 分開維護，列出破壞性變更與遷移步驟。

## Contribution Workflow
- Branch: feature 分支開發 → PR → Review（資料與前端可分開 reviewer）。
- Checks: CI 驗證 schema（JSON Schema）、lint、基本單元測試、體積門檻。
- Code owners: 指派資料管線與前端維護者。

## Risks & Mitigations
- PDF 抽取品質不一：使用雙引擎比對或引入版面/字體線索，人工抽樣校正。
- 標題規則變動：引入可組態標題檢測與路徑對映表（mapping）。
- 大檔載入與性能：使用分頁載入與虛擬清單，摘要預先計算。
- 語義變動難以量化：先以字面差異為主，逐步加入術語字典與相似度語義模型。

## Glossary
- TOC: 目錄樹狀結構。
- Anchor: 前端深連結定位點（slug）。
- Diff Pair: 一對 2015/2025 對應節點之差異紀錄。
- Overview/Detailed/Change-only: 三種比較與顯示模式。
