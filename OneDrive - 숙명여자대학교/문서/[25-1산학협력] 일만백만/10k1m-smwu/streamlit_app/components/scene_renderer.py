"""
로컬 이미지 전용 Scene Renderer
data\images\extracted 폴더의 이미지들만 사용
외부 다운로드 기능 제거
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import json
from typing import List, Dict, Optional
import logging
from PIL import Image, ImageDraw, ImageFont
import io
import glob

logger = logging.getLogger(__name__)

class SceneRenderer:
    """로컬 이미지 전용 Scene HTML 렌더러"""
    
    def __init__(self, images_dir: str = "data/images"):
        self.images_dir = images_dir
        self.extracted_images_dir = os.path.join(images_dir, "extracted")
        
        # 디렉토리 존재 확인
        if not os.path.exists(self.extracted_images_dir):
            st.warning(f"⚠️ 이미지 폴더를 찾을 수 없습니다: {self.extracted_images_dir}")
            os.makedirs(self.extracted_images_dir, exist_ok=True)
        
        # 사용 가능한 이미지 파일 목록 가져오기
        self.available_images = self._get_available_images()
        
        # 사이드바에 이미지 정보 표시
        self._show_image_info()
    
    def _get_available_images(self) -> List[str]:
        """사용 가능한 이미지 파일 목록 반환"""
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.webp']
        available_images = []
        
        for ext in image_extensions:
            pattern = os.path.join(self.extracted_images_dir, ext)
            available_images.extend(glob.glob(pattern))
            # 대문자 확장자도 체크
            pattern_upper = os.path.join(self.extracted_images_dir, ext.upper())
            available_images.extend(glob.glob(pattern_upper))
        
        # 파일명만 추출하여 반환
        return [os.path.basename(img) for img in available_images]
    
    def _show_image_info(self):
        """사이드바에 이미지 정보 표시"""
        with st.sidebar:
            st.subheader("📁 로컬 이미지 정보")
            st.write(f"📂 이미지 폴더: `{self.extracted_images_dir}`")
            st.write(f"🖼️ 발견된 이미지: {len(self.available_images)}개")
            
            if self.available_images:
                with st.expander("📋 이미지 목록"):
                    for i, img in enumerate(self.available_images, 1):
                        st.write(f"{i}. {img}")
            else:
                st.warning("⚠️ 이미지 파일이 없습니다!")
                st.info("이미지를 `data/images/extracted/` 폴더에 넣어주세요.")
    
    def render_scenes(self, scenes_data: List[Dict]):
        """여러 Scene들을 탭으로 렌더링"""
        if not scenes_data:
            st.warning("렌더링할 Scene이 없습니다.")
            return
        
        # 탭 이름 생성
        tab_names = []
        for i, scene in enumerate(scenes_data):
            timeframe = scene.get('timeFrame', {})
            start = timeframe.get('start', 0)
            end = timeframe.get('end', 5000)
            tab_names.append(f"Scene {i+1} ({start}~{end}ms)")
        
        # 탭 생성
        tabs = st.tabs(tab_names)
        
        # 각 탭에서 Scene 렌더링
        for i, (tab, scene) in enumerate(zip(tabs, scenes_data)):
            with tab:
                self._render_single_scene(scene, i+1)
    
    def _render_single_scene(self, scene: Dict, scene_number: int):
        """단일 Scene 렌더링"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"🎬 Scene {scene_number}")
            
            # TimeFrame 정보
            timeframe = scene.get('timeFrame', {})
            if timeframe:
                start = timeframe.get('start', 0)
                end = timeframe.get('end', 5000)
                duration = end - start
                st.info(f"⏱️ 재생 시간: {start}ms ~ {end}ms (지속시간: {duration}ms)")
            
            # HTML 렌더링
            try:
                scene_html = self._create_scene_html(scene)
                components.html(scene_html, height=2000, scrolling=True)
            except Exception as e:
                st.error(f"Scene 렌더링 오류: {e}")
                logger.error(f"Scene {scene_number} 렌더링 실패: {e}")
        
        with col2:
            self._render_scene_info(scene, scene_number)
    
    def _render_scene_info(self, scene: Dict, scene_number: int):
        """Scene 정보 패널"""
        st.subheader("📋 Scene 정보")
        
        # 요소 분석
        elements = scene.get("editorElements", [])
        element_stats = self._analyze_elements(elements)
        
        # 통계 표시
        col1, col2 = st.columns(2)
        with col1:
            st.metric("총 요소", len(elements))
        with col2:
            st.metric("이미지", element_stats['image_count'])
        
        st.metric("텍스트", element_stats['text_count'])
        
        # 이미지 요소 상세 정보
        with st.expander("📊 이미지 요소들"):
            for i, img_element in enumerate(element_stats['images']):
                st.write(f"**이미지 {i+1}**")
                src = img_element.get('properties', {}).get('src', 'N/A')
                st.write(f"원본 URL: `{src}`")
                
                # 로컬 이미지 매핑 확인
                local_path = self._resolve_local_image_path(src)
                if local_path:
                    st.write(f"로컬 파일: `{os.path.basename(local_path)}`")
                    try:
                        st.image(local_path, width=150, caption=f"이미지 {i+1}")
                    except Exception as e:
                        st.error(f"이미지 표시 실패: {e}")
                else:
                    st.warning("매칭되는 로컬 이미지를 찾을 수 없습니다.")
                
                placement = img_element.get('placement', {})
                st.write(f"위치: ({placement.get('x', 0)}, {placement.get('y', 0)})")
                st.write(f"크기: {placement.get('width', 0)}x{placement.get('height', 0)}")
                st.write("---")
        
        # 텍스트 요소 상세 정보
        with st.expander("📝 텍스트 요소들"):
            for i, text_element in enumerate(element_stats['texts']):
                st.write(f"**텍스트 {i+1}**")
                props = text_element.get('properties', {})
                text = props.get('text', '')
                
                # 텍스트 미리보기
                text_preview = text[:100] + "..." if len(text) > 100 else text
                st.write(f'"{text_preview}"')
                
                # 스타일 정보
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"크기: {props.get('fontSize', 'N/A')}px")
                    st.write(f"굵기: {props.get('fontWeight', 'N/A')}")
                with col2:
                    st.write(f"색상: {props.get('fontColor', 'N/A')}")
                    st.write(f"정렬: {props.get('textAlign', 'N/A')}")
                
                placement = text_element.get('placement', {})
                st.write(f"위치: ({placement.get('x', 0)}, {placement.get('y', 0)})")
                st.write("---")
        
        # JSON 다운로드
        st.download_button(
            label="📄 Scene JSON 다운로드",
            data=json.dumps(scene, ensure_ascii=False, indent=2),
            file_name=f"scene_{scene_number}.json",
            mime="application/json"
        )
    
    def _analyze_elements(self, elements: List[Dict]) -> Dict:
        """요소들 분석"""
        images = []
        texts = []
        
        for element in elements:
            elem_type = element.get('type', '')
            if elem_type == 'image':
                images.append(element)
            elif elem_type == 'text':
                texts.append(element)
        
        return {
            'image_count': len(images),
            'text_count': len(texts),
            'images': images,
            'texts': texts
        }
    
    def _resolve_local_image_path(self, src: str) -> Optional[str]:
        """로컬 이미지 경로 해결"""
        if not src:
            return None
        
        # URL에서 파일명 추출
        if src.startswith('http'):
            # URL에서 파일명 추출 (여러 방법 시도)
            filename_candidates = []
            
            # 1. URL 마지막 부분에서 파일명 추출
            url_parts = src.split('/')
            if url_parts:
                last_part = url_parts[-1]
                # 쿼리 파라미터 제거
                if '?' in last_part:
                    last_part = last_part.split('?')[0]
                if last_part and '.' in last_part:
                    filename_candidates.append(last_part)
            
            # 2. 일반적인 이미지 파일명 패턴 매칭
            for available_img in self.available_images:
                img_base = os.path.splitext(available_img)[0].lower()
                src_lower = src.lower()
                
                # 파일명이 URL에 포함되어 있는지 확인
                if img_base in src_lower or available_img.lower() in src_lower:
                    filename_candidates.append(available_img)
            
            # 3. 후보 중에서 실제 존재하는 파일 찾기
            for candidate in filename_candidates:
                full_path = os.path.join(self.extracted_images_dir, candidate)
                if os.path.exists(full_path):
                    return full_path
        
        # 로컬 파일 경로인 경우
        else:
            # 상대 경로 처리
            if 'extracted/' in src:
                filename = src.split('extracted/')[-1]
            else:
                filename = os.path.basename(src)
            
            full_path = os.path.join(self.extracted_images_dir, filename)
            if os.path.exists(full_path):
                return full_path
        
        # 매칭 실패 시 첫 번째 사용 가능한 이미지 반환 (데모용)
        if self.available_images:
            demo_path = os.path.join(self.extracted_images_dir, self.available_images[0])
            if os.path.exists(demo_path):
                st.info(f"🔄 대체 이미지 사용: {self.available_images[0]}")
                return demo_path
        
        return None
    
    def _create_scene_html(self, scene: Dict) -> str:
        """Scene HTML 생성"""
        elements_html = ""
        
        for element in scene.get("editorElements", []):
            element_html = self._create_element_html(element)
            if element_html:
                elements_html += element_html
        
        return self._wrap_in_frame(elements_html)
    
    def _create_element_html(self, element: Dict) -> str:
        """요소 HTML 생성"""
        elem_type = element.get("type", "")
        placement = element.get("placement", {})
        
        # 기본 스타일
        base_style = self._get_base_style(placement)
        
        if elem_type == "image":
            return self._create_image_html(element, base_style)
        elif elem_type == "text":
            return self._create_text_html(element, base_style)
        elif elem_type == "table":
            return self._create_table_html(element, base_style)
        else:
            logger.warning(f"알 수 없는 요소 타입: {elem_type}")
            return ""
    
    def _get_base_style(self, placement: Dict) -> str:
        """기본 배치 스타일 생성"""
        return f"""
            position: absolute;
            left: {placement.get('x', 0)}px;
            top: {placement.get('y', 0)}px;
            width: {placement.get('width', 100)}px;
            height: {placement.get('height', 100)}px;
            transform: scale({placement.get('scaleX', 1)}, {placement.get('scaleY', 1)});
            box-sizing: border-box;
        """
    
    def _create_image_html(self, element: Dict, base_style: str) -> str:
        """이미지 요소 HTML 생성"""
        properties = element.get("properties", {})
        src = properties.get("src", "")
        placement = element.get("placement", {})
        
        # 로컬 이미지 경로 해결
        local_image_path = self._resolve_local_image_path(src)
        
        if local_image_path and os.path.exists(local_image_path):
            # 로컬 이미지를 base64로 변환
            img_base64 = self._get_image_base64(local_image_path)
            if img_base64:
                # 파일 확장자에 따라 MIME 타입 결정
                file_ext = os.path.splitext(local_image_path)[1].lower()
                mime_type = {
                    '.jpg': 'jpeg', '.jpeg': 'jpeg',
                    '.png': 'png', '.gif': 'gif',
                    '.bmp': 'bmp', '.webp': 'webp'
                }.get(file_ext, 'jpeg')
                
                img_src = f"data:image/{mime_type};base64,{img_base64}"
            else:
                img_src = self._create_placeholder_image(
                    placement.get('width', 400), 
                    placement.get('height', 300), 
                    "인코딩 실패"
                )
        else:
            # 로컬 이미지를 찾을 수 없는 경우 플레이스홀더
            img_src = self._create_placeholder_image(
                placement.get('width', 400), 
                placement.get('height', 300), 
                "이미지 없음"
            )
        
        return f"""
        <img src="{img_src}" style="{base_style} 
            object-fit: cover; 
            border-radius: 8px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border: 1px solid #e0e0e0;" 
            alt="Scene Image" />
        """
    
    def _create_text_html(self, element: Dict, base_style: str) -> str:
        """텍스트 요소 HTML 생성"""
        properties = element.get("properties", {})
        
        # 텍스트 스타일
        text_style = f"""
            font-size: {properties.get('fontSize', 16)}px;
            font-weight: {properties.get('fontWeight', 400)};
            color: {properties.get('fontColor', '#333333')};
            background-color: {properties.get('backgroundColor', 'transparent')};
            text-align: {properties.get('textAlign', 'left')};
            line-height: {properties.get('lineHeight', 1.4)};
            padding: {properties.get('padding', 8)}px;
            font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            word-wrap: break-word;
            overflow-wrap: break-word;
            display: flex;
            align-items: center;
            justify-content: {self._get_text_justify(properties.get('textAlign', 'left'))};
            border-radius: 4px;
        """
        
        text_content = properties.get('text', '').replace('\n', '<br>')
        
        return f"""
        <div style="{base_style} {text_style}">
            <div style="width: 100%; height: 100%; display: flex; align-items: center;">
                {text_content}
            </div>
        </div>
        """
    
    def _create_table_html(self, element: Dict, base_style: str) -> str:
        """테이블 요소 HTML 생성"""
        properties = element.get("properties", {})
        table_data = properties.get("tableData", [])
        
        if not table_data:
            return f'<div style="{base_style}">테이블 데이터 없음</div>'
        
        table_style = """
            width: 100%;
            height: 100%;
            border-collapse: collapse;
            font-family: 'Noto Sans KR', sans-serif;
            font-size: 14px;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        """
        
        table_html = f'<table style="{table_style}">'
        
        for i, row in enumerate(table_data):
            row_style = "background-color: #f8f9fa;" if i % 2 == 0 else "background-color: white;"
            table_html += f'<tr style="{row_style}">'
            
            for j, cell in enumerate(row):
                cell_style = """
                    border: 1px solid #dee2e6;
                    padding: 12px 8px;
                    text-align: left;
                    vertical-align: top;
                """
                
                if i == 0:  # 헤더 행
                    cell_style += "font-weight: 600; background-color: #e9ecef;"
                
                if isinstance(cell, dict):
                    cell_text = str(cell.get('text', cell))
                else:
                    cell_text = str(cell) if cell else ""
                
                table_html += f'<td style="{cell_style}">{cell_text}</td>'
            
            table_html += '</tr>'
        
        table_html += '</table>'
        
        return f"""
        <div style="{base_style} overflow: auto; padding: 8px;">
            {table_html}
        </div>
        """
    
    def _wrap_in_frame(self, elements_html: str) -> str:
        """프레임으로 감싸기"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
            <style>
                .frame {{
                    position: relative;
                    width: 1080px;
                    height: 1920px;
                    border: 3px solid #007788;
                    margin: 0 auto;
                    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                    overflow: hidden;
                    border-radius: 16px;
                }}
                
                * {{
                    box-sizing: border-box;
                }}
                
                img {{
                    max-width: 100%;
                    max-height: 100%;
                }}
            </style>
        </head>
        <body style="margin: 0; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); font-family: 'Noto Sans KR', sans-serif;">
            <div class="frame">
                {elements_html}
            </div>
            <div style="text-align: center; margin-top: 20px; color: #666; font-size: 14px;">
                🎨 Local PDF to JSON Converter
            </div>
        </body>
        </html>
        """
    
    def _get_image_base64(self, image_path: str) -> Optional[str]:
        """이미지를 base64로 인코딩"""
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception as e:
            logger.error(f"이미지 base64 인코딩 실패: {e}")
            return None
    
    def _create_placeholder_image(self, width: int = 400, height: int = 300, text: str = "이미지 없음") -> str:
        """플레이스홀더 이미지 생성"""
        try:
            # PIL로 이미지 생성
            img = Image.new('RGB', (width, height), color='#f0f0f0')
            draw = ImageDraw.Draw(img)
            
            # 테두리 그리기
            draw.rectangle([0, 0, width-1, height-1], outline='#cccccc', width=2)
            
            # 대각선 그리기
            draw.line([0, 0, width, height], fill='#dddddd', width=1)
            draw.line([width, 0, 0, height], fill='#dddddd', width=1)
            
            # 텍스트 추가
            try:
                font = ImageFont.truetype("malgun.ttf", 16)  # Windows
            except:
                try:
                    font = ImageFont.truetype("AppleGothic.ttf", 16)  # macOS
                except:
                    font = ImageFont.load_default()
            
            # 텍스트 위치 계산
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            draw.text((x, y), text, fill='#999999', font=font)
            
            # base64로 변환
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
            
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            logger.error(f"플레이스홀더 이미지 생성 실패: {e}")
            return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIiBzdHJva2U9IiNjY2MiIHN0cm9rZS13aWR0aD0iMiIgcng9IjgiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE2IiBmaWxsPSIjOTk5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+7J207a+867KM7KeAIOydtOuvuOyngDwvdGV4dD48L3N2Zz4="
    
    def _get_text_justify(self, align: str) -> str:
        """텍스트 정렬을 justify 속성으로 변환"""
        align_map = {
            'left': 'flex-start',
            'center': 'center', 
            'right': 'flex-end'
        }
        return align_map.get(align, 'flex-start')