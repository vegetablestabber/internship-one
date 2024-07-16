from pandas import DataFrame, read_excel

from .. import CORRESPONDENCE_PATH
from . import CORRESPONDENCE_SHEET_INFO

def load_industry_correspondence() -> list[DataFrame]:
    """Load the industry classification standard correspondence spreadsheet as multiple DataFrames, each for a standard.

    Returns:
        list[DataFrame]: Industry classification standard correspondence DataFrames.
    """

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