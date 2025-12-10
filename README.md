# Offline-YouTube-Video-Summarizer
An offline AI system that downloads YouTube videos, extracts audio, transcribes using Whisper, and generates a clean summary-completely offline with no API usage.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech stack](#tech-stack)
4. [Prerequisites](#prerequisites)
5. [Installation (step-by-step)](#installation-step-by-step)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [How it works (pipeline)](#how-it-works-pipeline)
9. [Project structure](#project-structure)
10. [Troubleshooting & tips](#troubleshooting--tips)
11. [Testing](#testing)
12. [Contribution guidelines](#contribution-guidelines)
13. [License & attribution](#license--attribution)
14. [Contact](#contact)

---

## Project Overview

This project downloads YouTube videos locally (supports long videos and shorts), extracts audio, transcribes it using an offline speech-to-text model, and produces concise, human-readable summaries. The goal is a privacy-preserving, offline-capable summarizer that works without sending data to third-party APIs.

## Features

* Download any public YouTube video (including shorts) to local disk.
* Extract audio and standardize format (e.g., 16kHz WAV/FLAC) for transcription.
* Offline transcription using an open-source model (e.g., Whisper-style local model or VOSK/whisperx depending on implementation).
* Text cleaning and segmentation for better summarization.
* Summary generation using an offline summarization model or lightweight rule-based summarizer (depending on configuration).
* Command-line interface for single-video or batch processing.

## Tech stack

* Python 3.10+ (recommend 3.10–3.11)
* `yt-dlp` — downloading YouTube videos
* `pydub` or `ffmpeg-python` — audio extraction and format conversion
* Offline speech model: `whisper`/`openai-whisper` (local) or `vosk` / `whisperx` (depending on repository implementation)
* Text summarization: local transformer model (e.g., `transformers`) or simple extractive summarizer
* `numpy`, `tqdm`, `torch` (if using PyTorch models)

## Prerequisites

1. A machine with Python 3.10+ installed.
2. `ffmpeg` installed and available on `PATH` (required by `yt-dlp` and `pydub`).

   * macOS: `brew install ffmpeg`
   * Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg -y`
   * Windows: download static build from ffmpeg.org and add to PATH.
3. (Optional but recommended) A virtual environment for Python dependencies.
4. If using GPU-accelerated transcription/summarization, install the appropriate CUDA toolkit and GPU drivers.

## Installation (step-by-step)

Follow these steps to set up the project locally.

> These commands assume a UNIX-like shell (macOS, Linux). For Windows use PowerShell/CMD equivalents.

1. **Clone the repository** (or upload this project to GitHub then clone):

```bash
# if you have a remote, otherwise skip
git clone https://github.com/<your-username>/<repo-name>.git
cd "<repo-name>"
```

2. **Create and activate a virtual environment** (recommended):

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

3. **Install system dependency `ffmpeg`** (if not already installed) — see Prerequisites above.

4. **Install Python dependencies**

If the repository includes `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If there is a `pyproject.toml` or `poetry.lock`, follow that project's instructions.

5. **(Optional) Download model files**

Some offline speech and summarization models are heavy. If the repo provides a helper script to pre-download models (e.g., `download_models.py`), run it now:

```bash
python scripts/download_models.py
```

Or follow the README section for model choice and location.

## Configuration

The repo may include a `config.yml` or `config.json`. Typical options to check:

* `model_name` — transcription model to use (e.g., `small`, `base`, `medium`)
* `device` — `cpu` or `cuda`
* `audio_format` — `wav` or `flac`
* `sample_rate` — 16000

Example `config.yml` snippet:

```yaml
model_name: small
device: cpu
audio_format: wav
sample_rate: 16000
```

## Usage

### Download + Transcribe a single video (CLI)

```bash
# Basic usage
python main.py "https://youtube.com/watch?v=VIDEO_ID"

# Example (shorts or full video)
python main.py "https://youtube.com/shorts/HcbrB7DGruk?si=..."
```

### Common CLI flags (if supported)

```
# download only (skip transcription)
python main.py --download-only "<URL>"

# specify output directory
python main.py --output-dir ./outputs "<URL>"

# force CPU
python main.py --device cpu "<URL>"

# preclean downloaded files after summarization
python main.py --cleanup "<URL>"
```

> See `python main.py --help` to view exact flags implemented in this repository.

## How it works (pipeline)

1. **Download video** — `yt-dlp` fetches the video and saves it to `downloads/`.
2. **Extract audio** — The extractor converts video to a standardized audio file using `ffmpeg` (mono, 16 kHz recommended).
3. **Transcription** — Audio gets segmented (long audio -> chunks), each chunk is transcribed by an offline model. Transcriptions are concatenated and post-processed (punctuation restoration, filler removal).
4. **Summarization** — The cleaned transcript is fed into a summarizer. For very long transcripts, chunk + summarize + combine is recommended.
5. **Output** — The repo writes: `{video_id}.txt` (full transcript), `{video_id}_summary.txt`, and optionally `{video_id}.srt`.

## Project structure (expected)

```
├── README.md
├── requirements.txt
├── main.py                # entry point
├── downloader.py          # yt-dlp wrapper
├── transcriber.py         # handles audio -> text
├── summarizer.py          # text -> summary
├── utils/
│   ├── audio.py           # ffmpeg/pydub helpers
│   └── text.py            # cleaning and chunking helpers
├── scripts/
│   └── download_models.py
├── tests/
└── outputs/               # where results are stored
```

If your repo differs, update this section accordingly.

## Troubleshooting & tips

* **`ModuleNotFoundError` for `downloader` or other modules**: make sure you run from the project root or add `.` to `PYTHONPATH`.

  ```bash
  export PYTHONPATH=$(pwd):$PYTHONPATH
  ```
* **`ffmpeg` not found**: confirm `ffmpeg` is installed and on PATH: `ffmpeg -version`.
* **Model memory errors (OOM)**: use smaller model (`base` -> `small` -> `tiny`) or switch to CPU by setting `device: cpu`.
* **Slow transcription**: enable GPU (if available) and install the correct CUDA-enabled `torch` package.
* **Poor transcription quality**: try a larger model or improve audio preprocessing (noise reduction, normalization).
* **YouTube download issues**: update `yt-dlp` frequently: `pip install -U yt-dlp`.

## Testing

Include unit/integration tests (if available):

```bash
# run pytest (if tests included)
pytest -q
```

## Contribution guidelines

1. Fork the repository and create a feature branch: `git checkout -b feature/clear-cli`
2. Make changes, add tests if possible.
3. Run linters and tests locally.
4. Submit a pull request with a clear description of changes.

## License & attribution

Add a license file (e.g., `MIT` or `Apache-2.0`) in the repo root. If any 3rd-party models/libraries require attribution, make sure to include proper credit.

## Contact

If you have questions, open an issue on GitHub or contact the author at: `kiranpamidi2001@gmail.com`.

---

### Quick checklist before uploading to GitHub

* [ ] Add `README.md` (this file) to repo root
* [ ] Add `requirements.txt` with pinned versions
* [ ] Add `.gitignore` (ignore `.venv`, `__pycache__`, `outputs/`, `*.pth`, model caches)
* [ ] Add `LICENSE` file
* [ ] Add small sample input link and sample outputs in `examples/`
* [ ] Add CI (GitHub Actions) to run unit tests on push

**Happy summarizing!**

---

## Generated `requirements.txt`

Below is a recommended `requirements.txt` you can drop into the project root. It contains the core packages needed for downloading, offline transcription with Whisper, and summarization with Hugging Face Transformers.

```
yt-dlp>=2025.10.0
openai-whisper>=2024.12.0
transformers>=4.30.0
torch>=2.0.0
ffmpeg-python>=0.3.0
pydub>=0.25.1
numpy>=1.24.0
tqdm>=4.65.0
huggingface-hub>=0.17.0
sentencepiece>=0.1.99
accelerate>=0.21.0
```

**Notes:**

* `ffmpeg` must be installed on your system separately (not via pip). See the `Prerequisites` section.
* Version numbers are suggestions; you can pin exact versions after testing in your environment.
* If you plan to run on GPU, ensure the installed `torch` matches your CUDA drivers (see [https://pytorch.org](https://pytorch.org) for exact install commands).

If you want, I can also:

* Pin exact versions I recommend after testing.
* Generate a `requirements-dev.txt` with testing and linting tools.
* Create a `pyproject.toml` or `environment.yml` for Conda.



