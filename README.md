# YouTube Video Summarizer

A complete offline YouTube video summarizer that downloads audio, transcribes it using Whisper, and generates summaries using transformer models. No API keys or internet connection required after initial setup.

---

## 🚀 Features
- **Complete Offline Processing:** All processing happens locally on your machine  
- **High-Quality Transcription:** Uses OpenAI's Whisper for accurate speech-to-text  
- **Advanced Summarization:** Employs BART or other Hugging Face transformer models  
- **Flexible Output:** Save results to file or display in terminal  
- **Automatic Cleanup:** Optionally removes temporary audio files after processing  
- **Multiple Model Sizes:** Choose balance between speed and accuracy  

---

## 📋 Prerequisites

### Core Dependencies
- Python 3.8+  
- FFmpeg (for audio processing)  

### Python Packages
- `yt-dlp` - YouTube audio downloading  
- `openai-whisper` - Speech-to-text transcription  
- `transformers` - Text summarization models  
- `torch` - Deep learning framework  

---

## 🔧 Installation

### Step 1: Install FFmpeg
### Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

### macOS
brew install ffmpeg

### Windows (manual)
Download from https://ffmpeg.org/download.html and add to PATH

---

## Step 2: Clone the Repository
git clone https://github.com/yourusername/youtube-summarizer.git
cd youtube-summarizer

## Step 3: Install Python Dependencies
pip install yt-dlp openai-whisper transformers torch

### Step 4: Verify Installation
python verify_setup.py

For full verification including model loading:
python verify_setup.py --check-models

### Step 5: Project Structure

youtube-summarizer \
    ├──init.py              #Package initialization \
    ├──main.py              #Main CLI application \
    ├──downloader.py        #YouTube audio downloader \
    ├──transcriber.py       #Whisper transcription module \
    ├──summarizer.py        #Text summarization module \
    ├──verify_setup.py      #Setup verification script \
    ├──README.md            #This file \
    └──downloads/           #Temporary audio storage (created automatically)


## 🎯 Usage

### Basic Usage
python main.py https://www.youtube.com/watch?v=VIDEO_ID

Save Output to File
# Save to any location
python main.py https://youtube.com/watch?v=VIDEO_ID --output my_summary.txt

# Save specifically to downloads folder
python main.py https://youtube.com/watch?v=VIDEO_ID --output downloads/summary.txt

# Advanced Options
python main.py https://www.youtube.com/watch?v=VIDEO_ID \
    - whisper-model medium \
    - summarizer-model facebook/bart-large-cnn \
    - output summary.txt \
    - output-dir downloads \
    - no-cleanup \
    - verbose
### Command-line Arguments
| Argument             | Description                                          | Default                 |
| -------------------- | ---------------------------------------------------- | ----------------------- |
| `url`                | YouTube video URL (required)                         | -                       |
| `--whisper-model`    | Whisper model size: tiny, base, small, medium, large | base                    |
| `--summarizer-model` | Hugging Face summarization model                     | facebook/bart-large-cnn |
| `--output`           | Output file path for text results (optional)         | stdout                  |
| `--output-dir`       | Directory for temporary audio downloads              | downloads               |
| `--no-cleanup`       | Keep downloaded audio files                          | False                   |
| `--transcript-only`  | Only transcribe, don't summarize                     | False                   |
| `--verbose`          | Enable verbose logging                               | False                   |

### Storage Information

Important Notes:

downloads/ directory: Only stores temporary audio files (.wav format)

Text outputs: NOT automatically saved to downloads/ - must specify with --output

What Gets Saved Where:
| File Type          | Storage Location                   | Notes                                         |
| ------------------ | ---------------------------------- | --------------------------------------------- |
| Audio files (.wav) | downloads/ directory               | Temporary, auto-cleaned unless `--no-cleanup` |
| Text outputs       | User-specified path via `--output` | Not auto-saved; must specify path             |
| Transcript         | Included in text output            | Part of the summary file                      |
| Summary            | Included in text output            | Part of the summary file                      |

How to Save Text Outputs:

Specify Custom Output File (Recommended):
python main.py https://youtube.com/watch?v=VIDEO_ID --output my_summary.txt

Pipe to file:
python main.py https://youtube.com/watch?v=VIDEO_ID > output.txt

View only in terminal:
python main.py https://youtube.com/watch?v=VIDEO_ID

### Model Information
Whisper Models (Transcription)
| Model  | Size    | Relative Speed | Recommended Use    |
| ------ | ------- | -------------- | ------------------ |
| tiny   | ~75 MB  | 32x            | Fast, low-accuracy |
| base   | ~150 MB | 16x            | Balanced (default) |
| small  | ~500 MB | 6x             | Good accuracy      |
| medium | ~1.5 GB | 2x             | High accuracy      |
| large  | ~3 GB   | 1x             | Best accuracy      |

### Summarization Models

facebook/bart-large-cnn: Recommended default (~1.6GB)

Other models from Hugging Face Model Hub can be used

Examples
Example 1: Simple Transcription Only
python main.py https://youtu.be/dQw4w9WgXcQ --transcript-only

Example 2: Complete Summary with File Output
python main.py https://www.youtube.com/watch?v=VIDEO_ID --output video_summary.txt

Example 3: High-Accuracy Processing
python main.py https://www.youtube.com/watch?v=VIDEO_ID \
    - whisper-model large \
    - summarizer-model facebook/bart-large-cnn \
    - output /path/to/save/summary.txt \
    - no-cleanup \
    - verbose

Example 4: Fast Processing with Output Redirection
python main.py https://youtu.be/VIDEO_ID --whisper-model tiny > fast_summary.txt

Example 5: Save to Downloads Folder
python main.py https://youtu.be/VIDEO_ID --output downloads/my_video_summary.txt

### How It Works

1. Download: Extracts audio from YouTube video using yt-dlp

2. Transcribe: Converts speech to text using Whisper (offline)

3. Summarize: Generates summary using transformer models (offline)

4. Output: Displays or saves transcript and summary

### Troubleshooting

Common Issues:

- "FFmpeg not found" error
# Ubuntu/Debian
sudo apt install ffmpeg

# Verify installation
ffmpeg -version

- "CUDA out of memory" error
# Use smaller model
python main.py URL --whisper-model base

# Force CPU usage
CUDA_VISIBLE_DEVICES="" python main.py URL

- Slow performance
-Use smaller Whisper models (tiny or base)
-Check GPU acceleration:
python -c "import torch; print(torch.cuda.is_available())"

- Model download issues

- First run downloads models automatically (~2-5GB total)

- Check internet connection

- Models cache: ~/.cache/whisper/ and ~/.cache/huggingface/

- Text not saved
# Use --output flag to save
python main.py URL --output summary.txt


### Notes & Limitations
First run downloads models: Whisper (~150MB-3GB) + BART (~1.6GB)
Processing time: 2-10x video length depending on model and hardware
GPU acceleration recommended for faster transcription
Text outputs require explicit --output argument
Long videos (>30 mins) may require more RAM/VRAM

### License
This project is for educational purposes. Ensure you comply with YouTube's Terms of Service when using this tool.
