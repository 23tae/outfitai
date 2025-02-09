from PIL import Image
import os
from shutil import copyfile, rmtree
from typing import Tuple
import base64
from config import UtilsConfig


class ImageSizeError(Exception):
    pass


def get_image_dimensions(image: Image.Image) -> Tuple[int, int]:
    """이미지의 width와 height를 반환한다."""
    return image.size


def should_resize(width: int, height: int, threshold: int = UtilsConfig.IMG_THRESHOLD) -> bool:
    """더 긴 변이 threshold를 초과하는지 확인한다."""
    return max(width, height) > threshold


def prepare_temp_directory(temp_dir: str) -> None:
    if os.path.exists(temp_dir):
        if os.path.isdir(temp_dir):
            rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)


def check_image_size(image_path: str, temp_dir: str = UtilsConfig.TEMP_DIRECTORY) -> str:
    """
    이미지 크기를 확인하고 필요한 경우 리사이징한다.
    """
    try:
        with Image.open(image_path) as im:
            width, height = get_image_dimensions(im)

        prepare_temp_directory(temp_dir)

        filename = os.path.basename(image_path)
        temp_image_path = os.path.join(temp_dir, filename)
        copyfile(image_path, temp_image_path)

        if should_resize(width, height):
            return resize_image(temp_image_path)

        return temp_image_path

    except Exception as e:
        raise ImageSizeError(f"Image erorr: {str(e)}")


def resize_image(image_path: str, target_size: int = UtilsConfig.IMG_THRESHOLD) -> str:
    """
    이미지를 리사이징한다. 긴 쪽을 기준으로 비율을 유지하여 조정한다.
    """
    try:
        with Image.open(image_path) as img:
            width, height = get_image_dimensions(img)

            # 긴 쪽을 기준으로 비율 계산
            longer_side = max(width, height)
            ratio = target_size / longer_side

            new_width = int(width * ratio)
            new_height = int(height * ratio)

            resized_img = img.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

            new_image_path = f"{os.path.splitext(image_path)[0]}_resized.jpg"
            resized_img.save(new_image_path, 'JPEG', quality=95)

            return new_image_path

    except Exception as e:
        print(f'Image resize failed: {str(e)}')
        raise


def encode_image(image_path):
    """
    이미지를 Base64로 변환한다.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
