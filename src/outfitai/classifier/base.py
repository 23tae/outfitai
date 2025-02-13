from abc import ABC, abstractmethod
from typing import Dict, List, Any, Union
from pathlib import Path
import asyncio
from ..config.settings import Settings
from ..utils.logger import Logger
from ..utils.image_processor import ImageProcessor


class BaseClassifier(ABC):
    """Base class for all image classifiers."""

    def __init__(self, settings: Settings):
        """
        Initialize the base classifier.

        Args:
            settings: Settings instance containing configuration
        """
        self.settings = settings
        logger_manager = Logger(self.settings)
        self.logger = logger_manager.setup_logger(__name__)
        self.image_processor = ImageProcessor(self.settings)
        self._init_constants()

    def _init_constants(self):
        """Initialize constant values used in classification."""
        self.category_values = [
            "top", "bottom", "outer", "dress",
            "footwear", "bag", "accessory", "other"
        ]
        self.dresscode_values = [
            "casual", "business casual", "campus", "date night attire",
            "travel wear", "formal", "loungewear", "beachwear", "other"
        ]
        self.season_values = ["spring", "summer", "fall", "winter"]

    @abstractmethod
    async def classify_single(self, image_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Classify a single clothing item.

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary containing classification results
        """
        pass

    async def classify_batch(
        self,
        image_paths: Union[str, Path, List[Union[str, Path]]],
        batch_size: int = None
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

    @abstractmethod
    def _validate_response(self, data: Dict[str, Any]) -> None:
        """
        Validate the API response format and values.

        Args:
            data: Response data to validate

        Raises:
            ValidationError: If the response format is invalid
        """
        pass

    @abstractmethod
    def _create_prompt(self) -> str:
        """
        Create the prompt for the API.

        Returns:
            String containing the prompt
        """
        pass
