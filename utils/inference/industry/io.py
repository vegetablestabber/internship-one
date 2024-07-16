from pathlib import Path

from pandas import DataFrame, read_csv, read_excel

from utils.industry import IndustryStandard

from . import INDUSTRY_INFERENCE_PATHS, RAW_INDUSTRY_INFERENCE_PATHS

def load_raw_inference() -> dict[IndustryStandard, list[DataFrame]]:
    """Load the raw industry classification standard inference tables as DataFrames.

    Returns:
        dict[IndustryStandard, list[DataFrame]]: Dictionary containing the raw inference tables.
    """

    dfs = dict()
    
    for std, paths in RAW_INDUSTRY_INFERENCE_PATHS.items():
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

def load_inference() -> dict[IndustryStandard, DataFrame]:
    """Load the industry classification standard inference tables as DataFrames.

    Returns:
        dict[IndustryStandard, DataFrame]: Dictionary containing the inference tables.
    """

    dfs = dict()
    
    for std, path in INDUSTRY_INFERENCE_PATHS.items():
        # Reading from a cleaned CSV
        df = read_csv(path)
        
        # Basic text processing for inferencing ISIC codes using NACE codes as indices
        df["Code"] = df["Code"].str.replace(".", "")
        df["Parent"] = df["Parent"].str.replace(".", "")
        df = df.set_index("Code")
        df = df.fillna("")

        dfs[std] = df
    
    return dfs

def export_inference_to_csv(dfs: list[DataFrame]):
    """Export industry classification standard inference DataFrames to CSV files.

    Args:
        dfs (list[DataFrame]): Industry classification standard inference DataFrames.
    """

    for std, df in dfs.items():
        filepath = Path(INDUSTRY_INFERENCE_PATHS[std])  
        filepath.parent.mkdir(parents=True, exist_ok=True)  

        df.to_csv(filepath)