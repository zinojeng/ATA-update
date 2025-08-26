"""
基礎解析器類別
定義所有解析器的共同介面和基本功能
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ParsedContent:
    """解析後的內容結構"""
    content_type: str  # 內容類型（text, table, image, chart等）
    raw_content: Any  # 原始內容
    structured_data: Dict[str, Any]  # 結構化數據
    metadata: Dict[str, Any]  # 元數據（來源、頁數、位置等）
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ParsedDocument:
    """解析後的完整文件"""
    filename: str
    file_type: str
    contents: List[ParsedContent]
    metadata: Dict[str, Any]
    summary: Optional[str] = None
    key_points: Optional[List[str]] = None
    entities: Optional[Dict[str, List[str]]] = None  # 實體識別結果


class BaseParser(ABC):
    """所有解析器的基礎類別"""
    
    def __init__(self):
        self.supported_formats = []
        
    @abstractmethod
    def parse(self, file_path: str) -> ParsedDocument:
        """
        解析檔案並返回結構化內容
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            ParsedDocument: 解析後的文件物件
        """
        pass
    
    @abstractmethod
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        提取檔案元數據
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            Dict: 包含檔案元數據的字典
        """
        pass
    
    def validate_file(self, file_path: str) -> bool:
        """
        驗證檔案是否可以被解析
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            bool: 是否可以解析
        """
        import os
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        return file_extension in self.supported_formats
    
    def extract_key_elements(self, content: str) -> Dict[str, Any]:
        """
        提取關鍵元素（如數字、日期、專有名詞等）
        
        Args:
            content: 文本內容
            
        Returns:
            Dict: 包含各類關鍵元素的字典
        """
        import re
        
        elements = {
            'numbers': [],
            'dates': [],
            'percentages': [],
            'currencies': [],
            'emails': [],
            'urls': []
        }
        
        # 提取數字
        numbers = re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', content)
        elements['numbers'] = numbers
        
        # 提取百分比
        percentages = re.findall(r'\b\d+(?:\.\d+)?%\b', content)
        elements['percentages'] = percentages
        
        # 提取貨幣金額
        currencies = re.findall(r'[$¥€£]\s*\d+(?:,\d{3})*(?:\.\d+)?', content)
        elements['currencies'] = currencies
        
        # 提取電子郵件
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        elements['emails'] = emails
        
        # 提取網址
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        elements['urls'] = urls
        
        return elements