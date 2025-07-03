#!/usr/bin/env python3
"""프로젝트 초기 설정"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config.settings import *

def setup_project():
    print("🔧 프로젝트 설정 중...")
    
    directories = [DATA_DIR, IMAGES_DIR, OUTPUT_DIR, INPUT_DIR, 
                  os.path.join(PROJECT_ROOT, 'logs')]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ 디렉토리 생성: {directory}")
    
    print("🎉 설정 완료!")

if __name__ == "__main__":
    setup_project()
