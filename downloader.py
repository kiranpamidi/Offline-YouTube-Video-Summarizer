#!/usr/bin/env python
# coding: utf-8

# In[3]:


"""
YouTube Audio Downloader Module

This module handles downloading audio from YouTube videos using yt-dlp.
"""
import os
import logging
from pathlib import Path
from typing import Optional
import yt_dlp

logger = logging.getLogger(__name__)


class YouTubeDownloader:
    """Downloads audio from YouTube videos."""

    def __init__(self, output_dir: str = "downloads"):
        """
        Initialize the YouTube downloader.

        Args:
            output_dir: Directory to save downloaded audio files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_audio(self, url: str, video_id: Optional[str] = None) -> str:
        """
        Download audio from a YouTube URL.

        Args:
            url: YouTube video URL
            video_id: Optional video ID for naming the file

        Returns:
            Path to the downloaded audio file

        Raises:
            Exception: If download fails
        """
        try:
            # Extract video ID if not provided
            if video_id is None:
                video_id = self._extract_video_id(url)

            output_path = self.output_dir / f"{video_id}.%(ext)s"

            # Configure yt-dlp options
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": str(output_path),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "wav",
                        "preferredquality": "192",
                    }
                ],
                # Allow progress/info to show when verbose logging enabled
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
            }

            logger.info(f"Downloading audio from: {url}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first to get video details
                info = ydl.extract_info(url, download=False)
                video_title = info.get("title", "Unknown")
                duration = info.get("duration", 0)

                logger.info(f"Video: {video_title}")
                logger.info(f"Duration: {duration} seconds")

                # Download the audio
                ydl.download([url])

                # Find the downloaded file (prefer .wav from postprocessor)
                audio_file = self.output_dir / f"{video_id}.wav"

                if not audio_file.exists():
                    # Try to find any audio file with the video_id
                    audio_files = list(self.output_dir.glob(f"{video_id}.*"))
                    if audio_files:
                        audio_file = audio_files[0]
                    else:
                        raise FileNotFoundError(
                            f"Downloaded audio file not found for {video_id}"
                        )

                logger.info(f"Audio downloaded successfully: {audio_file}")
                return str(audio_file)

        except Exception as e:
            logger.error(f"Error downloading audio: {str(e)}")
            raise Exception(f"Failed to download audio from YouTube: {str(e)}")

    def _extract_video_id(self, url: str) -> str:
        """
        Extract video ID from YouTube URL.

        Args:
            url: YouTube video URL

        Returns:
            Video ID
        """
        import re
        import hashlib

        patterns = [
            r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)",
            r"youtube\.com\/watch\?.*v=([^&\n?#]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # Fallback: use hash of URL
        return hashlib.md5(url.encode()).hexdigest()[:12]

    def cleanup(self, file_path: str):
        """
        Remove downloaded audio file.

        Args:
            file_path: Path to the file to remove
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")


# In[ ]:




