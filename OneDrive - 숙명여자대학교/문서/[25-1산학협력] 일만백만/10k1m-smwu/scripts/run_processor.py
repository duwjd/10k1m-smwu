#!/usr/bin/env python3
"""PDF 처리 실행 스크립트"""
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.pdf_processor import process_pdf_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/run_processor.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    if not os.path.exists(pdf_file):
        print(f"❌ 파일을 찾을 수 없습니다: {pdf_file}")
        sys.exit(1)
    
    print(f"🚀 PDF 처리 시작: {pdf_file}")
    output_path, result_json = process_pdf_file(pdf_file)
    
    if output_path:
        print(f"✅ 처리 완료: {output_path}")
    else:
        print("❌ 처리 실패")

if __name__ == "__main__":
    main()
