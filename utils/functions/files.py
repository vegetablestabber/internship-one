from pathlib import Path 
from pandas import read_csv, read_excel

from ..constants import UNFORMATTED_INFERENCE_PATHS, INFERENCE_PATHS, CORRESPONDENCE_INFO

def read_unformatted_inference():
    dfs = dict()
    
    for std, paths in UNFORMATTED_INFERENCE_PATHS.items():
        dfs[std] = []
        
        for path in paths:
            if type(path) == str:
                if ".xls" in path:
                    dfs[std].append(read_excel(path))
                elif ".csv" in path:
                    dfs[std].append(read_csv(path))
            elif type(path) == tuple:
                if ".xls" in path[0]:
                    dfs[std].append(read_excel(path[0], sheet_name=path[1]))
    
    return dfs

def read_correspondence():
    # Read the MAESTRI dataset as a DataFrame
    dfs = dict()
    filename = CORRESPONDENCE_INFO["path"]

    for std, info in CORRESPONDENCE_INFO["stds"].items():
        sheet_name = info["sheet_name"]
        cols = {k: v for k, v in info["cols"].items() if v != None}
        
        df = read_excel(filename, sheet_name=sheet_name, dtype=str)
        
        # Replace NaN values with empty strings
        df = df.fillna("")
        
        df = df[cols.values()]
        df = df.rename(columns={v: f"{k.value} code" if k != std else "Code" for k, v in cols.items()})
        
        for col in df.columns:
            df[col] = df[col].str.replace(r"\.|-", "", regex=True)
        
        df = df.set_index("Code")
        
        dfs[std] = df
    
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

# Save data to new CSV files
def export_inference(d: dict):
    for std, df in d.items():
        filepath = Path(INFERENCE_PATHS[std])  
        filepath.parent.mkdir(parents=True, exist_ok=True)  

        df.to_csv(filepath)