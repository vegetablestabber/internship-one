from pandas import DataFrame, ExcelWriter, read_excel

from .. import DATA_PATH, EXPORTS_PATH, STANDARDS
from ..types import IndustryStandard

MAESTRI_PATH = (DATA_PATH / "Exchanges-database Maestri.xlsx", "MAESTRI")
"""Path to the MAESTRI dataset and the name of the sheet to be analysed in  the file."""

MAESTRI_ROLES = ("Providing", "Intermediate", "Receiving")
"""Roles of companies in the MAESTRI dataset."""

OLD_MAESTRI_ID_COL = "Database-ID"
"""Old name of the identifier column for an exchange."""

MAESTRI_ID_COL = "Database ID"
"""Name of the identifier column for an exchange."""

MAESTRI_DESC_COL = "Company description"
"""Name of the column describing a company's activity."""

NON_NACE_STDS = [std for std in STANDARDS if std != IndustryStandard.NACE]
"""All industry classification standards except NACE."""

def get_old_code_col(std: IndustryStandard, role: str) -> str:
    """Obtain the old name of the column categorising companies using codes of an industry classification standard.

    Args:
        std (IndustryStandard): Industry classification standard to lookup.
        role (str): Role of the companies.

    Returns:
        str: Old column name.
    """

    return f"{std.value} code - {role} industry"

def get_old_desc_col(role: str) -> str:
    """Obtain the old name of the column describing the activities of companies.

    Args:
        role (str): Role of the company.

    Returns:
        str: Column name.
    """

    return f"{role} industry (according to original database)"

def get_maestri_code_col(std: IndustryStandard) -> str:
    """Obtain the name of the column categorising companies using codes of an industry classification standard.

    Args:
        std (IndustryStandard): Industry classification standard to lookup.

    Returns:
        str: Column name.
    """

    return f"{std.value} code"

def get_maestri_similarity_col(std: IndustryStandard) -> str:
    """Obtain the name of the column for similarity scores.

    Args:
        std (IndustryStandard): Industry classification standard to lookup.

    Returns:
        str: Column name.
    """

    return f"{std.value} code sim. score"

def simplify_nace_str(text: str) -> str:
    """Remove extra NACE codes to simplify comparisons between other industry classification standards.

    Args:
        text (str): Text including possibly multiple NACE codes.

    Returns:
        str: Only the first code as a string.
    """

    return text.split(",")[0] if "," in text else text.split(";")[0]

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

    # "NACE code"
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

def export_maestri_to_excel(dfs: list[DataFrame]):
    """Export the MAESTRI DataFrames to an Excel spreadsheet.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames.
    """
    with ExcelWriter(f"{EXPORTS_PATH}/MAESTRI.xlsx") as writer:
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