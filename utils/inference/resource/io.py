from pandas import DataFrame, read_csv

from utils.resource import ResourceStandard

from . import RESOURCE_INFERENCE_PATHS

def load_resource_inference() -> dict[ResourceStandard, DataFrame]:
    """Load the resource classification standard inference tables as DataFrames.

    Returns:
        dict[ResourceStandard, DataFrame]: Dictionary containing the inference tables.
    """

    dfs = dict()
    
    for std, path in RESOURCE_INFERENCE_PATHS.items():
        # Reading from a cleaned CSV
        df = read_csv(path)
        
        # Basic text processing for inferencing ISIC codes using NACE codes as indices
        df = df.fillna("")
        df = df.set_index("Code")

        dfs[std] = df
    
    return dfs