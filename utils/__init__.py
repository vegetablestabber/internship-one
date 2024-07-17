from pathlib import Path

from .industry import IndustryStandard

# Note: File paths are relative to the 'notebooks' folder, so this could break if used outside of the 'notebooks' folder.

DATA_PATH = Path("../data")
"""Data folder path."""

EXPORTS_PATH = Path("../exports")
"""Exports folder path."""

CHUAN_FU_PATH = Path("../Chuan Fu")
"""Path to all of Chuan Fu's files (not included in the project)."""

STANDARDS = [std for std in IndustryStandard]
"""Collection of industry standards."""

DIFF_THRESHOLD = 20
"""Standard code difference threshold, 't'."""