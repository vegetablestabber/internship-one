from enum import Enum
from pathlib import Path
from typing import Any

from numpy import dtype
import pandas as pd

from utils import DATA_PATH, EXPORTS_PATH

INFERENCE_PATH = DATA_PATH / "inference"
"""Path to the folder containing inference data."""

INFERENCE_EXPORTS_PATH = EXPORTS_PATH / "inference"
"""Path to the folder containing exported inference data."""

def load_raw_inference(paths: dict[Enum, Any]) -> dict[Enum, list[pd.DataFrame]]:
    """Load raw inference tables as DataFrames.

    Args:
        paths (dict[Enum, Any]): Raw inference table paths.

    Returns:
        dict[Enum, list[DataFrame]]: Dictionary containing the raw inference tables.
    """

    dfs = dict()
    
    for std, paths in paths.items():
        dfs[std] = []
        
        for path in paths:
            if isinstance(path, Path):
                if ".xls" in path.suffix:
                    dfs[std].append(pd.read_excel(path, dtype=str))
                elif ".csv" in path.suffix:
                    dfs[std].append(pd.read_csv(path, dtype=str))
            elif type(path) == tuple:
                if ".xls" in path[0].suffix:
                    dfs[std].append(pd.read_excel(path[0], sheet_name=path[1], dtype=str))
    
    return dfs

def export_inference_to_csv(dfs: dict[Enum, pd.DataFrame], paths: dict[Enum, Any]):
    """Export inference DataFrames to CSV files.

    Args:
        dfs (dict[Enum, DataFrame]): Inference DataFrames.
        paths (dict[Enum, Any]): Paths to export the formatted inference tables.
    """

    for std, df in dfs.items():
        filepath = Path(paths[std])  
        filepath.parent.mkdir(parents=True, exist_ok=True)  

        df.to_csv(filepath)

def insert_levels(df: pd.DataFrame):
    """Insert a column for the levels of a classification standard.

    Args:
        df (DataFrame): Inference DataFrame for a classification standard.
    """

    levels = df.index.str.len()
    df.insert(0, "Level", levels)

def insert_parents(df: pd.DataFrame):
    """Insert a column for the parents of a classification standard.

    Args:
        df (DataFrame): Inference DataFrame for a classification standard.
    """

    parents = []
    history = []
    prev = {"Level": 0, "Code": ""}

    # Iterate through the dataframe to deduce the parent
    for row in df.itertuples():
        prev_level = len(history)
        current_level = row.Level
        current_code = row.Index
        
        ## If the current level is '1'
        if current_level == 1:
            current_parent = ""
            history = [current_code]
            
        ## If the current level is lower than the previous level
        elif current_level > prev_level:
            current_parent = history[prev_level - 1]
            history.append(current_code)
            
        ## If the current level is higher than the previous level
        elif current_level < prev_level:
            current_parent = history[(current_level - 1) - 1]
            del history[current_level - 1:]
            history.append(current_code)
        
        else:
            current_parent = history[(current_level - 1) - 1]
        
        parents.append(current_parent)
        prev.update({"Level": current_level, "Code": current_code})
        
    # Insert the list as a column
    df.insert(1, "Parent", parents)