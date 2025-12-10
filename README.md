# Offline-YouTube-Video-Summarizer
An offline AI system that downloads YouTube videos, extracts audio, transcribes using Whisper, and generates a clean summary-completely offline with no API usage.

# 🎥 YouTube Video Summarizer

An offline, local-first tool to automatically download the audio from a YouTube video, generate a full transcript using OpenAI's Whisper model, and produce a concise summary using a Hugging Face transformer model (BART-Large-CNN).

This project runs the entire pipeline—download, transcription, and summarization—on your local machine.

## ✨ Features

* **Offline Processing:** Runs all NLP tasks (transcription and summarization) locally without relying on external APIs (except for the initial model downloads).
* **Audio Download:** Uses `yt-dlp` to download the best available audio stream from a YouTube URL.
* **High-Quality Transcription:** Leverages the powerful **OpenAI Whisper** model for accurate transcription. Supports multiple model sizes (`tiny` to `large`).
* **Abstractive Summarization:** Uses the **BART-Large-CNN** transformer model for high-quality, abstractive summaries.
* **Long Text Handling:** Includes logic to chunk and recursively summarize very long transcripts.
* **Setup Verification:** A dedicated script to check dependencies and model readiness.

  ## 🚀 Getting Started

### Prerequisites

You need the following installed on your system:

1.  **Python 3.8+**
2.  **FFmpeg:** Required by `yt-dlp` and `openai-whisper` for audio handling.
    * [Install FFmpeg Guide](https://ffmpeg.org/download.html)

### Installation

1.  **Clone the repository (or set up the files):**
    ```bash
    git clone [Your-Repo-Link-Here]
    cd youtube-summarizer
    ```

2.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` with the packages mentioned in `verify_setup.py`)*

    **Example `requirements.txt` content:**
    ```
    yt-dlp
    openai-whisper
    transformers
    torch
    ```
    * You may also need `ffmpeg-python` if Whisper requires it.

### Setup Verification

Run the verification script to ensure all dependencies and FFmpeg are correctly set up.

```bash
python verify_setup.py
To also check if the large models can be downloaded and loaded (this may take significant time and storage, as the BART model is ~1.6GB):Bashpython verify_setup.py --check-models
💻 UsageThe main application is run via the command-line interface in main.py.Basic CommandProvide a YouTube URL as the first argument.Bashpython main.py [https://www.youtube.com/watch?v=VIDEO_ID](https://www.youtube.com/watch?v=VIDEO_ID)
The script will:Download the audio to the downloads directory.Transcribe the audio using the default base Whisper model.Summarize the transcript using the default facebook/bart-large-cnn model.Print the transcript and summary to the console.Remove the downloaded audio file (--cleanup is default).Advanced OptionsFlagDescriptionDefaultChoices/Exampleurl (positional)Required YouTube video URL.N/Ahttps://youtu.be/ID--whisper-modelWhisper model size for transcription.basetiny, base, small, medium, large--summarizer-modelHugging Face summarization model.facebook/bart-large-cnn(Any suitable Hugging Face model)--output FILEFile path to write the results (summary & transcript).None (print to stdout)summary.txt--output-dir DIRDirectory for temporary audio downloads.downloadstemp_audio--no-cleanupKeep the downloaded audio files after processing.(False)--transcript-onlySkip the summarization step, outputting only the transcript.(False)--verboseEnable verbose logging (DEBUG level).(False)Examples1. Use the smaller Whisper model and keep audio file:Bashpython main.py [https://www.youtube.com/watch?v=VIDEO_ID](https://www.youtube.com/watch?v=VIDEO_ID) --whisper-model small --no-cleanup
2. Output the summary and transcript to a file:Bashpython main.py [https://www.youtube.com/watch?v=VIDEO_ID](https://www.youtube.com/watch?v=VIDEO_ID) --output output/summary.txt
🛠️ Project StructureFileDescriptionmain.pyCommand-Line Interface (CLI) and orchestration of the entire pipeline.downloader.pyHandles downloading the audio from a YouTube URL using yt-dlp.transcriber.pyImplements the transcription logic using the openai-whisper library.summarizer.pyImplements the text summarization using the transformers library (BART-Large-CNN).verify_setup.pyScript to check for required dependencies and external tools (FFmpeg, models).__init__.pyPackage initialization file (sets version and imports components).📦 DependenciesThe core functionality relies on:yt-dlp: For downloading YouTube video audio.openai-whisper: For local, high-quality audio transcription.transformers: For utilizing the BART model for summarization.torch: The underlying deep learning framework (for Whisper and Transformers).
---

Would you like me to generate the **`requirements.txt`** file based on the dependencies used in the code?
