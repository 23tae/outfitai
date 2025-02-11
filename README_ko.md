- [개요](#개요)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [설정 관리](#설정-관리)
- [참고 사항](#참고-사항)

## 개요

AI 기반의 의류 이미지 분류 도구입니다. 의류 이미지를 분석하여 색상, 카테고리, 드레스 코드, 계절 정보를 JSON 형태로 출력합니다.

### 주요 기능

- 이미지 분류(색상, 카테고리, 드레스 코드, 계절)
- CLI 및 라이브러리 형태로 사용 가능
- 단일 이미지 및 배치 처리 지원
- 비동기 처리를 통한 성능 최적화
- 유연한 설정 관리

#### 분류 항목

- **Color**: 주요 색상 (ex. #FF0000)
- **Category**: top, bottom, outer, dress, footwear, bag, accessory, other
- **Dress code**: casual, business, party, sports, formal, other
- **Season**: spring, summer, fall, winter

### 시스템 요구사항

- Python 3

## 설치 방법

### 1. PyPI를 통한 설치 (권장)

```bash
pip install outfitai
```

### 2. 소스코드를 통한 설치

```bash
# 저장소 복제
git clone https://github.com/23tae/outfitai.git
cd outfitai

# 패키지 설치
pip install -e .
```

## 사용 방법

- 사용 전 [OpenAPI 키 설정](#openai-api-키-설정-방법)이 필요합니다.
- 지원하는 이미지 파일 형식: PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp), non-animated GIF(.gif)

### 1. 라이브러리로 사용

Python 코드에서 다음과 같이 사용할 수 있습니다:

```python
from outfitai import OpenAIClassifier, Settings
import asyncio

# 방법 1: 환경 변수나 .env 파일 사용
classifier = OpenAIClassifier()

# 방법 2: 직접 설정
settings = Settings(OPENAI_API_KEY="your-api-key")
classifier = OpenAIClassifier(settings)

# 방법 3: 딕셔너리로 설정
classifier = OpenAIClassifier({
    "OPENAI_API_KEY": "your-api-key",
    "BATCH_SIZE": 5
})

# 단일 이미지 처리
async def process_single():
    result = await classifier.classify_single("path/to/image.jpg")
    print(result)

# 다중 이미지 처리
async def process_batch():
    # 디렉토리에서 처리
    results = await classifier.classify_batch("path/to/images/")
    # 또는 파일 목록으로 처리
    results = await classifier.classify_batch(["image1.jpg", "image2.jpg"])
    print(results)

# 비동기 함수 실행
asyncio.run(process_single())
asyncio.run(process_batch())
```

### 2. CLI 사용

단일 이미지 처리:
```bash
outfitai path/to/image.jpg
```

결과를 파일로 저장:
```bash
outfitai path/to/image.jpg --output results.json
```

디렉토리 내 모든 이미지 처리:
```bash
outfitai path/to/images/ --batch
```

#### CLI 옵션

```
필수:
  IMAGE_PATH          이미지 파일이나 디렉토리의 경로

선택:
  --batch, -b         특정 디렉토리에 위치한 모든 이미지 처리
  --output, -o FILE   결과를 JSON 형식으로 저장
```

### 출력 예시

```json
[
  {
    "image_path": "path/to/image.jpg",
    "color": "#FF0000",
    "category": "outer",
    "dresscode": "formal",
    "season": ["fall", "winter"]
  }
]
```

## 설정 관리

### OpenAI API 키 설정 방법

1. 환경 변수 사용 (권장):
    ```bash
    export OPENAI_API_KEY=your-api-key
    ```

2. `.bashrc` 또는 `.zshrc` 설정:
    ```bash
    echo 'export OPENAI_API_KEY=your-api-key' >> ~/.bashrc
    ```

3. 프로젝트 루트에 `.env` 파일 생성:
    ```
    OPENAI_API_KEY=your_api_key
    ```

4. 코드에서 직접 설정:
    ```python
    settings = Settings(OPENAI_API_KEY="your-api-key")
    classifier = OpenAIClassifier(settings)
    ```

### 설정 가능한 옵션

모든 설정은 환경 변수, `.env` 파일, 또는 코드에서 직접 설정할 수 있습니다:

- 필수 사항:
  - `OPENAI_API_KEY`: **OpenAI API 키**
- 선택 사항:
  - `OPENAI_MODEL`: 사용할 OpenAI 모델 (기본값: gpt-4o-mini) ([참고](https://platform.openai.com/docs/models))
  - `BATCH_SIZE`: 배치 처리 크기 (기본값: 10)
  - `LOG_LEVEL`: 로깅 레벨 (기본값: INFO)

커스텀 설정 예시:
```python
settings = Settings(
    OPENAI_API_KEY="your-api-key",
    OPENAI_MODEL="gpt-4o",
    BATCH_SIZE=5,
    LOG_LEVEL="DEBUG"
)
classifier = OpenAIClassifier(settings)
```

## 참고 사항

- OpenAI 모델별로 API 호출 비용에 차이가 있습니다 ([참고](https://platform.openai.com/docs/pricing))
- 라이브러리로 사용시 메서드가 비동기(async)임을 유의바랍니다
- 라이브러리가 자동으로 이미지 크기를 최적화합니다
