"""
純文字檔案解析器
支援 .txt, .md, .csv 等純文字格式
"""

import os
from typing import Dict, Any, List
from .base_parser import BaseParser, ParsedDocument, ParsedContent
import csv
import re

# Try to import chardet, use fallback if not available
try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False


class TextParser(BaseParser):
    """純文字檔案解析器"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ['.txt', '.md', '.csv', '.log']
        
    def parse(self, file_path: str) -> ParsedDocument:
        """解析純文字檔案"""
        if not self.validate_file(file_path):
            raise ValueError(f"Unsupported file format: {file_path}")
        
        # 偵測檔案編碼
        encoding = self._detect_encoding(file_path)
        
        # 讀取檔案內容
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        
        # 提取元數據
        metadata = self.extract_metadata(file_path)
        
        # 根據檔案類型進行不同的解析
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.csv':
            contents = self._parse_csv(file_path, encoding)
        elif file_ext == '.md':
            contents = self._parse_markdown(content)
        else:
            contents = self._parse_plain_text(content)
        
        # 建立解析後的文件物件
        parsed_doc = ParsedDocument(
            filename=os.path.basename(file_path),
            file_type='text',
            contents=contents,
            metadata=metadata,
            summary=self._generate_summary(content),
            key_points=self._extract_key_points(content),
            entities=self._extract_entities(content)
        )
        
        return parsed_doc
    
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """提取檔案元數據"""
        stat = os.stat(file_path)
        return {
            'file_size': stat.st_size,
            'created_time': stat.st_ctime,
            'modified_time': stat.st_mtime,
            'file_path': file_path,
            'encoding': self._detect_encoding(file_path)
        }
    
    def _detect_encoding(self, file_path: str) -> str:
        """偵測檔案編碼"""
        if HAS_CHARDET:
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read(10000))
            return result['encoding'] or 'utf-8'
        else:
            # Fallback: try common encodings
            encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'iso-8859-1']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        f.read(1000)  # Try reading a small portion
                    return encoding
                except UnicodeDecodeError:
                    continue
            return 'utf-8'  # Default fallback
    
    def _parse_plain_text(self, content: str) -> List[ParsedContent]:
        """解析純文字內容"""
        contents = []
        
        # 按段落分割
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        for i, paragraph in enumerate(paragraphs):
            # 提取關鍵元素
            key_elements = self.extract_key_elements(paragraph)
            
            parsed_content = ParsedContent(
                content_type='paragraph',
                raw_content=paragraph,
                structured_data={
                    'text': paragraph,
                    'word_count': len(paragraph.split()),
                    'char_count': len(paragraph),
                    'key_elements': key_elements
                },
                metadata={
                    'paragraph_index': i,
                    'position': 'body'
                }
            )
            contents.append(parsed_content)
        
        return contents
    
    def _parse_markdown(self, content: str) -> List[ParsedContent]:
        """解析 Markdown 格式內容"""
        contents = []
        lines = content.split('\n')
        
        current_section = []
        section_level = 0
        
        for line in lines:
            # 檢查是否為標題
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                # 保存前一個段落
                if current_section:
                    contents.append(self._create_markdown_content(current_section, 'paragraph'))
                    current_section = []
                
                # 添加標題
                level = len(heading_match.group(1))
                heading_text = heading_match.group(2)
                contents.append(ParsedContent(
                    content_type='heading',
                    raw_content=line,
                    structured_data={
                        'text': heading_text,
                        'level': level
                    },
                    metadata={'position': 'heading'}
                ))
                section_level = level
            
            # 檢查是否為列表
            elif re.match(r'^[\*\-\+]\s+', line) or re.match(r'^\d+\.\s+', line):
                current_section.append(line)
            
            # 檢查是否為程式碼區塊
            elif line.strip().startswith('```'):
                if current_section:
                    contents.append(self._create_markdown_content(current_section, 'paragraph'))
                    current_section = []
                # 處理程式碼區塊
                current_section.append(line)
            
            else:
                current_section.append(line)
        
        # 保存最後一個段落
        if current_section:
            contents.append(self._create_markdown_content(current_section, 'paragraph'))
        
        return contents
    
    def _create_markdown_content(self, lines: List[str], content_type: str) -> ParsedContent:
        """建立 Markdown 內容物件"""
        text = '\n'.join(lines).strip()
        return ParsedContent(
            content_type=content_type,
            raw_content=text,
            structured_data={
                'text': text,
                'word_count': len(text.split()),
                'key_elements': self.extract_key_elements(text)
            },
            metadata={'format': 'markdown'}
        )
    
    def _parse_csv(self, file_path: str, encoding: str) -> List[ParsedContent]:
        """解析 CSV 檔案"""
        contents = []
        
        with open(file_path, 'r', encoding=encoding) as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            # 添加表格標題
            contents.append(ParsedContent(
                content_type='table_header',
                raw_content=headers,
                structured_data={
                    'headers': headers,
                    'column_count': len(headers)
                },
                metadata={'table_type': 'csv'}
            ))
            
            # 讀取數據行
            rows = list(reader)
            contents.append(ParsedContent(
                content_type='table_data',
                raw_content=rows,
                structured_data={
                    'rows': rows,
                    'row_count': len(rows),
                    'statistics': self._calculate_csv_statistics(rows, headers)
                },
                metadata={'table_type': 'csv'}
            ))
        
        return contents
    
    def _calculate_csv_statistics(self, rows: List[Dict], headers: List[str]) -> Dict[str, Any]:
        """計算 CSV 數據統計資訊"""
        stats = {}
        
        for header in headers:
            values = [row.get(header, '') for row in rows]
            
            # 嘗試將值轉換為數字
            numeric_values = []
            for value in values:
                try:
                    numeric_values.append(float(value))
                except ValueError:
                    pass
            
            if numeric_values:
                stats[header] = {
                    'min': min(numeric_values),
                    'max': max(numeric_values),
                    'avg': sum(numeric_values) / len(numeric_values),
                    'count': len(numeric_values)
                }
        
        return stats
    
    def _generate_summary(self, content: str) -> str:
        """生成內容摘要"""
        # 簡單的摘要生成：取前 200 個字
        words = content.split()[:200]
        summary = ' '.join(words)
        if len(content.split()) > 200:
            summary += '...'
        return summary
    
    def _extract_key_points(self, content: str) -> List[str]:
        """提取關鍵要點"""
        key_points = []
        
        # 尋找包含數字的句子（可能是重要數據）
        sentences = content.split('.')
        for sentence in sentences:
            if any(char.isdigit() for char in sentence):
                key_points.append(sentence.strip())
        
        return key_points[:5]  # 只返回前5個要點
    
    def _extract_entities(self, content: str) -> Dict[str, List[str]]:
        """提取命名實體"""
        entities = {
            'dates': [],
            'numbers': [],
            'keywords': []
        }
        
        # 提取日期（簡單模式）
        date_patterns = [
            r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b',
            r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b'
        ]
        
        for pattern in date_patterns:
            dates = re.findall(pattern, content, re.IGNORECASE)
            entities['dates'].extend(dates)
        
        # 提取重要數字
        numbers = re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', content)
        entities['numbers'] = numbers[:10]  # 只保留前10個數字
        
        # 提取可能的關鍵詞（首字母大寫的詞組）
        keywords = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', content)
        entities['keywords'] = list(set(keywords))[:20]  # 去重並只保留前20個
        
        return entities