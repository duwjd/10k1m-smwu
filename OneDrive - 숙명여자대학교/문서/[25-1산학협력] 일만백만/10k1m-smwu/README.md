# PDF to JSON Converter

🎨 AI 기반 PDF → JSON 템플릿 변환기

## 🚀 빠른 시작

### 1. 설치
```bash
cd web
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/setup.py
```

### 2. 설정
```bash
# .env 파일 설정
cp .env.example .env
# .env 파일을 열어서 실제 API 키들 입력

# Google Vision API 키 배치
# google_vision_key.json을 config/ 폴더에 복사
```

### 3. 실행
```bash
# PDF 처리
python scripts/run_processor.py data/input/your_file.pdf

# Streamlit 앱
python scripts/run_streamlit.py
```


## 📁 프로젝트 구조

```
web/
├── config/          # 설정
├── src/            # 소스 코드
├── streamlit_app/  # 웹 앱
├── data/           # 데이터
└── scripts/        # 실행 스크립트
```
