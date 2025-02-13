from google import genai
import json
from typing import Dict, Any, Optional, Union
from pathlib import Path
import re
from ..error.exceptions import APIError, ValidationError
from .base import BaseClassifier
from ..config.settings import Settings


class GeminiClassifier(BaseClassifier):
    def __init__(self, settings: Optional[Union[Settings, dict]] = None):
        """
        Initialize Gemini classifier with optional settings.

        Args:
            settings: Optional Settings instance or dictionary of settings
        """
        try:
            if isinstance(settings, dict):
                settings = Settings.from_dict(settings)
            elif settings is None:
                settings = Settings()

            super().__init__(settings)
            self.client = genai.Client(api_key=self.settings.GEMINI_API_KEY)
            self.prompt_text = self._create_prompt()

        except ValueError as e:
            raise ValueError(str(e)) from e

    def _create_prompt(self) -> str:
        """Create the prompt for the Gemini API."""
        return f"""
        Analyze the clothing item in the image and classify it according to these rules.
        You must return a valid JSON object with exactly these keys and valid values:
        - 'color': Primary color as a HEX code (e.g. #FF0000)
        - 'category': One value from this list: {self.category_values}
        - 'dresscode': One value from this list: {self.dresscode_values}
        - 'season': Array of one or more values from this list: {self.season_values}
        
        Ensure your response is only the JSON object, with no additional text.
        """

    async def classify_single(self, image_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Classify a single clothing item using Gemini Vision API.

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary containing classification results
        """
        try:
            self.image_processor.check_image_file(str(image_path))

            image = self.image_processor.load_image(str(image_path))

            response = self.client.models.generate_content(
                model=self.settings.GEMINI_MODEL,
                contents=[
                    self.prompt_text,
                    image
                ]
            )

            try:
                result = self._parse_json_from_gemini(response.text)
            except json.JSONDecodeError:
                raise APIError("Failed to parse JSON response from Gemini API")

            self._validate_response(result)

            return {
                "image_path": str(image_path),
                **result
            }

        except Exception as e:
            raise APIError(f"Error classifying image with Gemini: {str(e)}")

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

        # Validate color format (HEX code)
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
    def create(cls, settings_dict: dict) -> 'GeminiClassifier':
        """
        Create a classifier instance from a dictionary of settings.

        Args:
            settings_dict: Dictionary containing settings

        Returns:
            GeminiClassifier instance
        """
        return cls(settings=settings_dict)

    def _parse_json_from_gemini(self, json_str: str):
        """Parses a dictionary from a JSON-like object string.

        Args:
        json_str: A string representing a JSON-like object, e.g.:
            ```json
            {
            "key1": "value1",
            "key2": "value2"
            }
            ```

        Returns:
        A dictionary representing the parsed object, or None if parsing fails.
        """

        try:
            # Remove potential leading/trailing whitespace
            json_str = json_str.strip()

            # Extract JSON content from triple backticks and "json" language specifier
            json_match = re.search(
                r"```json\s*(.*?)\s*```", json_str, re.DOTALL)

            if json_match:
                json_str = json_match.group(1)

            return json.loads(json_str)
        except (json.JSONDecodeError, AttributeError):
            return None
