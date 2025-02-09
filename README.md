# AI Fashion Classifier

AI 기반 의류 이미지 분류 도구입니다. OpenAI의 GPT-4o mini 모델을 사용하여 의류 이미지를 분석하고, 색상, 카테고리, 드레스 코드, 계절 정보 등을 JSON 형태로 출력합니다.

## 주요 기능

- 이미지 크기 최적화
- 의류 주요 색상 검출 (HEX 코드)
- 의류 카테고리 분류 (상의, 하의, 아우터 등)
- 드레스 코드 분류 (캐주얼, 비즈니스, 포멀 등)
- 계절 분류

## 시스템 요구사항

- Python 3
- OpenAI API 키

## 설치 방법

1. 가상환경 생성 및 활성화

  ```bash
  python3 -m venv .venv
  source .venv/bin/activate  # Windows: .venv\Scripts\activate
  ```

2. 필요한 패키지 설치

  ```bash
  pip install -r requirements.txt
  ```

3. 프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 OpenAI API 키 추가

  ```
  OPENAI_API_KEY=your_api_key
  ```

## 사용 방법

- 이미지 경로과 함께 프로그램 실행

  ```bash
  python3 main.py <이미지_경로>
  ```

- 프로그램 실행 과정

  1. 이미지 크기 확인 및 필요시 최적화
  2. OpenAI API를 통한 이미지 분석
  3. 분류 결과를 JSON 형식으로 출력

### 출력 예시

```json
{
  "color": "#FF0000",
  "category": "outer",
  "dresscode": "formal",
  "season": ["fall", "winter"]
}
```

## 설정

`config.py`에서 설정을 변경할 수 있습니다.

- `MODEL`: 사용할 OpenAI 모델 ([참고](https://platform.openai.com/docs/models))
- `TEMP_DIRECTORY`: 임시 파일 저장 디렉토리
- `IMG_THRESHOLD`: 이미지 최대 픽셀수 ([참고](https://platform.openai.com/docs/guides/vision))


## 참고사항

- 이미지 처리 후 임시 파일은 자동으로 삭제됩니다.
- OpenAI 모델별로 API 호출 비용에 차이가 있습니다. ([참고](https://platform.openai.com/docs/pricing))
