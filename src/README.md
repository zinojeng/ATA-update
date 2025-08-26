UI plan (summary)

- Routes: `#/compare` with params `mode`, `left`, `right`, `anchor`, `q`.
- Views: Overview, Detailed, Change-only, Version-only toggle.
- Components: TOC sidebar, Breadcrumbs, DiffPane(L/R), SearchBox, Legend, Toolbar, BookmarkList.
- Data loading: read `data/json/*.json` + `data/diff/diff.json` + `data/toc/*.toc.json`.
- Accessibility: keyboard navigation for next/prev change; ARIA labels; high-contrast support.

