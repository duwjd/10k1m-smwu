"""파일 업로드 컴포넌트"""
import streamlit as st

class FileUploader:
    def render(self):
        return st.file_uploader("JSON 파일 업로드", type=["json"])
