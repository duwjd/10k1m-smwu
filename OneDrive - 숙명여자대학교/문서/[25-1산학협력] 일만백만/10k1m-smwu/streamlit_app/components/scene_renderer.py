"""
업데이트된 Scene Renderer - 추출된 이미지들 지원
streamlit_app/components/scene_renderer.py 파일을 이 내용으로 교체하세요
"""

import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import json
from typing import List, Dict, Optional
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)

class SceneRenderer:
    """향상된 Scene HTML 렌더러 - 추출된 이미지 지원"""
    
    def __init__(self, images_dir: str):
        self.images_dir = images_dir
        self.extracted_images_dir = os.path.join(images_dir, "extracted")
    
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
                scene_html = self._create_enhanced_scene_html(scene)
                components.html(scene_html, height=2000, scrolling=True)
            except Exception as e:
                st.error(f"Scene 렌더링 오류: {e}")
                logger.error(f"Scene {scene_number} 렌더링 실패: {e}")
        
        with col2:
            self._render_enhanced_scene_info(scene, scene_number)
    
    def _render_enhanced_scene_info(self, scene: Dict, scene_number: int):
        """향상된 Scene 정보 패널"""
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
        
        # 요소별 상세 정보
        with st.expander("📊 이미지 요소들"):
            for i, img_element in enumerate(element_stats['images']):
                st.write(f"**이미지 {i+1}**")
                src = img_element.get('properties', {}).get('src', 'N/A')
                st.write(f"파일: `{src}`")
                
                # 이미지 미리보기
                if src and src != 'N/A':
                    img_path = self._resolve_image_path(src)
                    if img_path and os.path.exists(img_path):
                        try:
                            st.image(img_path, width=150, caption=src)
                        except Exception as e:
                            st.error(f"이미지 로드 실패: {e}")
                    else:
                        st.warning(f"이미지 파일을 찾을 수 없음: {src}")
                
                placement = img_element.get('placement', {})
                st.write(f"위치: ({placement.get('x', 0)}, {placement.get('y', 0)})")
                st.write(f"크기: {placement.get('width', 0)}x{placement.get('height', 0)}")
                st.write("---")
        
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
    
    def _resolve_image_path(self, src: str) -> Optional[str]:
        """이미지 경로 해결"""
        if not src:
            return None
        
        # URL인 경우
        if src.startswith('http'):
            return src
        
        # 상대 경로 처리
        if src.startswith('extracted/'):
            # 추출된 이미지
            filename = src.replace('extracted/', '')
            return os.path.join(self.extracted_images_dir, filename)
        else:
            # 일반 이미지 (배경 등)
            return os.path.join(self.images_dir, src)
    
    def _create_enhanced_scene_html(self, scene: Dict) -> str:
        """향상된 Scene HTML 생성"""
        elements_html = ""
        
        for element in scene.get("editorElements", []):
            element_html = self._create_enhanced_element_html(element)
            if element_html:
                elements_html += element_html
        
        return self._wrap_in_enhanced_frame(elements_html)
    
    def _create_enhanced_element_html(self, element: Dict) -> str:
        """향상된 요소 HTML 생성"""
        elem_type = element.get("type", "")
        placement = element.get("placement", {})
        
        # 기본 스타일
        base_style = self._get_base_style(placement)
        
        if elem_type == "image":
            return self._create_enhanced_image_html(element, base_style)
        elif elem_type == "text":
            return self._create_enhanced_text_html(element, base_style)
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
    
    def _create_enhanced_image_html(self, element: Dict, base_style: str) -> str:
        """향상된 이미지 요소 HTML 생성"""
        properties = element.get("properties", {})
        src = properties.get("src", "")
        
        # 이미지 소스 처리
        img_src = self._process_image_source(src)
        
        return f"""
        <img src="{img_src}" style="{base_style} 
            object-fit: cover; 
            border-radius: 8px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border: 1px solid #e0e0e0;" 
            alt="Scene Image" />
        """
    
    def _process_image_source(self, src: str) -> str:
        """이미지 소스 처리"""
        if not src:
            return self._get_placeholder_image()
        
        # URL인 경우 그대로 사용
        if src.startswith("http"):
            return src
        
        # 로컬 파일 처리
        img_path = self._resolve_image_path(src)
        if img_path and os.path.exists(img_path):
            img_base64 = self._get_image_base64(img_path)
            if img_base64:
                return f"data:image/png;base64,{img_base64}"
        
        # 실패 시 플레이스홀더
        return self._get_placeholder_image()
    
    def _create_enhanced_text_html(self, element: Dict, base_style: str) -> str:
        """향상된 텍스트 요소 HTML 생성"""
        properties = element.get("properties", {})
        
        # 텍스트 스타일 개선
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
            text-shadow: 0 1px 2px rgba(0,0,0,0.05);
        """
        
        # 제목인 경우 강조 효과
        if properties.get('fontSize', 16) >= 40:
            text_style += """
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                font-weight: bold;
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
    
    def _wrap_in_enhanced_frame(self, elements_html: str) -> str:
        """향상된 프레임으로 감싸기"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
            <style>
                .enhanced-frame {{
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
                
                .element-overlay {{
                    transition: all 0.3s ease;
                }}
                
                .element-overlay:hover {{
                    transform: scale(1.02);
                    z-index: 100;
                }}
            </style>
        </head>
        <body style="margin: 0; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); font-family: 'Noto Sans KR', sans-serif;">
            <div class="enhanced-frame">
                {elements_html}
            </div>
            <div style="text-align: center; margin-top: 20px; color: #666; font-size: 14px;">
                🎨 Enhanced PDF to JSON Converter
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
    
    def _get_placeholder_image(self) -> str:
        """향상된 플레이스홀더 이미지 SVG"""
        return """data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImdyYWQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPjxzdG9wIG9mZnNldD0iMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiNmMGYwZjA7c3RvcC1vcGFjaXR5OjEiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjojZTBlMGUwO3N0b3Atb3BhY2l0eToxIiAvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JhZCkiIHN0cm9rZT0iI2NjYyIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtZGFzaGFycmF5PSI1LDUiIHJ4PSI4Ii8+PGNpcmNsZSBjeD0iMjAwIiBjeT0iMTIwIiByPSIyMCIgZmlsbD0iI2JiYiIvPjx0ZXh0IHg9IjUwJSIgeT0iNjAlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IiM5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7snbTrr7jsp4Ag7JeG7J2M7J6QPC90ZXh0Pjwvc3ZnPg=="""
    
    def _get_text_justify(self, align: str) -> str:
        """텍스트 정렬을 justify 속성으로 변환"""
        align_map = {
            'left': 'flex-start',
            'center': 'center', 
            'right': 'flex-end'
        }
        return align_map.get(align, 'flex-start')