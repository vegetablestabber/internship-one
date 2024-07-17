from pandas import DataFrame

from utils.industry import IndustryStandard
from utils.industry.similarity import compare_multiple

from .. import (MAESTRI_DESC_COL, NON_NACE_STDS, NACECode,
                get_maestri_code_col, get_maestri_similarity_col)
from ..helpers import (filter_industry_codes_with_common_level_1_parent,
                       industry_codes_to_str, str_to_industry_codes)

_blacklist = ["", "-"]

def calc_similarity(nace_text: str, other_text: str, other_std: IndustryStandard) -> float:
    """Compare industry classifications contained within strings in the MAESTRI dataset.

    Args:
        nace_text (str): Text containing a NACE code.
        other_text (str): Text containing a list of industry classification codes.
        other_std (IndustryStandard): Standard of the second list of classifications.

    Returns:
        float: Similarity score.
    """

    # If codes do not exist,
    if nace_text in _blacklist or other_text in _blacklist:
        return -1
 
    nace_code = NACECode(nace_text.strip())
    other_codes = str_to_industry_codes(other_std, other_text.strip())
    
    return compare_multiple(nace_code, other_codes)

def validate_maestri_companies(dfs: list[DataFrame]) -> list[DataFrame]:
    """Assign similarity score columns to MAESTRI DataFrames.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames.

    Returns:
        list[DataFrame]: MAESTRI DataFrames with similarity scores.
    """

    results = []

    # NACE column, example: 'Provider NACE code'
    nace_col = get_maestri_code_col(IndustryStandard.NACE)

    # Loop through all company types
    for i in range(len(dfs)):
        df = dfs[i].copy()
        
        # Iterate through all standards except NACE as it is to be compared with
        for std in NON_NACE_STDS:
            # Standard column, example for ISIC: 'Donor ISIC code'
            code_col = get_maestri_code_col(std)

            similarity_col = get_maestri_similarity_col(std)
            
            # Append the similarity score column of a certain standard to the DataFrame for a given role
            df[similarity_col] = df.apply(lambda row: calc_similarity(row[nace_col], row[code_col], std), axis=1)
            
            # Convert the similarity score column data type to 'float'
            df[similarity_col] = df[similarity_col].astype(float)
        
        # List containing new order of columns for readability
        cols = [MAESTRI_DESC_COL, nace_col] + [f(std) for std in NON_NACE_STDS for f in (get_maestri_code_col, get_maestri_similarity_col)]
        
        # Reorder columns for readability
        results[i] = results[i][cols]
    
    return results

def clear_dissimilar_maestri_industry_matches(dfs: list[DataFrame]) -> list[DataFrame]:
    """Clear dissimilar industry matches (similarity score < 1) from a validated MAESTRI dataset.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames with similarity scores.

    Returns:
        list[DataFrame]: MAESTRI DataFrames with matches of scores below 1 cleared.
    """

    results = []

    for i in range(len(dfs)):
        df = dfs[i].copy()
        nace_col = get_maestri_code_col(IndustryStandard.NACE)

        for std in NON_NACE_STDS:
            code_col = get_maestri_code_col(std)
            similarity_col = get_maestri_similarity_col(std)

            df[code_col] = df.apply(lambda row: industry_codes_to_str(
                filter_industry_codes_with_common_level_1_parent(NACECode(row[nace_col]), str_to_industry_codes(std, row[code_col]))
            ), axis=1)

            df.loc[df[similarity_col] < 1, code_col] = ""
            df.loc[df[similarity_col] < 1, similarity_col] = -1

        results.append(df)
    
    return results