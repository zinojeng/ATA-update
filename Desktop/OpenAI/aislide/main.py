"""
AI Slides - 主程式入口
實現 Step 1: 資料解析與語義分層
"""

import os
import sys
from typing import Dict, Any
import json
from datetime import datetime

# 添加 src 到 Python 路徑
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from parsers.text_parser import TextParser
from extractors.key_element_extractor import KeyElementExtractor
from extractors.semantic_extractor import SemanticExtractor


class AISlidesPipeline:
    """AI Slides 處理管線"""
    
    def __init__(self):
        # 初始化解析器
        self.parsers = {
            'text': TextParser()
        }
        
        # 初始化提取器
        self.key_extractor = KeyElementExtractor()
        self.semantic_extractor = SemanticExtractor()
    
    def process_step1(self, file_path: str) -> Dict[str, Any]:
        """
        執行 Step 1: 資料解析與語義分層
        
        Args:
            file_path: 輸入檔案路徑
            
        Returns:
            Dict: 處理結果
        """
        print(f"[Step 1] 開始處理檔案: {file_path}")
        
        # 1. 檔案解析
        print("  1.1 解析檔案結構...")
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in ['.txt', '.md', '.csv']:
            parser = self.parsers['text']
        else:
            raise ValueError(f"目前不支援的檔案格式: {file_ext}")
        
        parsed_doc = parser.parse(file_path)
        print(f"  ✓ 解析完成，找到 {len(parsed_doc.contents)} 個內容區塊")
        
        # 2. 關鍵元素提取
        print("  1.2 提取關鍵元素...")
        all_text = ' '.join([content.raw_content for content in parsed_doc.contents 
                           if isinstance(content.raw_content, str)])
        
        key_elements = self.key_extractor.extract(all_text)
        
        element_counts = {
            k: len(v) for k, v in key_elements.items()
        }
        print(f"  ✓ 提取完成: {element_counts}")
        
        # 3. 語義分層
        print("  1.3 進行語義分層...")
        semantic_structure = self.semantic_extractor.extract_semantic_structure(all_text)
        
        print(f"  ✓ 語義分層完成:")
        print(f"    - 核心論點: {len(semantic_structure.core_arguments)} 個")
        print(f"    - 支持證據: {len(semantic_structure.supporting_evidence)} 個")
        print(f"    - 參考資料: {len(semantic_structure.references)} 個")
        print(f"    - 結構類型: {semantic_structure.structure_type}")
        
        # 4. 資訊壓縮
        print("  1.4 壓縮資訊...")
        compressed_info = self.semantic_extractor.compress_information(all_text)
        print(f"  ✓ 壓縮完成，壓縮率: {compressed_info['compression_ratio']:.1%}")
        
        # 組合結果
        result = {
            'timestamp': datetime.now().isoformat(),
            'file_info': {
                'filename': parsed_doc.filename,
                'file_type': parsed_doc.file_type,
                'metadata': parsed_doc.metadata
            },
            'parsed_content': {
                'content_blocks': len(parsed_doc.contents),
                'summary': parsed_doc.summary,
                'key_points': parsed_doc.key_points,
                'entities': parsed_doc.entities
            },
            'key_elements': element_counts,
            'semantic_structure': {
                'type': semantic_structure.structure_type,
                'core_arguments': [
                    {
                        'content': arg.content[:200] + '...' if len(arg.content) > 200 else arg.content,
                        'score': arg.importance_score,
                        'keywords': arg.keywords[:5]
                    }
                    for arg in semantic_structure.core_arguments[:3]
                ],
                'summary': semantic_structure.summary
            },
            'compression': {
                'original_length': compressed_info['original_length'],
                'compressed_length': compressed_info['compressed_length'],
                'compression_ratio': compressed_info['compression_ratio'],
                'key_sentences': [s['text'] for s in compressed_info['key_sentences'][:5]]
            }
        }
        
        return result
    
    def save_result(self, result: Dict[str, Any], output_path: str):
        """保存處理結果"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n結果已保存至: {output_path}")


def main():
    """主函數"""
    print("=== AI Slides - Step 1: 資料解析與語義分層 ===\n")
    
    # 檢查命令列參數
    if len(sys.argv) < 2:
        print("使用方式: python main.py <輸入檔案路徑>")
        print("範例: python main.py Examples/sample.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # 檢查檔案是否存在
    if not os.path.exists(input_file):
        print(f"錯誤: 找不到檔案 {input_file}")
        sys.exit(1)
    
    # 建立處理管線
    pipeline = AISlidesPipeline()
    
    try:
        # 執行 Step 1
        result = pipeline.process_step1(input_file)
        
        # 保存結果
        output_file = os.path.splitext(input_file)[0] + '_step1_result.json'
        pipeline.save_result(result, output_file)
        
        # 顯示部分結果
        print("\n=== 處理結果摘要 ===")
        print(f"檔案: {result['file_info']['filename']}")
        print(f"內容區塊: {result['parsed_content']['content_blocks']}")
        print(f"\n關鍵元素統計:")
        for element_type, count in result['key_elements'].items():
            print(f"  - {element_type}: {count}")
        
        print(f"\n語義結構類型: {result['semantic_structure']['type']}")
        print(f"\n核心論點 (前3個):")
        for i, arg in enumerate(result['semantic_structure']['core_arguments'], 1):
            print(f"  {i}. {arg['content']}")
            print(f"     重要性分數: {arg['score']:.2f}")
            print(f"     關鍵詞: {', '.join(arg['keywords'])}")
        
        print(f"\n資訊壓縮率: {result['compression']['compression_ratio']:.1%}")
        
    except Exception as e:
        print(f"\n錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()