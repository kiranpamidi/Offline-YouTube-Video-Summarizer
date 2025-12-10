#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
Main Application Module

This module provides the CLI interface for the YouTube Video Summarizer.
"""

import argparse
import logging
import sys
from pathlib import Path

from downloader import YouTubeDownloader
from transcriber import Transcriber
from summarizer import Summarizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class YouTubeSummarizer:
    """Main application class that orchestrates the summarization pipeline."""

    def __init__(
        self,
        whisper_model: str = "base",
        summarizer_model: str = "facebook/bart-large-cnn",
        output_dir: str = "downloads",
        cleanup: bool = True,
    ):
        """
        Initialize the YouTube summarizer.

        Args:
            whisper_model: Whisper model size for transcription
            summarizer_model: Hugging Face model for summarization
            output_dir: Directory for temporary downloads
            cleanup: Whether to cleanup downloaded files after processing
        """
        self.downloader = YouTubeDownloader(output_dir=output_dir)
        self.transcriber = Transcriber(model_size=whisper_model)
        self.summarizer = Summarizer(model_name=summarizer_model)
        self.cleanup = cleanup

    def process_video(self, url: str) -> dict:
        """
        Process a YouTube video: download, transcribe, and summarize.

        Args:
            url: YouTube video URL

        Returns:
            Dictionary with 'transcript' and 'summary' keys
        """
        audio_path = None

        try:
            # Step 1: Download audio
            logger.info("=" * 60)
            logger.info("Step 1: Downloading audio from YouTube")
            logger.info("=" * 60)
            audio_path = self.downloader.download_audio(url)

            # Step 2: Transcribe audio
            logger.info("=" * 60)
            logger.info("Step 2: Transcribing audio to text")
            logger.info("=" * 60)
            transcript = self.transcriber.transcribe(audio_path)

            # Step 3: Summarize transcript
            logger.info("=" * 60)
            logger.info("Step 3: Summarizing transcript")
            logger.info("=" * 60)
            summary = ""
            if transcript and len(transcript.strip()) > 0:
                summary = self.summarizer.summarize(transcript)
            else:
                logger.warning("Transcript empty — skipping summarization")

            # Cleanup
            if self.cleanup and audio_path:
                self.downloader.cleanup(audio_path)

            return {"transcript": transcript, "summary": summary, "url": url}

        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            # Cleanup on error
            if audio_path and self.cleanup:
                self.downloader.cleanup(audio_path)
            raise


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Offline YouTube Video Summarizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
  python main.py https://youtu.be/dQw4w9WgXcQ --whisper-model small --no-cleanup
  python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --output summary.txt
        """,
    )

    parser.add_argument("url", type=str, help="YouTube video URL")

    parser.add_argument(
        "--whisper-model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base). Larger models are more accurate but slower.",
    )

    parser.add_argument(
        "--summarizer-model",
        type=str,
        default="facebook/bart-large-cnn",
        help="Hugging Face summarization model (default: facebook/bart-large-cnn)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path for summary (default: print to stdout)",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="downloads",
        help="Directory for temporary downloads (default: downloads)",
    )

    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Keep downloaded audio files after processing",
    )

    parser.add_argument(
        "--transcript-only",
        action="store_true",
        help="Only transcribe, do not summarize",
    )

    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args, unknown = parser.parse_known_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate URL
    if not args.url.startswith(("http://", "https://")):
        logger.error("Invalid URL. Please provide a valid YouTube URL.")
        sys.exit(1)

    try:
        # Initialize summarizer
        summarizer = YouTubeSummarizer(
            whisper_model=args.whisper_model,
            summarizer_model=args.summarizer_model,
            output_dir=args.output_dir,
            cleanup=not args.no_cleanup,
        )

        # Process video
        result = summarizer.process_video(args.url)

        # Output results
        output_text = f"""
{'=' * 60}
YouTube Video Summary
{'=' * 60}
URL: {result['url']}

{'=' * 60}
TRANSCRIPT
{'=' * 60}
{result['transcript']}

"""

        if not args.transcript_only:
            output_text += f"""
{'=' * 60}
SUMMARY
{'=' * 60}
{result['summary']}

"""

        if args.output:
            # Write to file
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output_text, encoding="utf-8")
            logger.info(f"Results saved to: {output_path}")
        else:
            # Print to stdout
            print(output_text)

    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to process video: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# In[ ]:




