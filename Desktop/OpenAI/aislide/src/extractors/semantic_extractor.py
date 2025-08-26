"""
語義提取器
負責資訊分層壓縮，將冗長內容分解為核心論點與支持證據
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import re


@dataclass
class SemanticLayer:
    """語義層級資料結構"""
    layer_type: str  # 層級類型：core_argument, supporting_evidence, reference
    content: str  # 內容
    importance_score: float  # 重要性分數
    keywords: List[str]  # 關鍵詞
    related_indices: List[int]  # 相關內容索引


@dataclass
class InformationStructure:
    """資訊結構"""
    core_arguments: List[SemanticLayer]  # 核心論點
    supporting_evidence: List[SemanticLayer]  # 支持證據
    references: List[SemanticLayer]  # 參考資料
    summary: str  # 總結
    structure_type: str  # 結構類型


class SemanticExtractor:
    """語義提取器"""
    
    def __init__(self):
        # 核心論點標記詞
        self.core_markers = [
            'therefore', 'thus', 'hence', 'consequently', 'in conclusion',
            'the key point', 'importantly', 'significantly', 'mainly',
            '因此', '所以', '總之', '重要的是', '關鍵是', '主要', '核心'
        ]
        
        # 證據標記詞
        self.evidence_markers = [
            'for example', 'such as', 'including', 'according to', 'data shows',
            'research indicates', 'studies show', 'evidence suggests',
            '例如', '比如', '包括', '根據', '數據顯示', '研究表明', '證據顯示'
        ]
        
        # 權威來源標記
        self.authority_markers = [
            'university', 'institute', 'research', 'journal', 'professor',
            'expert', 'study', 'report', 'survey',
            '大學', '研究所', '研究', '期刊', '教授', '專家', '報告', '調查'
        ]
    
    def extract_semantic_structure(self, text: str) -> InformationStructure:
        """
        提取語義結構
        
        Args:
            text: 輸入文本
            
        Returns:
            InformationStructure: 分層的資訊結構
        """
        # 分割段落
        paragraphs = self._split_paragraphs(text)
        
        # 分類段落
        classified_paragraphs = self._classify_paragraphs(paragraphs)
        
        # 提取各層級內容
        core_arguments = self._extract_core_arguments(classified_paragraphs)
        supporting_evidence = self._extract_supporting_evidence(classified_paragraphs)
        references = self._extract_references(classified_paragraphs)
        
        # 生成總結
        summary = self._generate_structured_summary(core_arguments, supporting_evidence)
        
        # 確定結構類型
        structure_type = self._determine_structure_type(classified_paragraphs)
        
        return InformationStructure(
            core_arguments=core_arguments,
            supporting_evidence=supporting_evidence,
            references=references,
            summary=summary,
            structure_type=structure_type
        )
    
    def compress_information(self, text: str) -> Dict[str, Any]:
        """
        壓縮資訊，過濾重複和低質量內容
        
        Args:
            text: 輸入文本
            
        Returns:
            Dict: 壓縮後的資訊
        """
        # 提取句子
        sentences = self._split_sentences(text)
        
        # 計算句子重要性
        scored_sentences = self._score_sentences(sentences)
        
        # 去除重複
        unique_sentences = self._remove_duplicates(scored_sentences)
        
        # 過濾低質量內容
        filtered_sentences = self._filter_low_quality(unique_sentences)
        
        # 重組內容
        compressed_content = {
            'original_length': len(text),
            'compressed_length': sum(len(s['text']) for s in filtered_sentences),
            'compression_ratio': 1 - (sum(len(s['text']) for s in filtered_sentences) / len(text)),
            'key_sentences': filtered_sentences[:10],  # 前10個最重要的句子
            'removed_content_types': self._identify_removed_content(sentences, filtered_sentences)
        }
        
        return compressed_content
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """分割段落"""
        # 按空行分割
        paragraphs = re.split(r'\n\s*\n', text)
        # 過濾空段落
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _split_sentences(self, text: str) -> List[str]:
        """分割句子"""
        # 使用正則表達式分割句子，保留句號
        sentences = re.split(r'(?<=[.!?。！？])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _classify_paragraphs(self, paragraphs: List[str]) -> List[Dict[str, Any]]:
        """分類段落"""
        classified = []
        
        for i, paragraph in enumerate(paragraphs):
            para_lower = paragraph.lower()
            
            # 計算各類標記詞的出現次數
            core_score = sum(1 for marker in self.core_markers if marker in para_lower)
            evidence_score = sum(1 for marker in self.evidence_markers if marker in para_lower)
            authority_score = sum(1 for marker in self.authority_markers if marker in para_lower)
            
            # 判斷段落類型
            if core_score >= evidence_score and core_score >= authority_score:
                para_type = 'core_argument'
            elif evidence_score > core_score and evidence_score >= authority_score:
                para_type = 'supporting_evidence'
            elif authority_score > 0:
                para_type = 'reference'
            else:
                para_type = 'general'
            
            classified.append({
                'index': i,
                'text': paragraph,
                'type': para_type,
                'scores': {
                    'core': core_score,
                    'evidence': evidence_score,
                    'authority': authority_score
                }
            })
        
        return classified
    
    def _extract_core_arguments(self, classified_paragraphs: List[Dict]) -> List[SemanticLayer]:
        """提取核心論點"""
        core_arguments = []
        
        for para in classified_paragraphs:
            if para['type'] in ['core_argument', 'general']:
                # 提取關鍵句子
                sentences = self._split_sentences(para['text'])
                key_sentences = self._identify_key_sentences(sentences)
                
                if key_sentences:
                    keywords = self._extract_keywords(para['text'])
                    
                    layer = SemanticLayer(
                        layer_type='core_argument',
                        content=' '.join(key_sentences),
                        importance_score=self._calculate_importance_score(para),
                        keywords=keywords,
                        related_indices=self._find_related_paragraphs(para, classified_paragraphs)
                    )
                    core_arguments.append(layer)
        
        return sorted(core_arguments, key=lambda x: x.importance_score, reverse=True)
    
    def _extract_supporting_evidence(self, classified_paragraphs: List[Dict]) -> List[SemanticLayer]:
        """提取支持證據"""
        evidence_layers = []
        
        for para in classified_paragraphs:
            if para['type'] == 'supporting_evidence':
                # 提取數據和例子
                data_points = self._extract_data_points(para['text'])
                examples = self._extract_examples(para['text'])
                
                if data_points or examples:
                    layer = SemanticLayer(
                        layer_type='supporting_evidence',
                        content=para['text'],
                        importance_score=self._calculate_evidence_score(data_points, examples),
                        keywords=self._extract_keywords(para['text']),
                        related_indices=[]
                    )
                    evidence_layers.append(layer)
        
        return evidence_layers
    
    def _extract_references(self, classified_paragraphs: List[Dict]) -> List[SemanticLayer]:
        """提取參考資料"""
        references = []
        
        for para in classified_paragraphs:
            if para['type'] == 'reference' or para['scores']['authority'] > 0:
                # 提取引用資訊
                citations = self._extract_citations(para['text'])
                
                if citations:
                    layer = SemanticLayer(
                        layer_type='reference',
                        content=para['text'],
                        importance_score=len(citations) * 0.5,
                        keywords=citations,
                        related_indices=[]
                    )
                    references.append(layer)
        
        return references
    
    def _score_sentences(self, sentences: List[str]) -> List[Dict[str, Any]]:
        """評分句子重要性"""
        scored = []
        
        for i, sentence in enumerate(sentences):
            score = 0
            
            # 長度分數（適中長度較好）
            length = len(sentence.split())
            if 10 <= length <= 30:
                score += 2
            elif 5 <= length <= 40:
                score += 1
            
            # 包含數字加分
            if re.search(r'\d+', sentence):
                score += 2
            
            # 包含關鍵標記詞加分
            sentence_lower = sentence.lower()
            for markers in [self.core_markers, self.evidence_markers]:
                if any(marker in sentence_lower for marker in markers):
                    score += 3
            
            # 位置分數（開頭和結尾較重要）
            if i < 2 or i >= len(sentences) - 2:
                score += 1
            
            scored.append({
                'index': i,
                'text': sentence,
                'score': score
            })
        
        return scored
    
    def _remove_duplicates(self, scored_sentences: List[Dict]) -> List[Dict]:
        """去除重複句子"""
        unique = []
        seen_content = set()
        
        for sentence in scored_sentences:
            # 簡化文本用於比較
            simplified = re.sub(r'\s+', ' ', sentence['text'].lower())
            simplified = re.sub(r'[^\w\s]', '', simplified)
            
            if simplified not in seen_content:
                seen_content.add(simplified)
                unique.append(sentence)
        
        return unique
    
    def _filter_low_quality(self, sentences: List[Dict]) -> List[Dict]:
        """過濾低質量內容"""
        filtered = []
        
        for sentence in sentences:
            # 過濾太短的句子
            if len(sentence['text'].split()) < 5:
                continue
            
            # 過濾純廣告或商業化內容
            if self._is_commercial_content(sentence['text']):
                continue
            
            # 過濾低分句子
            if sentence['score'] < 2:
                continue
            
            filtered.append(sentence)
        
        return sorted(filtered, key=lambda x: x['score'], reverse=True)
    
    def _is_commercial_content(self, text: str) -> bool:
        """判斷是否為商業化內容"""
        commercial_indicators = [
            'buy now', 'discount', 'sale', 'limited offer', 'click here',
            '立即購買', '優惠', '特價', '限時', '點擊這裡'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in commercial_indicators)
    
    def _identify_key_sentences(self, sentences: List[str]) -> List[str]:
        """識別關鍵句子"""
        key_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # 包含核心標記詞的句子
            if any(marker in sentence_lower for marker in self.core_markers):
                key_sentences.append(sentence)
            # 包含數據的句子
            elif re.search(r'\d+%|\d+\.\d+', sentence):
                key_sentences.append(sentence)
        
        return key_sentences[:3]  # 最多返回3個關鍵句子
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取關鍵詞"""
        # 簡單的關鍵詞提取：提取名詞短語
        words = text.split()
        keywords = []
        
        # 提取大寫開頭的詞組（可能是專有名詞）
        for i, word in enumerate(words):
            if word[0].isupper() and i > 0:
                keywords.append(word)
        
        # 提取包含數字的短語
        numeric_phrases = re.findall(r'\b\w*\d+\w*\b', text)
        keywords.extend(numeric_phrases)
        
        return list(set(keywords))[:10]
    
    def _extract_data_points(self, text: str) -> List[str]:
        """提取數據點"""
        # 提取包含數字的短語
        data_patterns = [
            r'\d+(?:\.\d+)?%',  # 百分比
            r'[$¥€£]\s*\d+(?:,\d{3})*(?:\.\d+)?',  # 貨幣
            r'\d+(?:,\d{3})*(?:\.\d+)?',  # 一般數字
        ]
        
        data_points = []
        for pattern in data_patterns:
            matches = re.findall(pattern, text)
            data_points.extend(matches)
        
        return data_points
    
    def _extract_examples(self, text: str) -> List[str]:
        """提取例子"""
        examples = []
        
        # 尋找例子標記詞後的內容
        for marker in ['for example', 'such as', 'e.g.', '例如', '比如']:
            pattern = f'{marker}[^.。]*[.。]'
            matches = re.findall(pattern, text, re.IGNORECASE)
            examples.extend(matches)
        
        return examples
    
    def _extract_citations(self, text: str) -> List[str]:
        """提取引用"""
        citations = []
        
        # 提取年份引用格式 (Author, Year)
        pattern1 = r'\([A-Za-z]+(?:\s+et\s+al\.)?,?\s+\d{4}\)'
        citations.extend(re.findall(pattern1, text))
        
        # 提取數字引用格式 [1], [2,3]
        pattern2 = r'\[\d+(?:,\s*\d+)*\]'
        citations.extend(re.findall(pattern2, text))
        
        return citations
    
    def _calculate_importance_score(self, paragraph: Dict) -> float:
        """計算段落重要性分數"""
        score = 0.0
        
        # 基於分類分數
        score += paragraph['scores']['core'] * 2
        score += paragraph['scores']['evidence'] * 1.5
        score += paragraph['scores']['authority'] * 1
        
        # 基於長度（適中為佳）
        word_count = len(paragraph['text'].split())
        if 50 <= word_count <= 200:
            score += 2
        
        # 基於位置（假設前面的段落更重要）
        score += (10 - paragraph['index']) * 0.1
        
        return score
    
    def _calculate_evidence_score(self, data_points: List[str], examples: List[str]) -> float:
        """計算證據分數"""
        return len(data_points) * 2 + len(examples) * 1.5
    
    def _find_related_paragraphs(self, current_para: Dict, all_paragraphs: List[Dict]) -> List[int]:
        """尋找相關段落"""
        related = []
        current_keywords = set(self._extract_keywords(current_para['text']))
        
        for para in all_paragraphs:
            if para['index'] != current_para['index']:
                para_keywords = set(self._extract_keywords(para['text']))
                
                # 計算關鍵詞重疊
                overlap = len(current_keywords & para_keywords)
                if overlap >= 2:
                    related.append(para['index'])
        
        return related
    
    def _generate_structured_summary(self, core_arguments: List[SemanticLayer], 
                                   supporting_evidence: List[SemanticLayer]) -> str:
        """生成結構化摘要"""
        summary_parts = []
        
        # 添加最重要的核心論點
        if core_arguments:
            summary_parts.append("核心論點：" + core_arguments[0].content)
        
        # 添加關鍵證據
        if supporting_evidence:
            key_evidence = supporting_evidence[0].content[:100] + "..."
            summary_parts.append("主要證據：" + key_evidence)
        
        return " ".join(summary_parts)
    
    def _determine_structure_type(self, classified_paragraphs: List[Dict]) -> str:
        """確定文本結構類型"""
        type_counts = {}
        for para in classified_paragraphs:
            para_type = para['type']
            type_counts[para_type] = type_counts.get(para_type, 0) + 1
        
        # 根據段落類型分布判斷
        if type_counts.get('core_argument', 0) > type_counts.get('supporting_evidence', 0):
            return 'argumentative'
        elif type_counts.get('supporting_evidence', 0) > type_counts.get('core_argument', 0):
            return 'evidence-based'
        elif type_counts.get('reference', 0) > len(classified_paragraphs) * 0.3:
            return 'academic'
        else:
            return 'mixed'
    
    def _identify_removed_content(self, original: List[str], filtered: List[Dict]) -> List[str]:
        """識別被移除的內容類型"""
        removed_types = []
        filtered_texts = [s['text'] for s in filtered]
        
        for sentence in original:
            if sentence not in filtered_texts:
                if self._is_commercial_content(sentence):
                    removed_types.append('commercial')
                elif len(sentence.split()) < 5:
                    removed_types.append('too_short')
                else:
                    removed_types.append('low_quality')
        
        return list(set(removed_types))