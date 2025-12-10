#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
Offline Text Summarization Module

This module handles text summarization using transformer models from Hugging Face.
Uses BART model for abstractive summarization, running entirely offline.
"""

import logging
from typing import Optional
from transformers import pipeline
import torch

logger = logging.getLogger(__name__)


class Summarizer:
    """Summarizes text using offline transformer models."""

    def __init__(
        self,
        model_name: str = "facebook/bart-large-cnn",
        max_length: int = 142,
        min_length: int = 56,
        device: Optional[str] = None,
    ):
        """
        Initialize the summarizer.

        Args:
            model_name: Hugging Face model name for summarization
            max_length: Maximum length of the summary
            min_length: Minimum length of the summary
            device: Device to run on ('cpu', 'cuda', or None for auto-detection)
        """
        self.model_name = model_name
        self.max_length = max_length
        self.min_length = min_length
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.summarizer_pipeline = None

        logger.info(f"Initializing summarizer: {model_name} on {self.device}")

    def load_model(self):
        """Load the summarization model."""
        try:
            logger.info(f"Loading summarization model '{self.model_name}'...")
            device_index = 0 if self.device == "cuda" else -1

            # Use pipeline for easier usage
            self.summarizer_pipeline = pipeline(
                "summarization",
                model=self.model_name,
                tokenizer=self.model_name,
                device=device_index,
                framework="pt",
            )

            logger.info("Summarization model loaded successfully")

        except Exception as e:
            logger.error(f"Error loading summarization model: {str(e)}")
            raise Exception(f"Failed to load summarization model: {str(e)}")

    def summarize(self, text: str, max_length: Optional[int] = None, min_length: Optional[int] = None) -> str:
        """
        Summarize the given text.

        Args:
            text: Text to summarize
            max_length: Maximum length of summary (overrides initialization)
            min_length: Minimum length of summary (overrides initialization)

        Returns:
            Summarized text
        """
        if self.summarizer_pipeline is None:
            self.load_model()

        if not text or len(text.strip()) == 0:
            raise ValueError("Input text is empty")

        max_len = max_length or self.max_length
        min_len = min_length or self.min_length

        try:
            logger.info(f"Summarizing text (length: {len(text)} characters)")

            # Handle long texts by chunking
            if len(text) > 1024:
                summary = self._summarize_long_text(text, max_len, min_len)
            else:
                result = self.summarizer_pipeline(
                    text,
                    max_length=max_len,
                    min_length=min_len,
                    do_sample=False,
                )
                summary = result[0]["summary_text"]

            logger.info(f"Summary generated (length: {len(summary)} characters)")

            return summary.strip()

        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise Exception(f"Summarization failed: {str(e)}")

    def _summarize_long_text(self, text: str, max_length: int, min_length: int) -> str:
        """
        Summarize long text by chunking.

        Args:
            text: Long text to summarize
            max_length: Maximum length of final summary
            min_length: Minimum length of final summary

        Returns:
            Summarized text
        """
        # Split text into chunks (sentences)
        sentences = text.split(". ")
        chunk_size = 800  # Characters per chunk
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "

        if current_chunk:
            chunks.append(current_chunk.strip())

        logger.info(f"Splitting text into {len(chunks)} chunks for summarization")

        # Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Summarizing chunk {i+1}/{len(chunks)}")
            try:
                result = self.summarizer_pipeline(
                    chunk,
                    max_length=max_length // max(1, len(chunks)) + 50,
                    min_length=min_length // max(1, len(chunks)) + 10,
                    do_sample=False,
                )
                chunk_summaries.append(result[0]["summary_text"])
            except Exception as e:
                logger.warning(f"Error summarizing chunk {i+1}: {str(e)}")
                # Fallback: use first part of chunk
                chunk_summaries.append(chunk[:200] + "...")

        # Combine chunk summaries
        combined_summary = " ".join(chunk_summaries)

        # If combined summary is still too long, summarize it again
        if len(combined_summary) > 1024:
            logger.info("Combined summary too long, summarizing again...")
            result = self.summarizer_pipeline(
                combined_summary,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
            )
            return result[0]["summary_text"]

        return combined_summary


# In[ ]:




