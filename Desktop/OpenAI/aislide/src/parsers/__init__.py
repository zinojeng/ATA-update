# Parsers module for AI Slides
"""
文件解析模組：負責解析不同格式的輸入檔案
支援格式：PDF, Word, Excel, PowerPoint, 純文字, 圖片等
"""

from .base_parser import BaseParser
from .text_parser import TextParser

__all__ = ['BaseParser', 'TextParser']