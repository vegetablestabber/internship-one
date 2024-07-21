from pandas import DataFrame, read_csv

from utils.industry import IndustryStandard

from . import INDUSTRY_INFERENCE_PATHS

def load_industry_inference() -> dict[IndustryStandard, DataFrame]:
    """Load the industry classification standard inference tables as DataFrames.

    Returns:
        dict[IndustryStandard, DataFrame]: Dictionary containing the inference tables.
    """

    dfs = dict()
    
    for std, path in INDUSTRY_INFERENCE_PATHS.items():
        # Reading from a cleaned CSV
        df = read_csv(path, dtype=str)
        
        # Basic text processing for inferencing ISIC codes using NACE codes as indices
        df.Code = df.Code.str.replace(".", "")
        # df.Level = df.Level.astype("uint8")
        df.Parent = df.Parent.str.replace(".", "")
        df = df.set_index("Code")

        dfs[std] = df
    
    return dfs