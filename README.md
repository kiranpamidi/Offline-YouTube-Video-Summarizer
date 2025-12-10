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
