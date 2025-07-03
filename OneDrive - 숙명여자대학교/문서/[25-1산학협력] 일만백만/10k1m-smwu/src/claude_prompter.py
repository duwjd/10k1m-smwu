"""
Claude 프롬프트 생성기
"""
from typing import List, Dict

class ClaudePrompter:
    def create_enhanced_prompt(self, scene_data_list: List[Dict], all_colors: List[str]) -> str:
        """향상된 프롬프트 생성"""
        color_palette = ", ".join(list(set(all_colors))[:5])
        
        prompt = f"""
당신은 전문적인 UI/UX 디자이너입니다. 다음 정보를 바탕으로 시각적으로 매력적이고 조화로운 JSON 템플릿을 생성해주세요.

【추출된 주요 색상】: {color_palette}

【디자인 원칙】:
1. 타이포그래피 계층구조 (제목: 48-72px, 본문: 18-28px)
2. 색상 조화
3. 레이아웃 균형

각 scene 구조:
- timeFrame: start, end
- editorElements: image + text 요소들

【데이터】:
"""
        
        for i, scene_data in enumerate(scene_data_list):
            scene_start = i * 5000
            scene_end = (i + 1) * 5000
            
            prompt += f"""
Scene {i+1} (TimeFrame: {scene_start}-{scene_end}ms):
이미지: {scene_data.get('image_filename', 'N/A')}
텍스트 요소들:
"""
            
            for j, text_item in enumerate(scene_data.get('text_data', [])):
                prompt += f"- {text_item['text'][:50]}...\n"
        
        prompt += "완전한 JSON 배열을 생성해주세요. JSON만 응답하세요."
        return prompt