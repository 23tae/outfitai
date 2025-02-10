import openai
from PIL import Image
import json
from config import OpenAIConfig
from utils import encode_image


class ClothingClassifier:
    def __init__(self):
        self.client = openai.OpenAI(api_key=OpenAIConfig.API_KEY)
        self._init_constants()

    def _init_constants(self):
        self.category_values = ["top", "bottom", "outer",
                                "dress", "footwear", "bag", "accessory", "other"]
        self.dresscode_values = ["casual", "business",
                                 "party", "sports", "formal", "other"]
        self.season_values = ["spring", "summer", "fall", "winter"]
        self.prompt_text = self._create_prompt()

    def _create_prompt(self):
        return f"""
        Analyze the clothing item in the image and classify it according to these rules.
        Return a JSON object with these keys:
        - 'color': Primary color as a HEX code (e.g. #FF0000)
        - 'category': 1 values from {self.category_values}
        - 'dresscode': 1 values from {self.dresscode_values}
        - 'season': 1+ values from {self.season_values} (array)

        Example:
        {{
            "color": "#FF0000",
            "category": "outer",
            "dresscode": "formal",
            "season": ["fall", "winter"]
        }}
        """

    def classify_clothes(self, image_path):
        """
        옷 사진을 입력받아 OpenAI API를 사용하여 JSON 형식으로 분류 결과를 반환한다.
        """

        try:
            img = Image.open(image_path)
            img_base64 = encode_image(image_path)

            response = openai.chat.completions.create(
                model=OpenAIConfig.MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/{img.format.lower()};base64,{img_base64}",
                                    "detail": "low"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
                response_format={"type": "json_object"}  # JSON 형식 응답 지정
            )

            json_answer = response.choices[0].message.content

            try:
                data = json.loads(json_answer)

                # 필수 키 검증
                required_keys = ["color", "category", "dresscode", "season"]
                if not all(key in data for key in required_keys):
                    return f"Missing required keys. Expected: {required_keys}"

                # 타입 검증
                type_checks = [
                    ("color", str),
                    ("category", str),
                    ("dresscode", str),
                    ("season", list)
                ]

                for key, expected_type in type_checks:
                    if not isinstance(data[key], expected_type):
                        return f"'{key}' must be {expected_type.__name__}"

                # 값 유효성 검사
                validations = [
                    ("category", self.category_values),
                    ("dresscode", self.dresscode_values),
                    ("season", self.season_values)
                ]

                for key, allowed_values in validations:
                    if isinstance(data[key], list):  # 리스트인 경우
                        for value in data[key]:
                            if value not in allowed_values:
                                return f"Invalid {key} value: {value}. Allowed: {allowed_values}"
                    else:  # 단일 값인 경우
                        if data[key] not in allowed_values:
                            return f"Invalid {key} value: {data[key]}. Allowed: {allowed_values}"

                return json.dumps(data, indent=2)

            except json.JSONDecodeError as e:
                return f"JSON Decode Error: {str(e)}\nResponse: {json_answer}"

        except Exception as e:
            return f"Error: {str(e)}"
