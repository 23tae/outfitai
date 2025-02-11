import openai
import json
from typing import Dict, List, Any, Optional, Union
import asyncio
from pathlib import Path
from ..error.exceptions import APIError, ValidationError
from ..utils.logger import Logger
from ..utils.utils import ImageProcessor
from ..config.settings import Settings


class OpenAIClassifier:
    def __init__(self, settings: Optional[Union[Settings, dict]] = None):
        """
        Initialize OpenAI classifier with optional settings.

        Args:
            settings: Optional Settings instance or dictionary of settings
        """
        try:
            if isinstance(settings, dict):
                self.settings = Settings.from_dict(settings)
            elif isinstance(settings, Settings):
                self.settings = settings
            else:
                self.settings = Settings()
        except ValueError as e:
            raise ValueError(str(e)) from e

        logger_manager = Logger(self.settings)
        self.logger = logger_manager.setup_logger(__name__)
        self.client = openai.AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.image_processor = ImageProcessor(self.settings)
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

    async def classify_single(self, image_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Classify a single clothing item.

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary containing classification results
        """
        try:
            self.image_processor.check_image_file(str(image_path))
            encoded_image = self.image_processor.encode_image(str(image_path))

            response = await self.client.chat.completions.create(
                model=self.settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.prompt_text},
                            {
                                "type": "image_url",
                                "image_url":
                                {
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
        image_paths: Union[str, Path, List[Union[str, Path]]],
        batch_size: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Classify multiple clothing items in batches.

        Args:
            image_paths: Directory path or list of image paths
            batch_size: Optional batch size for processing

        Returns:
            List of dictionaries containing classification results
        """
        batch_size = batch_size or self.settings.BATCH_SIZE

        # Handle directory input
        if isinstance(image_paths, (str, Path)):
            path = Path(image_paths)
            if path.is_dir():
                image_paths = [
                    p for p in path.glob("*")
                    if p.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', 'gif']
                ]
            else:
                raise ValueError(
                    "When providing a single path, it must be a directory")

        image_paths = [str(path) for path in image_paths]
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

    @classmethod
    def create(cls, settings_dict: dict) -> 'OpenAIClassifier':
        """
        Create a classifier instance from a dictionary of settings.

        Args:
            settings_dict: Dictionary containing settings

        Returns:
            OpenAIClassifier instance
        """
        return cls(settings=settings_dict)
