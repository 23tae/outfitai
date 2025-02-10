import openai
import json
from typing import Dict, List, Any, Optional
import asyncio
from ..error.exceptions import APIError, ValidationError
from ..utils.logger import setup_logger
from ..utils.utils import ImageProcessor
from ..config.settings import get_settings


class OpenAIClassifier:
    def __init__(self):
        self.settings = get_settings()
        self.logger = setup_logger(__name__)
        self.client = openai.AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.image_processor = ImageProcessor()
        self._init_constants()

    def _init_constants(self):
        """Initialize constant values used in classification."""
        self.category_values = [
            "top", "bottom", "outer", "dress",
            "footwear", "bag", "accessory", "other"
        ]
        self.dresscode_values = [
            "casual", "business", "party",
            "sports", "formal", "other"
        ]
        self.season_values = ["spring", "summer", "fall", "winter"]
        self.prompt_text = self._create_prompt()

    def _create_prompt(self) -> str:
        """Create the prompt for the OpenAI API."""
        return f"""
        Analyze the clothing item in the image and classify it according to these rules.
        Return a JSON object with these keys:
        - 'color': Primary color as a HEX code (e.g. #FF0000)
        - 'category': 1 value from {self.category_values}
        - 'dresscode': 1 value from {self.dresscode_values}
        - 'season': 1+ values from {self.season_values} (array)
        """

    async def classify_single(self, image_path: str) -> Dict[str, Any]:
        """Classify a single clothing item."""
        try:
            processed_path = await self.image_processor.process_image(image_path)
            encoded_image = self.image_processor.encode_image(processed_path)

            response = await self.client.chat.completions.create(
                model=self.settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}",
                                    "detail": "low"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=self.settings.OPENAI_MAX_TOKENS,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            self._validate_response(result)
            return result

        except Exception as e:
            raise APIError(f"Error classifying image: {str(e)}")

    async def classify_batch(
        self,
        image_paths: List[str],
        batch_size: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Classify multiple clothing items in batches."""
        batch_size = batch_size or self.settings.BATCH_SIZE
        results = []

        for i in range(0, len(image_paths), batch_size):
            batch = image_paths[i:i + batch_size]
            tasks = [self.classify_single(path) for path in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in batch_results:
                if isinstance(result, Exception):
                    self.logger.error(
                        f"Error in batch processing: {str(result)}")
                    results.append({"error": str(result)})
                else:
                    results.append(result)

        return results

    def _validate_response(self, data: Dict[str, Any]):
        """Validate the API response format and values."""
        required_keys = ["color", "category", "dresscode", "season"]

        # Check required keys
        for key in required_keys:
            if key not in data:
                raise ValidationError(f"Missing required key: {key}")

        # Validate color format
        if not isinstance(data["color"], str) or not data["color"].startswith("#"):
            raise ValidationError("Invalid color format")

        # Validate category
        if data["category"] not in self.category_values:
            raise ValidationError(f"Invalid category: {data['category']}")

        # Validate dresscode
        if data["dresscode"] not in self.dresscode_values:
            raise ValidationError(f"Invalid dresscode: {data['dresscode']}")

        # Validate seasons
        if not isinstance(data["season"], list):
            raise ValidationError("Season must be a list")

        for season in data["season"]:
            if season not in self.season_values:
                raise ValidationError(f"Invalid season: {season}")
