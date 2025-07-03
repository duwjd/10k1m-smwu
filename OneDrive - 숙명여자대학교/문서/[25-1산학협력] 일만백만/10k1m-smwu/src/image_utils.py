"""
이미지 처리 유틸리티
"""
from PIL import Image, ImageEnhance
import io

class ImageProcessor:
    def enhance_for_ocr(self, image_bytes: bytes) -> bytes:
        """OCR을 위한 이미지 향상"""
        try:
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            # 크기 조정
            width, height = pil_image.size
            if width < 1000 or height < 1000:
                scale_factor = max(1000/width, 1000/height)
                new_size = (int(width * scale_factor), int(height * scale_factor))
                pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)
            
            # 대비 향상
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.2)
            
            # 선명도 향상
            enhancer = ImageEnhance.Sharpness(pil_image)
            pil_image = enhancer.enhance(1.1)
            
            # bytes로 변환
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
            
        except Exception:
            return image_bytes
