from PIL import Image
from pathlib import Path
import base64
from typing import Tuple, Optional
from functools import lru_cache
from ..error.exceptions import ImageProcessingError
from ..config.settings import Settings
from .logger import Logger


class ImageProcessor:
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        logger_manager = Logger(self.settings)
        self.logger = logger_manager.setup_logger(__name__)
        self._setup_temp_directory()

    def _setup_temp_directory(self):
        """Set up temporary directory for processed images."""
        temp_dir = Path(self.settings.TEMP_DIRECTORY)
        if temp_dir.exists():
            for file in temp_dir.glob("*"):
                file.unlink()
        else:
            temp_dir.mkdir(parents=True)

    def get_image_dimensions(self, image: Image.Image) -> Tuple[int, int]:
        """Return the dimensions of an image."""
        return image.size

    def should_resize(self, width: int, height: int) -> bool:
        """Check if image needs resizing."""
        return max(width, height) > self.settings.IMG_THRESHOLD

    @lru_cache(maxsize=100)
    def encode_image(self, image_path: str) -> str:
        """Encode image to base64 with caching."""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except Exception as e:
            raise ImageProcessingError(f"Failed to encode image: {str(e)}")

    async def process_image(self, image_path: str) -> str:
        """Process a single image."""
        try:
            img = Image.open(image_path)
            width, height = self.get_image_dimensions(img)

            temp_path = Path(self.settings.TEMP_DIRECTORY) / \
                Path(image_path).name

            if self.should_resize(width, height):
                return await self._resize_image(img, temp_path)
            else:
                img.save(temp_path)
                return str(temp_path)

        except Exception as e:
            raise ImageProcessingError(f"Failed to process image: {str(e)}")

    async def _resize_image(self, img: Image.Image, output_path: Path) -> str:
        """Resize image maintaining aspect ratio."""
        width, height = self.get_image_dimensions(img)
        ratio = self.settings.IMG_THRESHOLD / max(width, height)

        new_size = (int(width * ratio), int(height * ratio))
        resized = img.resize(new_size, Image.Resampling.LANCZOS)

        resized.save(output_path, 'JPEG', quality=95)
        return str(output_path)
