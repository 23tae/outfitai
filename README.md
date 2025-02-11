- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Notes](#notes)

## Description

AI-based clothing image classification tool using OpenAI API. The tool analyzes clothing images and outputs color, category, dress code, and seasonal information in JSON format.

### Features

- Image classification (color, category, dress code, season)
- Both CLI and library usage support
- Single image and batch processing support
- Performance optimization through async processing
- Flexible configuration management

#### Classification Criteria

- **Color**: Primary color as a HEX code (e.g. #FF0000)
- **Category**: top, bottom, outer, dress, footwear, bag, accessory, other
- **Dress code**: casual, business, party, sports, formal, other
- **Season**: spring, summer, fall, winter

### Requirements

- Python 3.8+

## Installation

### 1. Install from PyPI (Recommended)

```bash
pip install outfitai
```

### 2. Install from source

```bash
# Clone repository
git clone https://github.com/23tae/outfitai.git
cd outfitai

# Install package
pip install -e .
```

## Usage

- [Set OpenAPI Key](#setting-openai-api-key) before use.
- Supported image file formats: PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp) and non-animated GIF(.gif)

### 1. As a Library

You can use it in your Python code:

```python
from outfitai import OpenAIClassifier, Settings
import asyncio

# Method 1: Use environment variables or .env file
classifier = OpenAIClassifier()

# Method 2: Direct settings
settings = Settings(OPENAI_API_KEY="your-api-key")
classifier = OpenAIClassifier(settings)

# Method 3: Dictionary settings
classifier = OpenAIClassifier({
    "OPENAI_API_KEY": "your-api-key",
    "BATCH_SIZE": 5
})

# Process single image
async def process_single():
    result = await classifier.classify_single("path/to/image.jpg")
    print(result)

# Process multiple images
async def process_batch():
    # From directory
    results = await classifier.classify_batch("path/to/images/")
    # Or from list of files
    results = await classifier.classify_batch(["image1.jpg", "image2.jpg"])
    print(results)

# Run async functions
asyncio.run(process_single())
asyncio.run(process_batch())
```

### 2. Command Line Interface

Process a single image and display results:
```bash
outfitai path/to/image.jpg
```

Save results to file:
```bash
outfitai path/to/image.jpg --output result.json
```

Process all images in a directory:
```bash
outfitai path/to/images/ --batch
```

#### CLI Options

```
Required:
  IMAGE_PATH          Path to image file or directory

Optional:
  --batch, -b         Process all images in directory
  --output, -o FILE   Save results to JSON file
```

### Example Output

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

## Configuration

### Setting OpenAI API Key

1. Environment variable (Recommended):
    ```bash
    export OPENAI_API_KEY=your-api-key
    ```

2. In `.bashrc` or `.zshrc`:
    ```bash
    echo 'export OPENAI_API_KEY=your-api-key' >> ~/.bashrc
    ```

3. `.env` file in project root:
    ```
    OPENAI_API_KEY=your_api_key
    ```

4. Direct in code:
    ```python
    settings = Settings(OPENAI_API_KEY="your-api-key")
    classifier = OpenAIClassifier(settings)
    ```

### Available Settings

All settings can be configured through environment variables, `.env` file, or in code:

- Required:
  - `OPENAI_API_KEY`: **OpenAI API key**
- Optional:
  - `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini) ([reference](https://platform.openai.com/docs/models))
  - `BATCH_SIZE`: Batch processing size (default: 10)
  - `LOG_LEVEL`: Logging level (default: INFO)

Example of using custom settings:
```python
settings = Settings(
    OPENAI_API_KEY="your-api-key",
    OPENAI_MODEL="gpt-4o",
    BATCH_SIZE=5,
    LOG_LEVEL="DEBUG"
)
classifier = OpenAIClassifier(settings)
```

## Notes

- API costs vary by OpenAI model ([reference](https://platform.openai.com/docs/pricing))
- When using as a library, remember that the classifier methods are asynchronous
- The library automatically handles image size optimization
