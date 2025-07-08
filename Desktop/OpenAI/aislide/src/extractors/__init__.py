# Extractors module for AI Slides
"""
內容提取模組：負責從解析後的內容中提取關鍵資訊
包含實體識別、關係提取、重點摘要等功能
"""

from .key_element_extractor import KeyElementExtractor
from .semantic_extractor import SemanticExtractor

__all__ = ['KeyElementExtractor', 'SemanticExtractor']