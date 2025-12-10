#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Transcription Module

Uses OpenAI Whisper (openai-whisper package) to transcribe audio locally.
"""

import logging
from typing import Optional
import torch

logger = logging.getLogger(__name__)


class Transcriber:
    """Transcribes audio files using Whisper."""

    def __init__(self, model_size: str = "base", device: Optional[str] = None):
        """
        Initialize the transcriber.

        Args:
            model_size: Whisper model size ('tiny','base','small','medium','large')
            device: 'cpu' or 'cuda' or None for auto-detect
        """
        self.model_size = model_size
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        logger.info(f"Initializing Transcriber: model={model_size} device={self.device}")

    def load_model(self):
        """Load the Whisper model."""
        if self.model is not None:
            return

        try:
            import whisper  # openai-whisper package
            logger.info(f"Loading Whisper model '{self.model_size}' (this may take a while)...")
            # whisper.load_model handles device internally (uses CPU/GPU automatically)
            self.model = whisper.load_model(self.model_size, device=self.device)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            raise

    def transcribe(self, audio_path: str, language: Optional[str] = None, task: str = "transcribe") -> str:
        """
        Transcribe an audio file to text.

        Args:
            audio_path: Path to audio file
            language: Optional ISO language code (e.g. 'en') to force language
            task: 'transcribe' or 'translate'

        Returns:
            Transcript string
        """
        if self.model is None:
            self.load_model()

        try:
            logger.info(f"Transcribing audio: {audio_path}")
            # whisper's transcribe returns a dict with 'text'
            options = {"task": task}
            if language:
                options["language"] = language

            result = self.model.transcribe(audio_path, **options)
            transcript = result.get("text", "").strip()
            logger.info(f"Transcription length: {len(transcript)} characters")
            return transcript
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise


# In[ ]:




