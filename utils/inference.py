from pathlib import Path 
from pandas import read_csv, read_excel
from .types import IndustryStandard
from .constants import DATA_PATH, EXPORTS_PATH

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

def read_unformatted_inference():
    dfs = dict()
    
    for std, paths in UNFORMATTED_INFERENCE_PATHS.items():
        dfs[std] = []
        
        for path in paths:
            if isinstance(path, Path):
                if ".xls" in path.suffix:
                    dfs[std].append(read_excel(path))
                elif ".csv" in path.suffix:
                    dfs[std].append(read_csv(path))
            elif type(path) == tuple:
                if ".xls" in path[0].suffix:
                    dfs[std].append(read_excel(path[0], sheet_name=path[1]))
    
    return dfs

def read_inference():
    dfs = dict()
    
    for std, path in INFERENCE_PATHS.items():
        # Reading from a cleaned CSV
        df = read_csv(path)
        
        # Basic text processing for inferencing ISIC codes using NACE codes as indices
        df["Code"] = df["Code"].str.replace(".", "")
        df["Parent"] = df["Parent"].str.replace(".", "")
        df = df.set_index("Code")
        df = df.fillna("")

        dfs[std] = df
    
    return dfs