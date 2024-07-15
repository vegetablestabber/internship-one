from .. import DATA_PATH, EXPORTS_PATH
from ..types import IndustryStandard

RAW_INFERENCE_PATHS = {
    IndustryStandard.ISIC: [DATA_PATH / "inference/ISIC Rev. 4.csv"],
    IndustryStandard.NACE: [DATA_PATH / "inference/NACE Rev. 2.xlsx"],
    IndustryStandard.WZ: [(DATA_PATH / "inference/WZ Issue 2008.xls", "Content")],
    IndustryStandard.SSIC: [DATA_PATH / "inference/SSIC 2020 v1.xlsx", DATA_PATH / "inference/SSIC 2020 v2.xlsx"]
}
"""Paths for the raw industry classification inference tables"""

INFERENCE_PATHS = {
    IndustryStandard.ISIC: EXPORTS_PATH / "inference/ISIC.csv",
    IndustryStandard.NACE: EXPORTS_PATH / "inference/NACE.csv",
    IndustryStandard.WZ: EXPORTS_PATH / "inference/WZ.csv",
    IndustryStandard.SSIC: EXPORTS_PATH / "inference/SSIC.csv"
}
"""
Paths for the formatted industry classification inference tables
Note: Run 'notebooks/clean_inference.ipynb' to generate these files if not available
"""