from pandas import DataFrame

from utils import DATA_PATH, EXPORTS_PATH
from utils.industry import IndustryStandard

RAW_INDUSTRY_INFERENCE_PATHS = {
    IndustryStandard.ISIC: [DATA_PATH / "inference/ISIC Rev. 4.csv"],
    IndustryStandard.NACE: [DATA_PATH / "inference/NACE Rev. 2.xlsx"],
    IndustryStandard.WZ: [(DATA_PATH / "inference/WZ Issue 2008.xls", "Content")],
    IndustryStandard.SSIC: [DATA_PATH / "inference/SSIC 2020 v1.xlsx", DATA_PATH / "inference/SSIC 2020 v2.xlsx"]
}
"""Paths for the raw industry classification inference tables"""

INDUSTRY_INFERENCE_PATHS = {
    IndustryStandard.ISIC: EXPORTS_PATH / "inference/ISIC.csv",
    IndustryStandard.NACE: EXPORTS_PATH / "inference/NACE.csv",
    IndustryStandard.WZ: EXPORTS_PATH / "inference/WZ.csv",
    IndustryStandard.SSIC: EXPORTS_PATH / "inference/SSIC.csv"
}
"""
Paths for the formatted industry classification inference tables
Note: Run 'notebooks/clean_inference.ipynb' to generate these files if not available
"""

def default_clean(df: DataFrame):
    """Simple text cleaning for industry classification standard inference DataFrames.

    Args:
        df (DataFrame): Inference DataFrame for an industry classification standard.
    """

    # Normalisation (lowercase strings)
    # lower = lambda x: x.lower() if isinstance(x, str) else x
    
    ## If the dataframe has ISIC code data
    # if "ISIC code" in df:
    #     if "Parent" in df:
    #         df.iloc[:, 2:-1] = df.iloc[:, 2:-1].map(lower)
    #     else:
    #         df.iloc[:, 1:-1] = df.iloc[:, 1:-1].map(lower)
        
    ## If the dataframe doesnt' have ISIC code data
    # else:
    #     df.loc[:, "Description":] = df.loc[:, "Description":].map(lower)
    
    # Replace punctuation with empty strings
    # df.loc[:, "Description":] = df.loc[:, "Description":].replace(r"[^\w\s]+", " ", regex=True)
    
    # Replace newlines and multiple spaces with whitespaces
    # df.replace([r"\n", r" +"], " ", regex=True, inplace=True)
    
    # Remove leading and trailing whitespaces
    df.loc[:, "Description":] = df.loc[:, "Description":].map(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Replace 'and or' with 'or'
    df.replace(r"and/or", "or", regex=True, inplace=True)