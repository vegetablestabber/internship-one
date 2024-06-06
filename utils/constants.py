from .types import IndustryStandard

# Data folder path
DATA_PATH = "data"

# Exports folder path
EXPORTS_PATH = "exports"

# Collection of industry standards
STANDARDS = [std for std in IndustryStandard]

# File names
FILENAMES = {
    "data": {
        IndustryStandard.ISIC: (
            f"{DATA_PATH}/ISIC Rev. 4.csv",
        ),
        IndustryStandard.NACE: (
            f"{DATA_PATH}/NACE Rev. 2.xlsx",
        ),
        IndustryStandard.WZ: (
            (f"{DATA_PATH}/WZ Issue 2008.xls", "Content"),
        ),
        IndustryStandard.SSIC: (
            f"{DATA_PATH}/SSIC 2020 v1.xlsx",
            f"{DATA_PATH}/SSIC 2020 v2.xlsx"
        )
    },
    "exports": {
        IndustryStandard.ISIC: f"{EXPORTS_PATH}/ISIC.csv",
        IndustryStandard.NACE: f"{EXPORTS_PATH}/NACE.csv",
        IndustryStandard.WZ: f"{EXPORTS_PATH}/WZ.csv",
        IndustryStandard.SSIC: f"{EXPORTS_PATH}/SSIC.csv"
    }
}