#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
YouTube Video Summarizer Package Initialization

This file makes the components importable as a package,
and it is compatible with Jupyter Notebook and normal Python scripts.
"""

__version__ = "1.0.0"

# Import components using absolute imports (Jupyter-friendly)
try:
    from downloader import YouTubeDownloader
    from transcriber import Transcriber
    from summarizer import Summarizer

except ImportError:
    # If running as a package (installed or proper module)
    from .downloader import YouTubeDownloader
    from .transcriber import Transcriber
    from .summarizer import Summarizer


# In[ ]:




