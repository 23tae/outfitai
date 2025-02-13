from PIL import Image, UnidentifiedImageError, ImageFile
from pathlib import Path
import base64
from typing import Optional, Set, Final
from functools import lru_cache
from ..error.exceptions import ImageProcessingError
from ..config.settings import Settings
from .logger import Logger


class ImageProcessor:
    SUPPORTED_EXTENSIONS: Final[Set[str]] = {
        ".png", ".jpeg", ".jpg", ".webp", ".gif"}

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.logger = Logger(self.settings).setup_logger(__name__)

    def check_image_file(self, image_path: str | Path) -> None:
        """
        Validates if the image file is supported and can be processed.

        Args:
            image_path: Path to the image file

        Raises:
            ImageProcessingError: If image validation fails
        """
        image_path = Path(image_path)
        if not self._is_supported_extension(image_path):
            raise ImageProcessingError("File extension not supported")

        if self._is_animated_gif(image_path):
            raise ImageProcessingError("Animated GIF not supported")

        try:
            self.load_image(image_path)
        except Exception as e:
            if isinstance(e, UnidentifiedImageError):
                raise ImageProcessingError("Failed to identify image file")
            raise ImageProcessingError(f"Failed to process image: {str(e)}")

    @lru_cache(maxsize=20)
    def encode_image(self, image_path: str | Path) -> str:
        """
        Encodes image to base64 string with caching.

        Args:
            image_path: Path to the image file

        Returns:
            Base64 encoded string of the image

        Raises:
            ImageProcessingError: If encoding fails
        """
        try:
            image_path = Path(image_path)
            return base64.b64encode(image_path.read_bytes()).decode("utf-8")
        except Exception as e:
            raise ImageProcessingError(f"Failed to encode image: {str(e)}")

    @lru_cache(maxsize=10)
    def load_image(self, image_path: str | Path) -> ImageFile:
        """
        Loads and returns a copy of the image with caching.

        Args:
            image_path: Path to the image file

        Returns:
            Copy of the loaded image

        Raises:
            ImageProcessingError: If image loading fails
        """
        try:
            with Image.open(image_path) as img:
                return img.copy()
        except Exception as e:
            raise ImageProcessingError(f"Failed to load image: {str(e)}")

    def _is_supported_extension(self, image_path: Path) -> bool:
        """Checks if the image file extension is supported."""
        extension = image_path.suffix.lower()
        if extension == ".gif" and not self.settings.OUTFITAI_PROVIDER == "openai":
            return False
        return extension in self.SUPPORTED_EXTENSIONS

    def _is_animated_gif(self, image_path: Path) -> bool:
        """Checks if the GIF image is animated."""
        if image_path.suffix.lower() != '.gif':
            return False

        try:
            img = self.load_image(image_path)
            try:
                img.seek(1)
                return True
            except EOFError:
                return False
        except Exception as e:
            raise ImageProcessingError(
                f"Error checking GIF animation: {str(e)}")
