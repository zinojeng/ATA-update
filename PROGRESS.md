# PROGRESS.md

專案進度、操作指引與後續 TODO（更新頻率：里程碑後）

## 摘要
- 目的：提供 2015 與 2025 ATA 指南的互動比較網站（搜尋、導航、匯出）。
- 目前：已完成資料骨架、示例 sections、初步 Diff/Search、前端靜態頁（Overview/Detailed/Change-only）。

## 里程碑與狀態
- 初始化腳手架：完成
- 示範資料與 Diff/Search：完成
- 靜態前端頁（/public）：完成
- 推送至 GitHub：完成（main）
- 進階 Diff 規則（相似度、split/merge）：待辦
- TOC/麵包屑/書籤：待辦
- 搜尋前端整合與高亮：待辦
- 匯出（PDF/列印/分享 URL）：待辦

## 目前產物
- 結構化資料（示例）
  - `data/json/2015.json`, `data/json/2025.json`
- 差異紀錄
  - `data/diff/diff.json`（含 New/Modified/Removed/Unchanged）
- 搜尋索引
  - `data/search/{2015.index.json,2025.index.json,merged.index.json}`
- 前端靜態頁
  - `public/{index.html,styles.css,app.js}`
- 設計說明
  - `AGENTS.md`

## 本地執行
- 產生骨架與初步輸出
  - `python3 scripts/init_scaffold.py`
  - `python3 scripts/generate_diff.py`
  - `python3 scripts/generate_search.py`
- 啟動簡易伺服器（專案根目錄）
  - `python3 -m http.server 8000`
  - 瀏覽：`http://localhost:8000/public/`

## 待辦（短期）
- Diff 強化
  - [ ] 標題相似度（≥0.85）與內容相似度（Jaccard ≥0.7）
  - [ ] split/merge 關係寫入 `relations`
  - [ ] 表格/清單差異判定與摘要
- 前端導航
  - [ ] TOC 側欄與麵包屑
  - [ ] 書籤（localStorage）
- 搜尋整合
  - [ ] 連動 `data/search/*.index.json`
  - [ ] 顯示 highlight snippet 與快速跳轉
- 匯出能力
  - [ ] 列印樣式與 PDF 匯出
  - [ ] 分享 URL（保留 mode/view/filter/anchor 狀態）

## 驗收與 KPI（節錄）
- Diff 準確率（抽樣 50 節點）≥ 95%
- 搜尋 NDCG@10 ≥ 0.8（基準查詢集）
- 首屏載入 ≤ 2.5 MB（壓縮），互動延遲 < 200ms

## 風險與對策
- PDF 抽取品質差異 → 允許人工對照表與 fallback 規則；抽樣校正
- 大檔載入 → 虛擬清單、延遲載入；預先計算摘要
- 章節命名變動 → 對映表與相似度匹配，保留 redirect 設定

## 變更日誌（最近）
- 添加示例 sections，產生可視 Diff/Search
- 新增前端頁（Overview/Detailed/Change-only）與色碼 legend
- 擴充 AGENTS.md（治理、比對政策、錨點穩定、排名與 KPI）

