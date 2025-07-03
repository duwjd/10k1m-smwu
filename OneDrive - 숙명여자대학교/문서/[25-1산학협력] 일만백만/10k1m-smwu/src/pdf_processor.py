"""
개선된 PDF 처리기 - 이미지 추출과 정확한 텍스트 추출 통합
src/pdf_processor.py 파일을 이 내용으로 완전히 교체하세요
"""

import os
import json
import logging
from typing import List, Dict, Tuple, Optional
import fitz  # PyMuPDF
import pdfplumber
from google.cloud import vision
from google.oauth2 import service_account
from anthropic import Anthropic
from PIL import Image, ImageEnhance
import io
import hashlib

from config.settings import *
from src.image_utils import ImageProcessor
from src.color_extractor import ColorExtractor

# 로깅 설정
logging.basicConfig(
    level=logging.INFO if DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(PROJECT_ROOT, 'logs', 'processor.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedPDFProcessor:
    """향상된 PDF to JSON 변환기 - 이미지 추출 + 정확한 텍스트 추출"""
    
    def __init__(self):
        """초기화"""
        self.setup_directories()
        self.setup_clients()
        self.image_processor = ImageProcessor()
        self.color_extractor = ColorExtractor()
        
        # 추출된 이미지 저장 폴더
        self.extracted_images_dir = os.path.join(IMAGES_DIR, "extracted")
        os.makedirs(self.extracted_images_dir, exist_ok=True)
        
        logger.info("향상된 PDF 처리기 초기화 완료")
    
    def setup_directories(self):
        """필요한 디렉토리 생성"""
        directories = [DATA_DIR, IMAGES_DIR, OUTPUT_DIR, INPUT_DIR, 
                      os.path.join(PROJECT_ROOT, 'logs')]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def setup_clients(self):
        """API 클라이언트 설정"""
        try:
            # Claude API 클라이언트
            if not CLAUDE_API_KEY:
                raise ValueError("CLAUDE_API_KEY가 설정되지 않았습니다")
            self.claude_client = Anthropic(api_key=CLAUDE_API_KEY)
            
            # Google Vision API 클라이언트 (OCR 보조용)
            if GOOGLE_APPLICATION_CREDENTIALS and os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
                credentials = service_account.Credentials.from_service_account_file(
                    GOOGLE_APPLICATION_CREDENTIALS,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
                self.vision_client = vision.ImageAnnotatorClient(credentials=credentials)
                self.use_vision = True
            else:
                logger.warning("Google Vision API 키가 없습니다. OCR 기능이 제한됩니다.")
                self.vision_client = None
                self.use_vision = False
            
            logger.info("API 클라이언트 설정 완료")
            
        except Exception as e:
            logger.error(f"API 클라이언트 설정 실패: {e}")
            raise
    
    def process_pdf(self, pdf_path: str) -> Tuple[Optional[str], Optional[str]]:
        """PDF 파일을 JSON 템플릿으로 변환"""
        try:
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
            
            logger.info(f"PDF 처리 시작: {pdf_path}")
            
            # PDF 열기
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            
            all_scene_data = []
            all_colors = []
            
            # 각 페이지 처리
            for page_index in range(total_pages):
                logger.info(f"페이지 {page_index + 1}/{total_pages} 처리 중...")
                
                scene_data = self._process_page_enhanced(doc, pdf_path, page_index)
                if scene_data:
                    all_scene_data.append(scene_data)
                    all_colors.extend(scene_data.get('colors', []))
            
            doc.close()
            
            if not all_scene_data:
                logger.warning("처리된 페이지가 없습니다")
                return None, None
            
            # Claude로 JSON 생성
            logger.info("Claude API로 JSON 템플릿 생성 중...")
            json_result = self._generate_enhanced_json_template(all_scene_data, all_colors)
            
            if json_result:
                # 결과 저장
                output_path = self._save_result(pdf_path, json_result)
                logger.info(f"처리 완료: {output_path}")
                return output_path, json_result
            else:
                logger.error("JSON 생성 실패")
                return None, None
                
        except Exception as e:
            logger.error(f"PDF 처리 실패: {e}")
            return None, None
    
    def _process_page_enhanced(self, doc: fitz.Document, pdf_path: str, page_index: int) -> Optional[Dict]:
        """향상된 페이지 처리 - 이미지와 텍스트 모두 추출"""
        try:
            page = doc[page_index]
            
            # 1. 배경 이미지 저장
            background_img = self._save_background_image(page, page_index)
            
            # 2. PDF 내장 이미지들 추출
            extracted_images = self._extract_embedded_images(page, page_index)
            
            # 3. 색상 추출 (배경 이미지에서)
            bg_img_path = os.path.join(IMAGES_DIR, background_img)
            with open(bg_img_path, 'rb') as f:
                img_bytes = f.read()
            colors = self.color_extractor.extract_dominant_colors(img_bytes)
            
            # 4. 정확한 텍스트 추출
            text_elements = self._extract_text_elements_accurate(pdf_path, page_index)
            
            return {
                'page_index': page_index,
                'background_image': background_img,
                'extracted_images': extracted_images,
                'text_elements': text_elements,
                'colors': colors,
                'layout_info': self._analyze_page_layout(page)
            }
            
        except Exception as e:
            logger.error(f"페이지 {page_index + 1} 처리 실패: {e}")
            return None
    
    def _save_background_image(self, page: fitz.Page, page_index: int) -> str:
        """배경 이미지 저장"""
        matrix = fitz.Matrix(IMAGE_RESOLUTION_SCALE, IMAGE_RESOLUTION_SCALE)
        pix = page.get_pixmap(matrix=matrix)
        
        img_filename = f"page_{page_index + 1}_background.png"
        img_path = os.path.join(IMAGES_DIR, img_filename)
        pix.save(img_path)
        
        logger.debug(f"배경 이미지 저장: {img_path}")
        return img_filename
    
    def _extract_embedded_images(self, page: fitz.Page, page_index: int) -> List[Dict]:
        """PDF에서 내장 이미지들 추출"""
        extracted_images = []
        image_list = page.get_images()
        
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                base_image = page.parent.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # 작은 이미지는 제외 (아이콘 등)
                if len(image_bytes) < 1000:
                    continue
                
                # 파일명 생성
                image_hash = hashlib.md5(image_bytes).hexdigest()[:8]
                img_filename = f"page_{page_index + 1}_extracted_{img_index + 1}_{image_hash}.{image_ext}"
                img_path = os.path.join(self.extracted_images_dir, img_filename)
                
                # 이미지 저장
                with open(img_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                # 크기 정보
                pil_image = Image.open(io.BytesIO(image_bytes))
                width, height = pil_image.size
                
                extracted_images.append({
                    'filename': img_filename,
                    'relative_path': f"extracted/{img_filename}",
                    'size': {'width': width, 'height': height},
                    'file_size': len(image_bytes),
                    'format': image_ext.upper()
                })
                
                logger.info(f"이미지 추출: {img_filename} ({width}x{height})")
                
            except Exception as e:
                logger.warning(f"이미지 {img_index} 추출 실패: {e}")
                continue
        
        return extracted_images
    
    def _extract_text_elements_accurate(self, pdf_path: str, page_index: int) -> List[Dict]:
        """pdfplumber로 정확한 텍스트 추출"""
        text_elements = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                page = pdf.pages[page_index]
                
                # 문자 단위로 추출
                chars = page.chars
                if not chars:
                    logger.warning(f"페이지 {page_index + 1}에서 텍스트 없음")
                    return []
                
                # 줄 단위로 그룹핑
                lines = self._group_chars_into_lines(chars)
                
                # 텍스트 블록으로 변환
                for line in lines:
                    if line.get('text', '').strip() and len(line.get('text', '').strip()) > 1:
                        text_elements.append({
                            'text': line['text'].strip(),
                            'x': int(line['x']),
                            'y': int(line['y']),
                            'width': int(line['width']),
                            'height': int(line['height']),
                            'fontSize': int(line['fontSize']),
                            'fontWeight': self._determine_font_weight(line),
                            'fontColor': '#333333',
                            'textAlign': self._determine_text_align(line),
                            'importance': self._determine_importance(line)
                        })
                
                logger.info(f"페이지 {page_index + 1}에서 {len(text_elements)}개 텍스트 추출")
                
        except Exception as e:
            logger.error(f"텍스트 추출 실패: {e}")
        
        return text_elements
    
    def _group_chars_into_lines(self, chars: List[Dict]) -> List[Dict]:
        """문자들을 줄 단위로 그룹핑"""
        if not chars:
            return []
        
        sorted_chars = sorted(chars, key=lambda c: (c['y0'], c['x0']))
        
        lines = []
        current_line = []
        current_y = sorted_chars[0]['y0']
        tolerance = 3
        
        for char in sorted_chars:
            if abs(char['y0'] - current_y) <= tolerance:
                current_line.append(char)
            else:
                if current_line:
                    lines.append(self._process_char_line(current_line))
                current_line = [char]
                current_y = char['y0']
        
        if current_line:
            lines.append(self._process_char_line(current_line))
        
        return [line for line in lines if line.get('text', '').strip()]
    
    def _process_char_line(self, chars: List[Dict]) -> Dict:
        """문자 줄 처리"""
        if not chars:
            return {}
        
        chars.sort(key=lambda c: c['x0'])
        text = ''.join([char['text'] for char in chars])
        
        min_x = min([c['x0'] for c in chars])
        min_y = min([c['y0'] for c in chars])
        max_x = max([c['x1'] for c in chars])
        max_y = max([c['y1'] for c in chars])
        
        # 폰트 크기
        font_sizes = [c.get('size', 12) for c in chars if c.get('size')]
        font_size = max(set(font_sizes), key=font_sizes.count) if font_sizes else 12
        
        return {
            'text': text.strip(),
            'x': min_x,
            'y': min_y,
            'width': max_x - min_x,
            'height': max_y - min_y,
            'fontSize': font_size
        }
    
    def _determine_font_weight(self, element: Dict) -> int:
        """폰트 굵기 결정"""
        font_size = element.get('fontSize', 12)
        text_length = len(element.get('text', ''))
        
        if font_size >= 24:
            return 900  # 매우 굵게 (큰 제목)
        elif font_size >= 18:
            return 700  # 굵게 (부제목)
        elif font_size >= 14 and text_length < 50:
            return 600  # 중간 굵기 (작은 제목)
        else:
            return 400  # 보통 (본문)
    
    def _determine_text_align(self, element: Dict) -> str:
        """텍스트 정렬 결정"""
        x = element.get('x', 0)
        
        if x < 100:
            return 'left'
        elif x > 400:
            return 'center'
        else:
            return 'left'
    
    def _determine_importance(self, element: Dict) -> str:
        """중요도 결정"""
        font_size = element.get('fontSize', 12)
        
        if font_size >= 24:
            return 'title'
        elif font_size >= 18:
            return 'subtitle'
        else:
            return 'body'
    
    def _analyze_page_layout(self, page: fitz.Page) -> Dict:
        """페이지 레이아웃 분석"""
        rect = page.rect
        return {
            'width': rect.width,
            'height': rect.height,
            'has_images': len(page.get_images()) > 0
        }
    
    def _generate_enhanced_json_template(self, scene_data_list: List[Dict], all_colors: List[str]) -> Optional[str]:
        """향상된 JSON 템플릿 생성 - 실제 텍스트와 이미지 사용"""
        try:
            prompt = self._create_detailed_prompt(scene_data_list, all_colors)
            
            response = self.claude_client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=4096,
                temperature=0.1,
                system="You are a JSON generator for video scenes. Create valid JSON using the provided text and image data. Respond with JSON only.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_json = response.content[0].text.strip()
            
            # 응답 정리
            result_json = result_json.replace('```json', '').replace('```', '').strip()
            
            # 빈 응답 체크
            if len(result_json) < 10:
                logger.warning("Claude 응답이 너무 짧음, 폴백 JSON 생성")
                return self._create_fallback_json_with_real_data(scene_data_list)
            
            # JSON 검증
            try:
                json.loads(result_json)
                logger.info("유효한 JSON 생성 완료")
                return result_json
            except json.JSONDecodeError as e:
                logger.error(f"JSON 파싱 실패: {e}")
                return self._create_fallback_json_with_real_data(scene_data_list)
                
        except Exception as e:
            logger.error(f"Claude API 호출 실패: {e}")
            return self._create_fallback_json_with_real_data(scene_data_list)
    
    def _create_detailed_prompt(self, scene_data_list: List[Dict], all_colors: List[str]) -> str:
        """실제 데이터 기반 상세 프롬프트"""
        colors = ', '.join(list(set(all_colors))[:3]) if all_colors else '#333333, #666666, #999999'
        
        prompt = f"""Create a JSON array for video scenes using this REAL extracted data.

Use these colors: {colors}

"""
        
        for i, scene_data in enumerate(scene_data_list):
            scene_start = i * 5000
            scene_end = (i + 1) * 5000
            
            prompt += f"""
SCENE {i+1} (timeFrame: {scene_start}-{scene_end}ms):

Background Image: {scene_data['background_image']}

Extracted Images ({len(scene_data['extracted_images'])}):"""
            
            for img in scene_data['extracted_images']:
                prompt += f"\n- {img['relative_path']} ({img['size']['width']}x{img['size']['height']})"
            
            prompt += f"\n\nText Elements ({len(scene_data['text_elements'])}):"
            
            for text in scene_data['text_elements']:
                prompt += f'\n- Text: "{text["text"]}"'
                prompt += f' | Position: ({text["x"]}, {text["y"]})'
                prompt += f' | Size: {text["fontSize"]}px | Weight: {text["fontWeight"]} | Importance: {text["importance"]}'
        
        prompt += f"""

Create a JSON array with {len(scene_data_list)} scenes. Use the EXACT text content and image filenames provided above.

Structure:
[
  {{
    "timeFrame": {{"start": 0, "end": 5000}},
    "editorElements": [
      // Use background image as main image
      // Use extracted images as separate image elements  
      // Use exact text content with proper positioning and styling
    ]
  }}
]

Important:
- Use EXACT text content from "Text Elements"
- Use EXACT image filenames from "Extracted Images" 
- Apply appropriate fontSize, fontWeight based on "importance"
- Distribute elements across the timeFrame
- Make title text larger (fontSize 48-72) and bold (fontWeight 700-900)
- Use the provided colors

JSON only, no explanations:"""
        
        return prompt
    
    def _create_fallback_json_with_real_data(self, scene_data_list: List[Dict]) -> str:
        """실제 데이터를 사용한 폴백 JSON"""
        scenes = []
        
        for i, scene_data in enumerate(scene_data_list):
            scene_start = i * 5000
            scene_end = (i + 1) * 5000
            
            elements = []
            
            # 배경 이미지
            elements.append({
                "type": "image",
                "placement": {"x": 0, "y": 0, "width": 1080, "height": 1920, "scaleX": 1, "scaleY": 1},
                "properties": {"src": scene_data['background_image']},
                "timeFrame": {"start": scene_start, "end": scene_end}
            })
            
            # 추출된 이미지들
            for j, img in enumerate(scene_data['extracted_images'][:3]):  # 최대 3개
                elements.append({
                    "type": "image",
                    "placement": {
                        "x": 100 + j * 150,
                        "y": 200 + j * 100,
                        "width": min(400, img['size']['width']),
                        "height": min(300, img['size']['height']),
                        "scaleX": 1,
                        "scaleY": 1
                    },
                    "properties": {"src": img['relative_path']},
                    "timeFrame": {"start": scene_start + j * 500, "end": scene_end}
                })
            
            # 텍스트 요소들
            for j, text in enumerate(scene_data['text_elements'][:10]):  # 최대 10개
                elements.append({
                    "type": "text",
                    "placement": {
                        "x": text['x'],
                        "y": text['y'],
                        "width": max(text['width'], 100),
                        "height": max(text['height'], 30),
                        "scaleX": 1,
                        "scaleY": 1
                    },
                    "properties": {
                        "text": text['text'],
                        "fontSize": text['fontSize'],
                        "fontWeight": text['fontWeight'],
                        "fontColor": text['fontColor'],
                        "textAlign": text['textAlign'],
                        "lineHeight": 1.4
                    },
                    "timeFrame": {"start": scene_start + j * 200, "end": scene_end}
                })
            
            scenes.append({
                "timeFrame": {"start": scene_start, "end": scene_end},
                "editorElements": elements
            })
        
        return json.dumps(scenes, ensure_ascii=False, indent=2)
    
    def _save_result(self, pdf_path: str, json_result: str) -> str:
        """결과 저장"""
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_filename = f"{base_name}_enhanced.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_result)
        
        return output_path
    
    def get_processing_stats(self) -> Dict:
        """처리 통계"""
        return {
            'images_count': len([f for f in os.listdir(IMAGES_DIR) if f.endswith('.png')]),
            'extracted_images_count': len([f for f in os.listdir(self.extracted_images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]) if os.path.exists(self.extracted_images_dir) else 0,
            'outputs_count': len([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.json')]),
            'images_dir': IMAGES_DIR,
            'output_dir': OUTPUT_DIR
        }

# 편의 함수들
def process_pdf_file(pdf_path: str) -> Tuple[Optional[str], Optional[str]]:
    """PDF 파일 처리 편의 함수"""
    processor = EnhancedPDFProcessor()
    return processor.process_pdf(pdf_path)

def get_available_pdfs() -> List[str]:
    """입력 폴더의 PDF 파일 목록 반환"""
    if not os.path.exists(INPUT_DIR):
        return []
    return [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]

def get_generated_jsons() -> List[str]:
    """출력 폴더의 JSON 파일 목록 반환"""
    if not os.path.exists(OUTPUT_DIR):
        return []
    return [f for f in os.listdir(OUTPUT_DIR) if f.lower().endswith('.json')]