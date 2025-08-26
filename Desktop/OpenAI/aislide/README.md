# AI Slides - 智慧簡報生成系統

基於多重 AI Agents 協作的智慧簡報生成系統，能夠自動將各種格式的原始資料轉換為專業簡報。

## 系統架構

AI Slides 採用五步驟流程：

```
解析 → 映射 → 適配 → 協作 → 整合
```

### Step 1: 資料解析與語義分層（已實現）

- **檔案解析**：支援純文字、Markdown、CSV 等格式
- **關鍵元素提取**：自動識別財務指標、KPI、戰術術語等
- **語義分層**：將內容分解為核心論點、支持證據和參考資料
- **資訊壓縮**：過濾重複和低質量內容

## 快速開始

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 執行 Step 1

```bash
python main.py <輸入檔案路徑>
```

範例：
```bash
python main.py Examples/sample.txt
```

## 專案結構

```
aislide/
├── src/
│   ├── parsers/          # 檔案解析器
│   │   ├── base_parser.py
│   │   └── text_parser.py
│   ├── extractors/       # 內容提取器
│   │   ├── key_element_extractor.py
│   │   └── semantic_extractor.py
│   └── agents/          # AI Agents（待實現）
├── Examples/            # 範例檔案
├── main.py             # 主程式入口
├── CLAUDE.md           # 詳細技術文件
└── requirements.txt    # 專案依賴
```

## 功能特點

### 已實現功能

1. **多格式檔案解析**
   - 純文字（.txt）
   - Markdown（.md）
   - CSV 表格

2. **智慧內容提取**
   - 財務指標識別
   - KPI 指標提取
   - 時間參考提取
   - 實體關係識別

3. **語義結構分析**
   - 核心論點提取
   - 支持證據識別
   - 參考資料整理
   - 自動摘要生成

4. **資訊壓縮優化**
   - 重複內容過濾
   - 低質量內容排除
   - 關鍵句子提取

### 待實現功能

- Step 2: 視覺元素映射
- Step 3: 風格適配與排版
- Step 4: 跨模型協作優化
- Step 5: 互動元素整合

## 輸出格式

Step 1 的輸出為 JSON 格式，包含：

```json
{
  "timestamp": "處理時間",
  "file_info": {
    "filename": "檔案名稱",
    "file_type": "檔案類型",
    "metadata": {}
  },
  "parsed_content": {
    "content_blocks": "內容區塊數",
    "summary": "摘要",
    "key_points": ["關鍵要點"],
    "entities": {}
  },
  "key_elements": {
    "financial_indicators": "財務指標數",
    "kpi_metrics": "KPI 指標數"
  },
  "semantic_structure": {
    "type": "結構類型",
    "core_arguments": ["核心論點"],
    "summary": "結構化摘要"
  },
  "compression": {
    "compression_ratio": "壓縮率",
    "key_sentences": ["關鍵句子"]
  }
}
```

## 技術細節

詳細的技術架構和實作說明請參考 [CLAUDE.md](CLAUDE.md)

## 貢獻指南

歡迎提交 Issue 和 Pull Request！

## 授權

MIT License