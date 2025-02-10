# AI Fashion Classifier

AI-based clothing image classification tool using OpenAI API. The tool analyzes clothing images and outputs color, category, dress code, and seasonal information in JSON format.

## Features

- Image classification (color, category, dress code, season)
- Image size optimization
- CLI interface
- Single image and batch processing support
- Performance optimization through async processing

## Requirements

- Python 3

## Installation

### 1. Install from PyPI (Recommended)

```bash
pip install ai-fashion-classifier
```

### 2. Install from source

```bash
# Clone repository
git clone https://github.com/23tae/ai-fashion-classifier.git
cd ai-fashion-classifier

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install package
pip install -e .
```

### Set OpenAI API Key

1. by Shell command (Recommended):
    ```bash
    export OPENAI_API_KEY=your-api-key
    ```

2. by `.bashrc` or `.zshrc`:
    ```bash
    echo 'export OPENAI_API_KEY=your-api-key' >> ~/.bashrc
    ```

3. by `.env` file:
    ```
    OPENAI_API_KEY=your_api_key
    ```

## Usage

### Basic Usage

Process a single image and display results:
```bash
ai-fc path/to/image.jpg
```

### Save Results to File

Analyze image and save results as JSON:
```bash
ai-fc path/to/image.jpg --output result.json
```

### Batch Processing

Process all images in a directory:
```bash
ai-fc path/to/images/ --batch
```

### Options

```
Required:
  IMAGE_PATH          Path to image file or directory

Optional:
  --batch, -b         Process all images in directory
  --output, -o FILE   Save results to JSON file
```

### Example Output

```json
{
  "color": "#FF0000",
  "category": "outer",
  "dresscode": "formal",
  "season": ["fall", "winter"]
}
```

## Configuration

Settings are managed by Shell command or `settings.py` file:
```bash
  export OPENAI_API_KEY=your-api-key
```

- Required:
  - `OPENAI_API_KEY`: **OpenAI API key**
- Optional:
  - `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini) ([reference](https://platform.openai.com/docs/models))
  - `TEMP_DIRECTORY`: Temporary file storage path (default: tmp)
  - `IMG_THRESHOLD`: Maximum image pixel size (default: 512) ([reference](https://platform.openai.com/docs/guides/vision))
  - `LOG_LEVEL`: Logging level (default: INFO)
  - `BATCH_SIZE`: Batch processing size (default: 10)

## Notes

- Temporary files are automatically deleted after image processing
- API costs vary by OpenAI model ([reference](https://platform.openai.com/docs/pricing))
