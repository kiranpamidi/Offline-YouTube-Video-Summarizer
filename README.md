YouTube Video Summarizer
A complete offline YouTube video summarizer that downloads audio, transcribes it using Whisper, and generates summaries using transformer models. No API keys or internet connection required after initial setup.

Features
Complete Offline Processing: All processing happens locally on your machine

High-Quality Transcription: Uses OpenAI's Whisper for accurate speech-to-text

Advanced Summarization: Employs BART or other Hugging Face transformer models

Flexible Output: Save results to file or display in terminal

Automatic Cleanup: Optionally removes temporary audio files after processing

Multiple Model Sizes: Choose balance between speed and accuracy

Requirements
Core Dependencies
Python 3.8+

FFmpeg (for audio processing)

Python Packages
yt-dlp - YouTube audio downloading

openai-whisper - Speech-to-text transcription

transformers - Text summarization models

torch - Deep learning framework

argparse - Command-line interface (standard library)

logging - Logging (standard library)

Installation
Install FFmpeg:

Ubuntu/Debian: sudo apt install ffmpeg

macOS: brew install ffmpeg

Windows: Download from ffmpeg.org

Install Python packages:

bash
pip install yt-dlp openai-whisper transformers torch
Verify installation:

bash
python verify_setup.py
For full verification including model loading:

bash
python verify_setup.py --check-models
Usage
Basic Usage
bash
python main.py https://www.youtube.com/watch?v=VIDEO_ID
Advanced Options
bash
python main.py https://www.youtube.com/watch?v=VIDEO_ID \
    --whisper-model medium \
    --summarizer-model facebook/bart-large-cnn \
    --output summary.txt \
    --output-dir downloads \
    --no-cleanup \
    --verbose
Command-line Arguments
Argument	Description	Default
url	YouTube video URL (required)	-
--whisper-model	Whisper model size: tiny, base, small, medium, large	base
--summarizer-model	Hugging Face summarization model	facebook/bart-large-cnn
--output	Output file path for text results (optional)	stdout
--output-dir	Directory for temporary audio downloads	downloads
--no-cleanup	Keep downloaded audio files	False
--transcript-only	Only transcribe, don't summarize	False
--verbose	Enable verbose logging	False
Important Storage Notes
Directory Structure:
downloads/ directory: Only for temporary audio files (.wav format)

Text outputs: NOT automatically saved to downloads/ - must specify output path

How to Save Text Outputs:
Specify Custom Output File (Recommended):

bash
# Save to any location
python main.py https://youtube.com/watch?v=VIDEO_ID --output my_summary.txt

# Save specifically to downloads folder
python main.py https://youtube.com/watch?v=VIDEO_ID --output downloads/summary.txt
Pipe to File:

bash
# Redirect terminal output
python main.py https://youtube.com/watch?v=VIDEO_ID > output.txt
View Only in Terminal (default):

bash
# Text is displayed but not saved
python main.py https://youtube.com/watch?v=VIDEO_ID
What Gets Saved Where:
File Type	Storage Location	Notes
Audio files (.wav)	downloads/ directory	Temporary, auto-cleaned unless --no-cleanup
Text outputs	User-specified path via --output	Not auto-saved; must specify path
Transcript	Included in text output	Part of the summary file
Summary	Included in text output	Part of the summary file
Project Structure
text
.
├── init.py              # Package initialization
├── main.py              # Main CLI application
├── downloader.py        # YouTube audio downloader
├── transcriber.py       # Whisper transcription module
├── summarizer.py        # Text summarization module
├── verify_setup.py      # Setup verification script
└── downloads/           # Temporary audio storage (created automatically)
Module Details
1. YouTubeDownloader (downloader.py)
Downloads audio from YouTube videos using yt-dlp

Extracts video ID from URLs

Converts to WAV format using FFmpeg

Saves audio to downloads/ directory

Optional cleanup of temporary audio files

2. Transcriber (transcriber.py)
Uses OpenAI Whisper for speech-to-text

Supports multiple model sizes for speed/accuracy trade-off

Automatic GPU detection (CUDA support)

Language detection and forced language options

3. Summarizer (summarizer.py)
Uses Hugging Face transformers for text summarization

Supports multiple models (BART, T5, etc.)

Handles long texts through chunking

Automatic device selection (CPU/GPU)

4. YouTubeSummarizer (main.py)
Orchestrates the complete pipeline

Provides CLI interface with argument parsing

Handles errors and cleanup

Manages logging and output formatting

Model Sizes and Performance
Whisper Models
Model	Size	Relative Speed	Recommended Use
tiny	~75 MB	32x	Fast, low-accuracy
base	~150 MB	16x	Balanced
small	~500 MB	6x	Good accuracy
medium	~1.5 GB	2x	High accuracy
large	~3 GB	1x	Best accuracy
Summarization Models
facebook/bart-large-cnn: Recommended default (~1.6GB)

Other models from Hugging Face Model Hub can be used

Examples
1. Simple transcription only (output to terminal):
bash
python main.py https://youtu.be/dQw4w9WgXcQ --transcript-only
2. Save complete summary to file:
bash
python main.py https://www.youtube.com/watch?v=VIDEO_ID --output video_summary.txt
3. High-accuracy processing with custom save location:
bash
python main.py https://www.youtube.com/watch?v=VIDEO_ID \
    --whisper-model large \
    --summarizer-model facebook/bart-large-cnn \
    --output /path/to/save/summary.txt \
    --no-cleanup \
    --verbose
4. Save to downloads folder specifically:
bash
python main.py https://youtu.be/VIDEO_ID --output downloads/my_video_summary.txt
5. Quick summary (fastest) with output redirection:
bash
python main.py https://youtu.be/VIDEO_ID --whisper-model tiny > fast_summary.txt
Error Handling
The application includes comprehensive error handling:

Invalid URLs are detected

Download failures are caught and reported

Model loading errors are handled gracefully

Cleanup happens even on failure (unless --no-cleanup)

Troubleshooting
"FFmpeg not found" error:

Install FFmpeg using your package manager

Add FFmpeg to your system PATH

"CUDA out of memory" error:

Use smaller models (--whisper-model base or small)

Run on CPU by setting CUDA_VISIBLE_DEVICES=""

Slow performance:

Use smaller Whisper models (tiny or base)

Ensure you have GPU acceleration enabled

Model download issues:

First run downloads models automatically

Check internet connection for initial download

Models are cached in ~/.cache/

"Text not saved to downloads folder":

Text outputs require explicit --output argument

Use --output downloads/filename.txt to save text to downloads

Notes
First run will download models (Whisper: ~150MB-3GB, BART: ~1.6GB)

Processing time depends on video length and model size

GPU acceleration significantly improves transcription speed

All processing happens offline after initial model download

Text outputs are not automatically saved - use --output to save them

License
This project is for educational purposes. Ensure you comply with YouTube's Terms of Service when using this tool.

Disclaimer
This tool is intended for personal use and educational purposes. Always respect copyright laws and content creators' rights. Download only content you have permission to access.

