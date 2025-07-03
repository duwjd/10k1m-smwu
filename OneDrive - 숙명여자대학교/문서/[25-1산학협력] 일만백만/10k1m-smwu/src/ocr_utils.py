"""
OCR 처리 유틸리티
"""
from google.cloud import vision
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, vision_client):
        self.vision_client = vision_client
    
    def extract_text_with_positions(self, image_bytes: bytes) -> List[Dict]:
        """텍스트와 위치 정보 추출"""
        try:
            image = vision.Image(content=image_bytes)
            response = self.vision_client.text_detection(image=image)
            annotations = response.text_annotations

            if not annotations:
                return []

            words = annotations[1:]
            lines_data = self._group_words_into_lines(words)
            return lines_data
            
        except Exception as e:
            logger.error(f"OCR 처리 실패: {e}")
            return []
    
    def _group_words_into_lines(self, words) -> List[Dict]:
        """단어들을 줄 단위로 그룹핑"""
        if not words:
            return []
        
        words_sorted = sorted(words, key=lambda w: w.bounding_poly.vertices[0].y)
        
        lines_data = []
        current_line = []
        current_y = words_sorted[0].bounding_poly.vertices[0].y
        line_tolerance = 20
        
        for word in words_sorted:
            word_y = word.bounding_poly.vertices[0].y
            
            if abs(word_y - current_y) <= line_tolerance:
                current_line.append(word)
            else:
                if current_line:
                    lines_data.append(self._process_line(current_line))
                current_line = [word]
                current_y = word_y
        
        if current_line:
            lines_data.append(self._process_line(current_line))
        
        return lines_data
    
    def _process_line(self, words_in_line) -> Dict:
        """한 줄의 단어들 처리"""
        words_in_line.sort(key=lambda w: w.bounding_poly.vertices[0].x)
        
        line_text = ' '.join([word.description for word in words_in_line])
        
        min_x = min([w.bounding_poly.vertices[0].x for w in words_in_line])
        min_y = min([w.bounding_poly.vertices[0].y for w in words_in_line])
        max_x = max([w.bounding_poly.vertices[1].x for w in words_in_line])
        max_y = max([w.bounding_poly.vertices[2].y for w in words_in_line])
        
        font_size = max_y - min_y
        
        return {
            "text": line_text,
            "x": min_x,
            "y": min_y,
            "width": max_x - min_x,
            "height": max_y - min_y,
            "fontSize": max(12, min(72, font_size))
        }
