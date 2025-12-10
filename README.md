# 🎥 Offline YouTube Video Summarizer

A fully offline AI system that downloads the audio from any YouTube video, transcribes it using **OpenAI Whisper**, and generates a clean, structured summary using a local **Hugging Face transformer model** (BART-Large-CNN) — all running **entirely on your machine** with no external APIs.

Perfect for offline research, privacy-sensitive environments, and local AI experimentation.

---

# ✨ Features

* **Offline Transcription:** Uses OpenAI Whisper for accurate speech-to-text conversion.
* **Offline Summarization:** Uses the BART-Large-CNN model (from Hugging Face Transformers) for abstractive summaries.
* **YouTube Audio Download:** Efficiently downloads audio streams using `yt-dlp`.
* **Long Transcript Handling:** Automatically splits very long transcripts into chunks for stable and effective summarization.
* **Simple Command-Line Interface (CLI):** Easy to run with minimal parameters.
* **Zero API Usage:** Everything runs locally.

---

# 🗂 Project Structure

The project has a clean and simple structure:

Offline-YouTube-Video-Summarizer/├── main.py             # Main CLI – runs the full pipeline├── downloader.py       # Handles YouTube audio downloads (using yt-dlp)├── transcriber.py      # Whisper transcription logic├── summarizer.py       # BART summarization logic├── verify_setup.py     # Checks dependencies and model readiness└── requirements.txt    # Python dependencies
---

# 📦 Requirements

### Python Dependencies

Install these packages using the `requirements.txt` file:

```txt
yt-dlp
openai-whisper
transformers
torch
(Note: torch is the foundation for Whisper and Transformers, and is required.)System PrerequisiteFFmpeg: Required by both yt-dlp and openai-whisper for audio extraction and format conversion.🛠 Installation1️⃣ Clone the RepositoryBashgit clone [https://github.com/your-username/Offline-YouTube-Video-Summarizer.git](https://github.com/your-username/Offline-YouTube-Video-Summarizer.git)
cd Offline-YouTube-Video-Summarizer
2️⃣ Install Python DependenciesBashpip install -r requirements.txt
3️⃣ Install FFmpegDownload and install FFmpeg for your operating system.Download from: https://ffmpeg.org/download.htmlVerify Installation:Bashffmpeg -version
🔍 Verify Your SetupRun the verify_setup.py script to ensure everything is ready:Bashpython verify_setup.py
To also check if the large models can be downloaded and loaded (this is optional but recommended for first-time use):Bashpython verify_setup.py --check-models
💻 UsageBasic CommandRun the entire pipeline by passing a YouTube URL as the positional argument:Bashpython main.py "YOUTUBE_LINK"
Example:Bashpython main.py "[https://www.youtube.com/watch?v=abcdefg](https://www.youtube.com/watch?v=abcdefg)"
This will automatically:Download YouTube audio to the downloads directory.Transcribe it using the default base Whisper model.Summarize the output using the default facebook/bart-large-cnn model.Print the full transcript and summary to your console.Remove the downloaded audio file (--cleanup is the default).⚙️ CLI OptionsFlagDescriptionDefaultChoices/ExampleurlRequired YouTube link (positional).required"https://youtu.be/ID"--whisper-modelWhisper model size for transcription.basetiny, base, small, medium, large--summarizer-modelHugging Face summarization model.facebook/bart-large-cnn(Any suitable model)--output file.txtSave results to file instead of printing to console.console onlysummary.txt--output-dir DIRDirectory to store temporary audio files.downloadstemp_audio--no-cleanupKeep the downloaded audio file after processing.False--transcript-onlySkip the summarization step, outputting only the transcript.False--verboseEnable verbose (DEBUG level) logging.False📘 Example Commands1. Basic summarizationBashpython main.py "[https://youtu.be/VIDEO_ID](https://youtu.be/VIDEO_ID)"
2. Use a smaller Whisper model and save the outputBashpython main.py "[https://youtu.be/VIDEO_ID](https://youtu.be/VIDEO_ID)" --whisper-model small --output my_video_summary.txt
3. Keep the downloaded audio file for later useBashpython main.py "[https://youtu.be/VIDEO_ID](https://youtu.be/VIDEO_ID)" --no-cleanup
🧠 How It Works (The Pipeline)downloader.py: Uses yt-dlp to download the best available audio stream and converts it into a .wav file in the temporary downloads folder.transcriber.py: Loads the specified Whisper model, processes the .wav file, and outputs the full, raw text transcript.summarizer.py:Loads the BART-Large-CNN summarization model.Checks the length of the transcript. If it's too long, it splits the text into manageable chunks.Generates summaries for the chunks and combines them into the final, coherent summary.main.py: Orchestrates the above steps, handles all command-line arguments, and manages the final output (printing or saving to file) and cleanup.
