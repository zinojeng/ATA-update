"""
關鍵元素提取器
負責從文本中提取財務指標、KPI、戰術術語等關鍵元素
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class KeyElement:
    """關鍵元素資料結構"""
    element_type: str  # 元素類型
    value: Any  # 元素值
    context: str  # 上下文
    confidence: float  # 置信度
    position: int  # 在原文中的位置


class KeyElementExtractor:
    """關鍵元素提取器"""
    
    def __init__(self):
        # 定義財務指標關鍵詞
        self.financial_keywords = [
            'revenue', 'profit', 'loss', 'margin', 'ROI', 'ROE', 'ROA',
            'earnings', 'EBITDA', 'cash flow', 'debt', 'asset', 'liability',
            '營收', '利潤', '毛利', '淨利', '資產', '負債', '現金流'
        ]
        
        # 定義 KPI 相關關鍵詞
        self.kpi_keywords = [
            'KPI', 'metric', 'performance', 'target', 'goal', 'objective',
            'conversion', 'retention', 'acquisition', 'engagement',
            '指標', '目標', '績效', '轉換率', '留存率', '達成率'
        ]
        
        # 定義戰術術語（可擴展）
        self.tactical_terms = [
            'strategy', 'tactic', 'approach', 'method', 'framework',
            'analysis', 'implementation', 'optimization',
            '策略', '戰術', '方法', '框架', '分析', '實施', '優化'
        ]
    
    def extract(self, text: str) -> Dict[str, List[KeyElement]]:
        """
        提取所有關鍵元素
        
        Args:
            text: 輸入文本
            
        Returns:
            Dict: 按類型分組的關鍵元素
        """
        elements = {
            'financial_indicators': self._extract_financial_indicators(text),
            'kpi_metrics': self._extract_kpi_metrics(text),
            'tactical_terms': self._extract_tactical_terms(text),
            'data_points': self._extract_data_points(text),
            'time_references': self._extract_time_references(text)
        }
        
        return elements
    
    def _extract_financial_indicators(self, text: str) -> List[KeyElement]:
        """提取財務指標"""
        indicators = []
        
        # 尋找包含財務關鍵詞的句子
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            
            for keyword in self.financial_keywords:
                if keyword.lower() in sentence_lower:
                    # 提取相關數值
                    numbers = self._extract_numbers_with_context(sentence)
                    
                    for number, context in numbers:
                        element = KeyElement(
                            element_type='financial_indicator',
                            value={
                                'keyword': keyword,
                                'number': number,
                                'unit': self._detect_unit(context)
                            },
                            context=sentence,
                            confidence=0.8,
                            position=i
                        )
                        indicators.append(element)
        
        return indicators
    
    def _extract_kpi_metrics(self, text: str) -> List[KeyElement]:
        """提取 KPI 指標"""
        metrics = []
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            
            # 檢查是否包含 KPI 關鍵詞
            for keyword in self.kpi_keywords:
                if keyword.lower() in sentence_lower:
                    # 提取百分比
                    percentages = re.findall(r'(\d+(?:\.\d+)?)\s*%', sentence)
                    
                    for percentage in percentages:
                        element = KeyElement(
                            element_type='kpi_metric',
                            value={
                                'keyword': keyword,
                                'percentage': float(percentage),
                                'metric_type': self._classify_metric_type(sentence)
                            },
                            context=sentence,
                            confidence=0.75,
                            position=i
                        )
                        metrics.append(element)
                    
                    # 提取其他數值指標
                    numbers = self._extract_numbers_with_context(sentence)
                    for number, context in numbers:
                        if '%' not in context:  # 避免重複提取百分比
                            element = KeyElement(
                                element_type='kpi_metric',
                                value={
                                    'keyword': keyword,
                                    'value': number,
                                    'metric_type': self._classify_metric_type(sentence)
                                },
                                context=sentence,
                                confidence=0.7,
                                position=i
                            )
                            metrics.append(element)
        
        return metrics
    
    def _extract_tactical_terms(self, text: str) -> List[KeyElement]:
        """提取戰術術語"""
        terms = []
        sentences = self._split_sentences(text)
        
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            
            for term in self.tactical_terms:
                if term.lower() in sentence_lower:
                    # 提取術語周圍的上下文
                    context_words = self._get_context_words(sentence, term)
                    
                    element = KeyElement(
                        element_type='tactical_term',
                        value={
                            'term': term,
                            'context_words': context_words,
                            'category': self._classify_tactical_category(term)
                        },
                        context=sentence,
                        confidence=0.85,
                        position=i
                    )
                    terms.append(element)
        
        return terms
    
    def _extract_data_points(self, text: str) -> List[KeyElement]:
        """提取數據點"""
        data_points = []
        
        # 提取所有數字及其上下文
        pattern = r'([\w\s]+?)\s*[:：]\s*([0-9,]+(?:\.[0-9]+)?)\s*([^0-9\s]+)?'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            label = match.group(1).strip()
            value = match.group(2).replace(',', '')
            unit = match.group(3).strip() if match.group(3) else ''
            
            element = KeyElement(
                element_type='data_point',
                value={
                    'label': label,
                    'value': float(value) if '.' in value else int(value),
                    'unit': unit
                },
                context=match.group(0),
                confidence=0.9,
                position=match.start()
            )
            data_points.append(element)
        
        return data_points
    
    def _extract_time_references(self, text: str) -> List[KeyElement]:
        """提取時間參考"""
        time_refs = []
        
        # 年份模式
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.finditer(year_pattern, text)
        
        for match in years:
            year = match.group(0)
            context = self._get_surrounding_text(text, match.start(), match.end())
            
            element = KeyElement(
                element_type='time_reference',
                value={
                    'type': 'year',
                    'value': int(year),
                    'context_type': self._classify_time_context(context)
                },
                context=context,
                confidence=0.95,
                position=match.start()
            )
            time_refs.append(element)
        
        # 季度模式
        quarter_pattern = r'Q[1-4]\s*(?:20)?\d{2}|(?:第)?[一二三四1-4]\s*季(?:度)?'
        quarters = re.finditer(quarter_pattern, text, re.IGNORECASE)
        
        for match in quarters:
            element = KeyElement(
                element_type='time_reference',
                value={
                    'type': 'quarter',
                    'value': match.group(0)
                },
                context=self._get_surrounding_text(text, match.start(), match.end()),
                confidence=0.9,
                position=match.start()
            )
            time_refs.append(element)
        
        return time_refs
    
    def _split_sentences(self, text: str) -> List[str]:
        """分割句子"""
        # 簡單的句子分割
        sentences = re.split(r'[.!?。！？]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_numbers_with_context(self, text: str) -> List[Tuple[float, str]]:
        """提取數字及其上下文"""
        results = []
        
        # 匹配各種數字格式
        pattern = r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*([%$¥€£萬億百千]?)'
        matches = re.finditer(pattern, text)
        
        for match in matches:
            number_str = match.group(1).replace(',', '')
            unit = match.group(2)
            
            try:
                number = float(number_str)
                
                # 處理中文數字單位
                if unit == '萬':
                    number *= 10000
                elif unit == '億':
                    number *= 100000000
                elif unit == '千':
                    number *= 1000
                elif unit == '百':
                    number *= 100
                
                context = text[max(0, match.start() - 20):min(len(text), match.end() + 20)]
                results.append((number, context))
            except ValueError:
                continue
        
        return results
    
    def _detect_unit(self, context: str) -> str:
        """檢測數值單位"""
        units = {
            '$': 'USD',
            '¥': 'CNY',
            '€': 'EUR',
            '£': 'GBP',
            '%': 'percentage',
            '萬': '10K',
            '億': '100M'
        }
        
        for symbol, unit in units.items():
            if symbol in context:
                return unit
        
        return 'number'
    
    def _classify_metric_type(self, sentence: str) -> str:
        """分類指標類型"""
        sentence_lower = sentence.lower()
        
        if any(word in sentence_lower for word in ['conversion', '轉換']):
            return 'conversion'
        elif any(word in sentence_lower for word in ['retention', '留存']):
            return 'retention'
        elif any(word in sentence_lower for word in ['growth', '增長', '成長']):
            return 'growth'
        elif any(word in sentence_lower for word in ['revenue', '營收']):
            return 'revenue'
        else:
            return 'general'
    
    def _get_context_words(self, sentence: str, term: str) -> List[str]:
        """獲取術語周圍的上下文詞彙"""
        words = sentence.split()
        term_words = term.split()
        context_words = []
        
        for i, word in enumerate(words):
            if word.lower() in [w.lower() for w in term_words]:
                # 獲取前後各2個詞
                start = max(0, i - 2)
                end = min(len(words), i + 3)
                context_words.extend(words[start:end])
        
        return list(set(context_words) - set(term_words))
    
    def _classify_tactical_category(self, term: str) -> str:
        """分類戰術術語類別"""
        term_lower = term.lower()
        
        if term_lower in ['strategy', '策略']:
            return 'strategic'
        elif term_lower in ['tactic', '戰術']:
            return 'tactical'
        elif term_lower in ['analysis', '分析']:
            return 'analytical'
        elif term_lower in ['implementation', '實施']:
            return 'operational'
        else:
            return 'general'
    
    def _get_surrounding_text(self, text: str, start: int, end: int, window: int = 50) -> str:
        """獲取周圍文本"""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)
        return text[context_start:context_end]
    
    def _classify_time_context(self, context: str) -> str:
        """分類時間上下文"""
        context_lower = context.lower()
        
        if any(word in context_lower for word in ['forecast', 'predict', '預測', '預計']):
            return 'future'
        elif any(word in context_lower for word in ['history', 'past', '歷史', '過去']):
            return 'past'
        elif any(word in context_lower for word in ['current', 'present', '當前', '目前']):
            return 'present'
        else:
            return 'unspecified'