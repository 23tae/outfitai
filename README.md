# AI Fashion Classifier

AI 기반 의류 이미지 분류 도구입니다. OpenAI의 GPT-4o mini 모델을 사용하여 의류 이미지를 분석하고, 색상, 카테고리, 드레스 코드, 계절 정보 등을 JSON 형태로 출력합니다.

## 주요 기능

- 이미지 분류(색상, 카테고리, 드레스 코드, 계절)
- 이미지 크기 최적화
- CLI 인터페이스 제공
- 단일 이미지 및 배치 처리 지원
- 비동기 처리를 통한 성능 최적화

## 시스템 요구사항

- Python 3
- OpenAI API 키

## 설치 방법

1. 가상환경 생성 및 활성화

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate  # Windows: .venv\Scripts\activate
  ```

2. 패키지 설치

  ```bash
  pip install -e .
  ```

3. 환경변수 설정 (`.env` 파일 생성)

  ```
  OPENAI_API_KEY=your_api_key
  ```

## 사용 방법

### 단일 이미지 분석

```bash
ai-fc image.jpg
```

### 다중 이미지 처리

```bash
ai-fc images_directory/ -b
```

### 결과 저장

```bash
ai-fc image.jpg -o result.json
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

## 설정 옵션

`Settings` 클래스에서 다음 설정을 관리합니다:

- `OPENAI_API_KEY`: OpenAI API 키
- `MODEL`: 사용할 OpenAI 모델 (기본값: gpt-4o-mini) ([참고](https://platform.openai.com/docs/models))
- `TEMP_DIRECTORY`: 임시 파일 저장 경로 (기본값: tmp)
- `IMG_THRESHOLD`: 이미지 최대 픽셀 크기 (기본값: 512) ([참고](https://platform.openai.com/docs/guides/vision))
- `LOG_LEVEL`: 로깅 레벨 (기본값: INFO)
- `BATCH_SIZE`: 배치 처리 크기 (기본값: 10)

## 참고사항

- 이미지 처리 후 임시 파일은 자동으로 삭제됩니다.
- OpenAI 모델별로 API 호출 비용에 차이가 있습니다. ([참고](https://platform.openai.com/docs/pricing))
