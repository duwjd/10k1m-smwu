"""
색상 추출 유틸리티
"""
from PIL import Image
import numpy as np
import io
from typing import List
import logging

logger = logging.getLogger(__name__)

class ColorExtractor:
    def extract_dominant_colors(self, image_bytes: bytes, n_colors: int = 3) -> List[str]:
        """주요 색상 추출"""
        try:
            pil_image = Image.open(io.BytesIO(image_bytes))
            pil_image = pil_image.convert('RGB')
            pil_image = pil_image.resize((150, 150))
            
            img_array = np.array(pil_image)
            img_array = img_array.reshape(-1, 3)
            
            colors = []
            for i in range(n_colors):
                sample_idx = np.random.choice(len(img_array), size=min(1000, len(img_array)), replace=False)
                sample_colors = img_array[sample_idx]
                avg_color = np.mean(sample_colors, axis=0).astype(int)
                hex_color = f"#{avg_color[0]:02x}{avg_color[1]:02x}{avg_color[2]:02x}"
                colors.append(hex_color)
            
            return colors
            
        except Exception as e:
            logger.error(f"색상 추출 실패: {e}")
            return ["#333333", "#666666", "#999999"]
