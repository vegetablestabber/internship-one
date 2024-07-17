from pandas import DataFrame
from tqdm import tqdm

from utils.industry import IndustryStandard
from utils.industry.match import classify_company

from .. import (MAESTRI_DESC_COL, MAESTRI_ROLES, NON_NACE_STDS, NACECompany,
                get_maestri_code_col)
from ..helpers import str_to_industry_codes

def classify_maestri_companies(dfs: list[DataFrame]) -> list[DataFrame]:
    """Classify companies in the MAESTRI dataset from their NACE codes under non-NACE standards.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames.

    Returns:
        list[DataFrame]: MAESTRI DataFrames with matches for non-NACE standards.
    """

    results = []

    l1 = len(max(MAESTRI_ROLES, key=len))
    l2 = len(max([std.value for std in NON_NACE_STDS], key=len))

    # Loop through all company types
    for i in range(len(dfs)):
        df = dfs[i].copy()

        # Role: either 'Providing', 'Intermediate' or 'Receiving'
        role = MAESTRI_ROLES[i]

        # Column: 'NACE code'
        nace_col = get_maestri_code_col(IndustryStandard.NACE)

        # Iterate through all standards except NACE as it is to be compared against
        for std in NON_NACE_STDS:
            code_col = get_maestri_code_col(std)

            df[code_col] = df[code_col].map(lambda text: [code for code in str_to_industry_codes(std, text)])

            tqdm.pandas(desc=("{0:>" + str(l1) + "} companies: NACE -> {1:<" + str(l2) + "}").format(role, std.value))

            df[code_col] = df.progress_apply(lambda row:
                classify_company(NACECompany(row[nace_col], row[MAESTRI_DESC_COL]), std, row[code_col]).value,
                axis=1
            )

            df[code_col] = df[code_col]
        
        results.append(df)

    return results