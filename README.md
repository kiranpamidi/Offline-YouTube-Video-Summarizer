# YouTube Video Summarizer

A complete offline YouTube video summarizer that downloads audio, transcribes it using Whisper, and generates summaries using transformer models. No API keys or internet connection required after initial setup.

## Features

- **Complete Offline Processing**: All processing happens locally on your machine
- **High-Quality Transcription**: Uses OpenAI's Whisper for accurate speech-to-text
- **Advanced Summarization**: Employs BART or other Hugging Face transformer models
- **Flexible Output**: Save results to file or display in terminal
- **Automatic Cleanup**: Optionally removes temporary audio files after processing
- **Multiple Model Sizes**: Choose balance between speed and accuracy

## Requirements

### Core Dependencies
- Python 3.8+
- FFmpeg (for audio processing)

### Python Packages
- yt-dlp - YouTube audio downloading
- openai-whisper - Speech-to-text transcription
- transformers - Text summarization models
- torch - Deep learning framework
- argparse - Command-line interface (standard library)
- logging - Logging (standard library)


### System Requirements
- 4GB+ RAM (8GB+ recommended)
- 2GB+ free disk space for models
- CUDA-capable GPU (optional, for faster processing)

## Installation

### 1. Install FFmpeg
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [FFmpeg official website](https://ffmpeg.org/download.html)

### 2. Install Python packages:
```bash
pip install yt-dlp openai-whisper transformers torch

### 3. Verify installation:
