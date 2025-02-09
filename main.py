import sys
from shutil import rmtree
from utils import check_image_size
from classify_openai import classify_clothing_item_openai
from config import UtilsConfig


def main(image_path: str):
    processed_image = None
    try:
        # 1. 이미지 규격 변환
        processed_image = check_image_size(image_path)

        # 2. 이미지 분석
        result = classify_clothing_item_openai(processed_image)
        print(result)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # 3. 임시 디렉토리 삭제
        temp_dir = UtilsConfig.TEMP_DIRECTORY
        rmtree(temp_dir)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    main(image_path)
