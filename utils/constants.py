from pathlib import Path
from .types import IndustryStandard

# Note: File paths are relative to the 'notebooks' folder,
#       so this could break if used outside of the 'notebooks' folder.

# Data folder path
DATA_PATH = Path("../data")

# Exports folder path
EXPORTS_PATH = Path("../exports")

# Collection of industry standards
STANDARDS = [std for std in IndustryStandard]

UNFORMATTED_INFERENCE_PATHS = {
    IndustryStandard.ISIC: [DATA_PATH / "inference/ISIC Rev. 4.csv"],
    IndustryStandard.NACE: [DATA_PATH / "inference/NACE Rev. 2.xlsx"],
    IndustryStandard.WZ: [(DATA_PATH / "inference/WZ Issue 2008.xls", "Content")],
    IndustryStandard.SSIC: [DATA_PATH / "inference/SSIC 2020 v1.xlsx", DATA_PATH / "inference/SSIC 2020 v2.xlsx"]
}

INFERENCE_PATHS = {
    IndustryStandard.ISIC: EXPORTS_PATH / "inference/ISIC.csv",
    IndustryStandard.NACE: EXPORTS_PATH / "inference/NACE.csv",
    IndustryStandard.WZ: EXPORTS_PATH / "inference/WZ.csv",
    IndustryStandard.SSIC: EXPORTS_PATH / "inference/SSIC.csv"
}

CHUAN_FU_PATH = Path("../Chuan Fu")

MAESTRI_PATH = (DATA_PATH / "Exchanges-database Maestri.xlsx", "MAESTRI")

# Roles of companies in industrial symbiosis
MAESTRI_ROLES = ("Providing", "Intermediate", "Receiving")

CORRESPONDENCE_INFO = {
    "path": CHUAN_FU_PATH / "Standardized codes and corresponding tables - trimmed.xlsx",
    "stds": {
        IndustryStandard.NACE: {
            "sheet_name": "NACE - ISIC - SSIC - WZ",
            "cols": {
                IndustryStandard.NACE: "Code",
                IndustryStandard.ISIC: "ISIC Rev. 4",
                IndustryStandard.SSIC: "SSIC 2020",
                IndustryStandard.WZ: "WZ 2008",
            }
        },
        IndustryStandard.ISIC: {
            "sheet_name": "ISIC-NACE-SSIC-WZ",
            "cols": {
                IndustryStandard.NACE: "NACE Rev. 2",
                IndustryStandard.ISIC: "ISIC Rev. 4",
                IndustryStandard.SSIC: "SSIC 2020",
                IndustryStandard.WZ: "WZ 2008",
            }
        },
        IndustryStandard.SSIC: {
            "sheet_name": "SSIC-ISIC-NACE-WZ",
            "cols": {
                IndustryStandard.NACE: None,
                IndustryStandard.ISIC: "ISIC",
                IndustryStandard.SSIC: "SSIC",
                IndustryStandard.WZ: "WZ",
            }
        },
        IndustryStandard.WZ: {
            "sheet_name": "WZ-ISIC-NACE-SSIC",
            "cols": {
                IndustryStandard.NACE: "NACE Rev. 2",
                IndustryStandard.ISIC: f"ISIC\nRev. 4",
                IndustryStandard.SSIC: "SSIC 2020",
                IndustryStandard.WZ: "WZ 2008",
            }
        }
    }
}

# Standard code difference threshold, 't'
DIFF_THRESHOLD = 10