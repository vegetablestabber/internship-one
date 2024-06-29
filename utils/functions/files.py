from pathlib import Path 
import pandas as pd

from ..constants import STANDARDS, UNFORMATTED_INFERENCE_PATHS, INFERENCE_PATHS, CORRESPONDENCE_INFO, MAESTRI_PATH, MAESTRI_ROLES
from .maestri import old_col, new_col, new_roles, old_desc_col, new_desc_col

def read_unformatted_inference():
    dfs = dict()
    
    for std, paths in UNFORMATTED_INFERENCE_PATHS.items():
        dfs[std] = []
        
        for path in paths:
            if isinstance(path, Path):
                if ".xls" in path.suffix:
                    dfs[std].append(pd.read_excel(path))
                elif ".csv" in path.suffix:
                    dfs[std].append(pd.read_csv(path))
            elif type(path) == tuple:
                if ".xls" in path[0].suffix:
                    dfs[std].append(pd.read_excel(path[0], sheet_name=path[1]))
    
    return dfs

def read_inference():
    dfs = dict()
    
    for std, path in INFERENCE_PATHS.items():
        # Reading from a cleaned CSV
        df = pd.read_csv(path)
        
        # Basic text processing for inferencing ISIC codes using NACE codes as indices
        df["Code"] = df["Code"].str.replace(".", "")
        df["Parent"] = df["Parent"].str.replace(".", "")
        df = df.set_index("Code")
        df = df.fillna("")

        dfs[std] = df
    
    return dfs

def read_correspondence():
    # Read the MAESTRI dataset as a DataFrame
    dfs = dict()
    filename = CORRESPONDENCE_INFO["path"]

    for std, info in CORRESPONDENCE_INFO["stds"].items():
        sheet_name = info["sheet_name"]
        cols = {k: v for k, v in info["cols"].items() if v != None}
        
        df = pd.read_excel(filename, sheet_name=sheet_name, dtype=str)
        
        # Replace NaN values with empty strings
        df = df.fillna("")
        
        df = df[cols.values()]
        df = df.rename(columns={v: f"{k.value} code" if k != std else "Code" for k, v in cols.items()})
        
        for col in df.columns:
            df[col] = df[col].str.replace(r"\.|-", "", regex=True)
        
        df = df.set_index("Code")
        
        dfs[std] = df
    
    return dfs

def read_maestri():
    # Importing the dataset
    
    # Read the MAESTRI dataset as a DataFrame
    df = pd.read_excel(MAESTRI_PATH[0], sheet_name=MAESTRI_PATH[1], dtype=str)

    # Replace NaN values with empty strings
    df = df.fillna("")

    # Remove carets, asterisks and hashes
    df.replace([r"\^|\*|#"], "", regex=True, inplace=True)
    
    # Split the main dataset into DataFrames for each role (i.e., provider, intermediary, receiver)
    
    # Aggregate relevant column names for data validation
    cols_list = [[old_desc_col(role)] + [old_col(std, role) for std in STANDARDS] for role in MAESTRI_ROLES]

    # Obtain subsets within the original dataset for validation
    maestri_dfs = [df[cols].copy() for cols in cols_list]

    # Rename columns within subsets
    for i in range(len(MAESTRI_ROLES)):
        col_dict = dict()
        old_role = MAESTRI_ROLES[i]
        new_role = new_roles[i]

        col_dict.update({old_desc_col(old_role): new_desc_col(new_role)})
        
        for std in STANDARDS:
            k = old_col(std, old_role)
            v = new_col(std, new_role)
            
            col_dict.update({k: v})

        maestri_dfs[i] = maestri_dfs[i].rename(columns=col_dict)
        
        # Drop rows with null values for the NACE code
        # Source: https://stackoverflow.com/questions/29314033/drop-rows-containing-empty-cells-from-a-pandas-dataframe
        std = STANDARDS[i + 1]
        maestri_dfs[i] = maestri_dfs[i][   maestri_dfs[i][new_col(std, new_role)].astype(bool)   ]

        maestri_dfs[i] = maestri_dfs[i].astype(str)
    
    return maestri_dfs