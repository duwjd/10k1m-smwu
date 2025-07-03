#!/usr/bin/env python3
"""Streamlit 앱 실행"""
import subprocess
import sys
from pathlib import Path

def main():
    project_root = Path(__file__).parent.parent
    app_path = project_root / 'streamlit_app' / 'main.py'
    
    print("🚀 Streamlit 앱 시작...")
    print("🌐 브라우저에서 http://localhost:8501 접속")
    
    cmd = ['streamlit', 'run', str(app_path), '--server.port', '8501']
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
