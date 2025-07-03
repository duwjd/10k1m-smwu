"""
로컬 환경용 Streamlit 메인 앱
"""
import streamlit as st
import sys
import os
import json
import logging
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from config.settings import *
    from src.pdf_processor import EnhancedPDFProcessor, get_available_pdfs, get_generated_jsons
    from streamlit_app.components.scene_renderer import SceneRenderer
    from streamlit_app.components.file_uploader import FileUploader
    from streamlit_app.components.json_validator import JSONValidator
except ImportError as e:
    st.error(f"모듈 import 실패: {e}")
    st.info("프로젝트 구조를 확인하고 필요한 패키지가 설치되었는지 확인해주세요.")
    st.stop()

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Enhanced PDF to JSON Converter",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🎨 Enhanced PDF to JSON Converter")
    st.markdown("### AI 기반 PDF → JSON 템플릿 변환기")
    
    # 사이드바
    with st.sidebar:
        st.header("🔧 설정")
        mode = st.radio("모드 선택", ["📁 파일 업로드", "📂 로컬 파일", "📋 JSON 뷰어"])
    
    # 메인 컨텐츠
    if mode == "📁 파일 업로드":
        uploaded_file = st.file_uploader("PDF 파일 업로드", type=['pdf'])
        if uploaded_file and st.button("처리 시작"):
            with st.spinner("처리 중..."):
                # 임시 저장 후 처리
                temp_path = os.path.join(INPUT_DIR, uploaded_file.name)
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                processor = EnhancedPDFProcessor()
                output_path, result = processor.process_pdf(temp_path)
                
                if output_path:
                    st.success("처리 완료!")
                    st.json(json.loads(result))
    
    elif mode == "📂 로컬 파일":
        pdfs = get_available_pdfs()
        if pdfs:
            selected = st.selectbox("PDF 선택", pdfs)
            if st.button("처리 시작"):
                processor = EnhancedPDFProcessor()
                pdf_path = os.path.join(INPUT_DIR, selected)
                output_path, result = processor.process_pdf(pdf_path)
                if output_path:
                    st.success("처리 완료!")
        else:
            st.info("data/input 폴더에 PDF 파일을 넣어주세요.")
    
    elif mode == "📋 JSON 뷰어":
        jsons = get_generated_jsons()
        if jsons:
            selected = st.selectbox("JSON 선택", jsons)
            if selected:
                json_path = os.path.join(OUTPUT_DIR, selected)
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                renderer = SceneRenderer(IMAGES_DIR)
                renderer.render_scenes(data if isinstance(data, list) else [data])
        else:
            st.info("생성된 JSON 파일이 없습니다.")

if __name__ == "__main__":
    main()
