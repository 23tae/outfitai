import openai
import json
from typing import Dict, Any, Optional, Union
from pathlib import Path
from ..error.exceptions import APIError, ValidationError
from .base import BaseClassifier
from ..config.settings import Settings


class OpenAIClassifier(BaseClassifier):
    def __init__(self, settings: Optional[Union[Settings, dict]] = None):
        """
        Initialize OpenAI classifier with optional settings.

        Args:
            settings: Optional Settings instance or dictionary of settings
        """
        try:
            if isinstance(settings, dict):
                settings = Settings.from_dict(settings)
            elif settings is None:
                settings = Settings()

            super().__init__(settings)
            self.client = openai.AsyncOpenAI(
                api_key=self.settings.OPENAI_API_KEY)
            self.prompt_text = self._create_prompt()

        except ValueError as e:
            raise ValueError(str(e)) from e

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
                                "text": self.prompt_text
                            },
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

            return {
                "image_path": str(image_path),
                **result
            }

        except Exception as e:
            raise APIError(f"Error classifying image: {str(e)}")

    def _validate_response(self, data: Dict[str, Any]) -> None:
        """
        Validate the API response format and values.

        Args:
            data: Response data to validate

        Raises:
            ValidationError: If the response format is invalid
        """
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
