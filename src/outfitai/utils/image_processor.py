from PIL import Image, UnidentifiedImageError
from pathlib import Path
import base64
from typing import Optional
from functools import lru_cache
from ..error.exceptions import ImageProcessingError
from ..config.settings import Settings
from .logger import Logger


class ImageProcessor:
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        logger_manager = Logger(self.settings)
        self.logger = logger_manager.setup_logger(__name__)

    def check_image_file(self, image_path):
        ext = Path(image_path).suffix
        if ext not in [".png", ".jpeg", ".jpg", ".webp", ".gif"]:
            raise ImageProcessingError("File extension not supported")
        if ext == ".gif" and self._check_animated_gif(image_path):
            raise ImageProcessingError("Animated GIF not supported")
        try:
            Image.open(image_path)
        except UnidentifiedImageError:
            raise ImageProcessingError("Failed to identify image file")

        except Exception as e:
            raise ImageProcessingError(f"Failed to process image: {str(e)}")

    @lru_cache(maxsize=100)
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 with caching."""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            raise ImageProcessingError(f"Failed to encode image: {str(e)}")

    def _check_animated_gif(self, image_path):
        try:
            with Image.open(image_path) as img:
                try:
                    img.seek(1)
                    return True
                except EOFError:
                    return False
        except Exception as e:
            raise Exception(f"Error checking GIF animation: {str(e)}")
