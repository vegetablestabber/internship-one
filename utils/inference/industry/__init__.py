from pandas import DataFrame

from utils.industry import IndustryStandard

from .. import INFERENCE_EXPORTS_PATH, INFERENCE_PATH

RAW_INDUSTRY_INFERENCE_FOLDER = INFERENCE_PATH / "industry"
"""Path to the folder containing raw industry classification inference tables."""

RAW_INDUSTRY_INFERENCE_PATHS = {
    IndustryStandard.ISIC: [RAW_INDUSTRY_INFERENCE_FOLDER / "ISIC Rev. 4.csv"],
    IndustryStandard.NACE: [RAW_INDUSTRY_INFERENCE_FOLDER / "NACE Rev. 2.xlsx"],
    IndustryStandard.WZ: [(RAW_INDUSTRY_INFERENCE_FOLDER / "WZ Issue 2008.xls", "Content")],
    IndustryStandard.SSIC: [RAW_INDUSTRY_INFERENCE_FOLDER / "SSIC 2020 v1.xlsx", RAW_INDUSTRY_INFERENCE_FOLDER / "SSIC 2020 v2.xlsx"]
}
"""Paths for the raw industry classification inference tables."""

INDUSTRY_INFERENCE_FOLDER = INFERENCE_EXPORTS_PATH / "industry"
"""Path to the folder containing exported industry classification inference tables."""

INDUSTRY_INFERENCE_PATHS = {
    IndustryStandard.ISIC: INDUSTRY_INFERENCE_FOLDER / "ISIC.csv",
    IndustryStandard.NACE: INDUSTRY_INFERENCE_FOLDER / "NACE.csv",
    IndustryStandard.WZ: INDUSTRY_INFERENCE_FOLDER / "WZ.csv",
    IndustryStandard.SSIC: INDUSTRY_INFERENCE_FOLDER / "SSIC.csv"
}
"""
Paths for the formatted industry classification inference tables.
Note: Run 'notebooks/clean_inference.ipynb' to generate these files if not available.
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