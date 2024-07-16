from pandas import DataFrame, ExcelWriter, read_excel

from utils import EXPORTS_PATH, STANDARDS
from utils.industry import IndustryStandard

from . import (MAESTRI_DESC_COL, MAESTRI_ID_COL, MAESTRI_PATH, MAESTRI_ROLES,
               OLD_MAESTRI_ID_COL, get_maestri_code_col, get_old_code_col,
               get_old_desc_col)
from .helpers import simplify_nace_str

def load_maestri() -> list[DataFrame]:
    """Load the MAESTRI dataset as multiple DataFrames.

    Returns:
        list[DataFrame]: List of DataFrames, each representing information about companies participating in different roles within industrial symbiosis.
    """

    ### Importing the dataset
    
    # Read the MAESTRI dataset as a DataFrame
    df = read_excel(MAESTRI_PATH[0], sheet_name=MAESTRI_PATH[1], dtype=str)

    # Replace NaN values with empty strings
    df = df.fillna("")

    # Remove carets, asterisks and hashes
    df.replace([r"\^|\*|#"], "", regex=True, inplace=True)
    
    ### Split the main dataset into DataFrames for each role (i.e., provider, intermediary, receiver)
    
    # Aggregate relevant column names for data validation
    cols_list = [[OLD_MAESTRI_ID_COL, get_old_desc_col(role)] + [get_old_code_col(std, role) for std in STANDARDS] for role in MAESTRI_ROLES]

    # Obtain subsets within the original dataset for validation
    maestri_dfs = [df[cols].copy() for cols in cols_list]

    # Column name: 'NACE code'
    nace_col = get_maestri_code_col(IndustryStandard.NACE)

    ### Rename columns within subsets
    
    for i in range(len(MAESTRI_ROLES)):
        col_dict = dict()
        role = MAESTRI_ROLES[i]

        col_dict.update({
            OLD_MAESTRI_ID_COL: MAESTRI_ID_COL,
            get_old_desc_col(role): MAESTRI_DESC_COL
        })
        
        for std in STANDARDS:
            k = get_old_code_col(std, role)
            v = get_maestri_code_col(std)
            
            col_dict.update({k: v})

        maestri_dfs[i] = maestri_dfs[i].rename(columns=col_dict)
        
        # Drop rows with null values for the NACE code
        # Source: https://stackoverflow.com/questions/29314033/drop-rows-containing-empty-cells-from-a-pandas-dataframe
        maestri_dfs[i] = maestri_dfs[i][   maestri_dfs[i][nace_col].astype(bool)   ]

        maestri_dfs[i][nace_col] = maestri_dfs[i][nace_col].map(simplify_nace_str)

        maestri_dfs[i] = maestri_dfs[i].set_index(MAESTRI_ID_COL)
    
    return maestri_dfs

def export_maestri_to_excel(dfs: list[DataFrame], suffix=""):
    """Export the MAESTRI DataFrames to an Excel spreadsheet.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames.
        suffix (str): Suffix to be added to the exported file. Defaults to ''.
    """
    with ExcelWriter(f"{EXPORTS_PATH}/MAESTRI_{suffix}.xlsx") as writer:
        for i in range(len(dfs)):
            role = MAESTRI_ROLES[i]
            df = dfs[i]
            
            df.to_excel(writer, sheet_name=role, index=False)
            worksheet = writer.sheets[role]
            workbook = writer.book
            
            format = workbook.add_format()
            format.set_align('left')
            format.set_align('vcenter')
            
            # Loop through all columns
            for index, col in enumerate(df):
                series = df[col]
                max_len = max((
                    series.astype(str).map(len).max(),  # Length of largest item
                    len(str(series.name))               # Length of column name/header
                ))
                
                # Set column width
                worksheet.set_column(index, index, max_len, format)