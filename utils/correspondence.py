from pandas import read_excel
from .types import IndustryStandard
from .constants import CHUAN_FU_PATH

CORRESPONDENCE_PATH = CHUAN_FU_PATH / "Standardized codes and corresponding tables - trimmed.xlsx"

CORRESPONDENCE_SHEET_INFO = {
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

def read_correspondence():
    # Read the MAESTRI dataset as a DataFrame
    dfs = dict()

    for std, info in CORRESPONDENCE_SHEET_INFO.items():
        sheet_name = info["sheet_name"]
        cols = {k: v for k, v in info["cols"].items() if v != None}
        
        df = read_excel(CORRESPONDENCE_PATH, sheet_name=sheet_name, dtype=str)
        
        # Replace NaN values with empty strings
        df = df.fillna("")
        
        df = df[cols.values()]
        df = df.rename(columns={v: f"{k.value} code" if k != std else "Code" for k, v in cols.items()})
        
        for col in df.columns:
            df[col] = df[col].str.replace(r"\.|-", "", regex=True)
        
        df = df.set_index("Code")
        
        dfs[std] = df
    
    return dfs