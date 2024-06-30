from pathlib import Path
from .types import IndustryStandard

# Note: File paths are relative to the 'notebooks' folder,
#       so this could break if used outside of the 'notebooks' folder.

# Data folder path
DATA_PATH = Path("../data")

# Exports folder path
EXPORTS_PATH = Path("../exports")

CHUAN_FU_PATH = Path("../Chuan Fu")

# Collection of industry standards
STANDARDS = [std for std in IndustryStandard]

# Standard code difference threshold, 't'
DIFF_THRESHOLD = 5