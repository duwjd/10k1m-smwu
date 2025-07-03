import os
from dotenv import load_dotenv
from pathlib import Path

# .env 파일 로드
load_dotenv()

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent

# API 설정
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# 경로 설정
DATA_DIR = PROJECT_ROOT / 'data'
IMAGES_DIR = DATA_DIR / 'images'
OUTPUT_DIR = DATA_DIR / 'output'
INPUT_DIR = DATA_DIR / 'input'

# 문자열로 변환 (호환성)
DATA_DIR = str(DATA_DIR)
IMAGES_DIR = str(IMAGES_DIR)
OUTPUT_DIR = str(OUTPUT_DIR)
INPUT_DIR = str(INPUT_DIR)
PROJECT_ROOT = str(PROJECT_ROOT)

# 앱 설정
STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', 8501))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
MAX_FILE_SIZE = os.getenv('MAX_FILE_SIZE', '50MB')

# 처리 설정
IMAGE_RESOLUTION_SCALE = int(os.getenv('IMAGE_RESOLUTION_SCALE', 3))
OCR_ENHANCEMENT = os.getenv('OCR_ENHANCEMENT', 'True').lower() == 'true'
COLOR_PALETTE_SIZE = int(os.getenv('COLOR_PALETTE_SIZE', 5))
