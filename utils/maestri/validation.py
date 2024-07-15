from ..inference.infer import select_cell
from ..types import IndustryStandard, NACECode
from . import (MAESTRI_DESC_COL, MAESTRI_ROLES, NON_NACE_STDS,
               get_maestri_code_col, get_maestri_similarity_col)
from .similarity import calc_similarity


def get_similarity(nace_str: str, code_str2: str, std2: IndustryStandard):
    if std2 == IndustryStandard.ISIC:
        nace_code = NACECode(nace_str)
        return 1 if select_cell(nace_code, "ISIC code") == code_str2 else 0
    
    return calc_similarity(nace_str, IndustryStandard.NACE, code_str2, std2)

def validate_maestri(dfs):
    results = [df.copy() for df in dfs]

    # NACE column, example: 'Provider NACE code'
    nace_col = get_maestri_code_col(IndustryStandard.NACE)

    # Loop through all company types
    for i in range(len(MAESTRI_ROLES)):
        df = results[i]
        
        # Iterate through all standards except NACE as it is to be compared with
        for std in NON_NACE_STDS:
            # Standard column, example for ISIC: 'Donor ISIC code'
            code_col = get_maestri_code_col(std)

            similarity_col = get_maestri_similarity_col(std)
            
            # Append the similarity score column of a certain standard to the DataFrame for a given role
            df[similarity_col] = df.apply(lambda row: get_similarity(row[nace_col], row[code_col], std), axis=1)
            
            # Convert the similarity score column data type to 'float'
            df[similarity_col] = df[similarity_col].astype(float)
        
        # List containing new order of columns for readability
        cols = [MAESTRI_DESC_COL, nace_col] + [f(std) for std in NON_NACE_STDS for f in (get_maestri_code_col, get_maestri_similarity_col)]
        
        # Reorder columns for readability
        results[i] = results[i][cols]
    
    return results