# AI Fashion Classifier

OpenAI API를 사용한 AI 기반 의류 이미지 분류 도구입니다. 의류 이미지를 분석하여 색상, 카테고리, 드레스 코드, 계절 정보를 JSON 형태로 출력합니다.

## 주요 기능

- 이미지 분류(색상, 카테고리, 드레스 코드, 계절)
- 이미지 크기 최적화
- CLI 인터페이스 제공
- 단일 이미지 및 배치 처리 지원
- 비동기 처리를 통한 성능 최적화

## 시스템 요구사항

- Python 3

## 설치 방법

### 1. PyPI를 통한 설치 (권장)

```bash
pip install ai-fashion-classifier
```

### 2. 소스코드를 통한 설치

```bash
# 저장소 복제
git clone https://github.com/23tae/ai-fashion-classifier.git
cd ai-fashion-classifier

# 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 패키지 설치
pip install -e .
```

### OpenAI API Key 설정

1. Shell 명령어 실행 (권장):
    ```bash
    export OPENAI_API_KEY=your-api-key
    ```

2. `.bashrc` 또는 `.zshrc` 설정:
    ```bash
    echo 'export OPENAI_API_KEY=your-api-key' >> ~/.bashrc
    ```

3. `.env` 파일 생성:
    ```
    OPENAI_API_KEY=your_api_key
    ```

## 사용 방법

### 기본 사용법

```bash
ai-fc path/to/image.jpg
```

### 분류 결과 저장

```bash
ai-fc path/to/image.jpg --output results.json
```

### 다중 이미지 처리

```bash
ai-fc path/to/images/ --batch
```

### 옵션

```
필수:
  IMAGE_PATH          이미지 파일이나 디렉토리의 경로

선택:
  --batch, -b         특정 디렉토리에 위치한 모든 이미지 처리
  --output, -o FILE   결과를 JSON 형식으로 저장
```

### 출력 예시

```json
{
  "color": "#FF0000",
  "category": "outer",
  "dresscode": "formal",
  "season": ["fall", "winter"]
}
```

## 설정 관리

Shell 명령어 또는 `settings.py` 파일을 통해 설정을 관리합니다.
```bash
  export OPENAI_API_KEY=your-api-key
```

- 필수 사항
  - `OPENAI_API_KEY`: **OpenAI API 키**
- 선택 사항
  - `OPENAI_MODEL`: 사용할 OpenAI 모델 (기본값: gpt-4o-mini) ([참고](https://platform.openai.com/docs/models))
  - `TEMP_DIRECTORY`: 임시 파일 저장 경로 (기본값: tmp)
  - `IMG_THRESHOLD`: 이미지 최대 픽셀 크기 (기본값: 512) ([참고](https://platform.openai.com/docs/guides/vision))
  - `LOG_LEVEL`: 로깅 레벨 (기본값: INFO)
  - `BATCH_SIZE`: 배치 처리 크기 (기본값: 10)

## 참고 사항
- 이미지 처리 후 임시 파일은 자동으로 삭제됩니다
- OpenAI 모델별로 API 호출 비용에 차이가 있습니다 ([참고](https://platform.openai.com/docs/pricing))
