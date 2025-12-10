#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Setup Verification Script

This script verifies that all dependencies are correctly installed
and models can be loaded.
"""

import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required packages are installed."""
    logger.info("Checking dependencies...")

    required_packages = {
        "yt_dlp": "yt-dlp",
        "whisper": "openai-whisper",
        "transformers": "transformers",
        "torch": "torch",
    }

    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
            logger.info(f"✓ {package} is installed")
        except ImportError:
            logger.error(f"✗ {package} is NOT installed")
            missing.append(package)

    return missing


def check_ffmpeg():
    """Check if FFmpeg is available."""
    logger.info("Checking FFmpeg...")

    import subprocess

    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            logger.info("✓ FFmpeg is available")
            return True
        else:
            logger.error("✗ FFmpeg is not working correctly")
            return False
    except FileNotFoundError:
        logger.error("✗ FFmpeg is NOT installed")
        logger.error("  Install FFmpeg: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        logger.error(f"✗ Error checking FFmpeg: {str(e)}")
        return False


def check_whisper_model():
    """Check if Whisper can load a model."""
    logger.info("Checking Whisper model loading...")

    try:
        import whisper

        logger.info("  Loading tiny model (this may take a moment)...")
        model = whisper.load_model("tiny")
        logger.info("✓ Whisper model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to load Whisper model: {str(e)}")
        return False


def check_summarizer_model():
    """Check if summarization model can be loaded."""
    logger.info("Checking summarization model loading...")

    try:
        from transformers import pipeline

        logger.info("  Loading BART model (this may take a moment and download ~1.6GB)...")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        logger.info("✓ Summarization model loaded successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to load summarization model: {str(e)}")
        logger.error("  Note: First run will download the model (~1.6GB)")
        return False


def main():
    """Run all verification checks."""
    logger.info("=" * 60)
    logger.info("YouTube Summarizer - Setup Verification")
    logger.info("=" * 60)
    logger.info("")

    all_checks_passed = True

    # Check dependencies
    missing = check_dependencies()
    if missing:
        logger.error("")
        logger.error("Please install missing packages:")
        logger.error(f"  pip install {' '.join(missing)}")
        all_checks_passed = False

    logger.info("")

    # Check FFmpeg
    if not check_ffmpeg():
        all_checks_passed = False

    logger.info("")

    # Check models (optional, may take time)
    if len(sys.argv) > 1 and sys.argv[1] == "--check-models":
        if not check_whisper_model():
            all_checks_passed = False

        logger.info("")

        if not check_summarizer_model():
            all_checks_passed = False

    logger.info("")
    logger.info("=" * 60)

    if all_checks_passed:
        logger.info("✓ All checks passed! You're ready to use the summarizer.")
        logger.info("")
        logger.info("Example usage:")
        logger.info("  python main.py https://www.youtube.com/watch?v=VIDEO_ID")
        return 0
    else:
        logger.error("✗ Some checks failed. Please fix the issues above.")
        logger.info("")
        logger.info("Note: Model checks are optional. Run with --check-models to verify models.")
        return 1


if __name__ == "__main__":
    sys.exit(main())


# In[ ]:




