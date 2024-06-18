from .types import IndustryStandard

# Note: File paths are relative to the 'notebooks' folder,
#       so this could break if used outside of the 'notebooks' folder.

# Data folder path
DATA_PATH = "../data"

# Exports folder path
EXPORTS_PATH = "../exports"

# Collection of industry standards
STANDARDS = [std for std in IndustryStandard]

# File info
FILES = {
    "data": {
        IndustryStandard.ISIC: {
            "paths": [f"{DATA_PATH}/ISIC Rev. 4.csv"]
        },
        IndustryStandard.NACE: {
            "paths": [f"{DATA_PATH}/NACE Rev. 2.xlsx"]
        },
        IndustryStandard.WZ: {
            "paths": [(f"{DATA_PATH}/WZ Issue 2008.xls", "Content")]
        },
        IndustryStandard.SSIC: {
            "paths": [f"{DATA_PATH}/SSIC 2020 v1.xlsx", f"{DATA_PATH}/SSIC 2020 v2.xlsx"]
        }
    },
    "exports": {
        IndustryStandard.ISIC: f"{EXPORTS_PATH}/ISIC.csv",
        IndustryStandard.NACE: f"{EXPORTS_PATH}/NACE.csv",
        IndustryStandard.WZ: f"{EXPORTS_PATH}/WZ.csv",
        IndustryStandard.SSIC: f"{EXPORTS_PATH}/SSIC.csv"
    },
    "correspondence": {
        "path": "../Chuan Fu/Standardized codes and corresponding tables - trimmed.xlsx",
        "std_info": {
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
}