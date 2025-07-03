"""JSON 검증 컴포넌트"""
import streamlit as st
import json

class JSONValidator:
    def validate(self, uploaded_file):
        try:
            return json.load(uploaded_file)
        except:
            st.error("JSON 파싱 실패")
            return None
    
    def validate_data(self, data):
        return [data] if isinstance(data, dict) else data
