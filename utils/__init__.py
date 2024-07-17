from pathlib import Path

# Paths
# Note: File paths are relative to the 'notebooks' folder, so this could break if used outside of the 'notebooks' folder.

DATA_PATH = Path("../data")
"""Data folder path."""

EXPORTS_PATH = Path("../exports")
"""Exports folder path."""

# Similarity score options

DIFF_THRESHOLD = 20
"""Standard code difference threshold, 't'."""

# Natural language processing (NLP) options

LLM_ID = "llama3"
"""
Identifier of the large language model (LLM) for Ollama used in this project.
For more on Ollama's supported models, visit https://ollama.com/library.
"""

LLM_OPTIONS = {"temperature": 0.2, "top_k": 10, "top_p": 0.5}
"""LLM options for Ollama."""