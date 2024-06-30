from pandas import read_excel
from .constants import DATA_PATH, STANDARDS

MAESTRI_PATH = (DATA_PATH / "Exchanges-database Maestri.xlsx", "MAESTRI")

# Roles of companies in industrial symbiosis
OLD_MAESTRI_ROLES = ("Providing", "Intermediate", "Receiving")

# Roles of companies in industrial symbiosis
NEW_MAESTRI_ROLES = ("Donor", "Intermediary", "Receiver")

# Obtain column name based on the imported MAESTRI dataset, given ICS and company role
get_old_code_col = lambda std, role: f"{std.value} code - {role} industry"

# Obtain concise column name, given ICS and company role
get_new_code_col = lambda std: f"{std.value} code"

get_old_desc_col = lambda role: f"{role} industry (according to original database)"

MAESTRI_DESC_COL = "Company description"

def read_maestri():
    # Importing the dataset
    
    # Read the MAESTRI dataset as a DataFrame
    df = read_excel(MAESTRI_PATH[0], sheet_name=MAESTRI_PATH[1], dtype=str)

    # Replace NaN values with empty strings
    df = df.fillna("")

    # Remove carets, asterisks and hashes
    df.replace([r"\^|\*|#"], "", regex=True, inplace=True)
    
    # Split the main dataset into DataFrames for each role (i.e., provider, intermediary, receiver)
    
    # Aggregate relevant column names for data validation
    cols_list = [[get_old_desc_col(role)] + [get_old_code_col(std, role) for std in STANDARDS] for role in OLD_MAESTRI_ROLES]

    # Obtain subsets within the original dataset for validation
    maestri_dfs = [df[cols].copy() for cols in cols_list]

    # Rename columns within subsets
    for i in range(len(OLD_MAESTRI_ROLES)):
        col_dict = dict()
        old_role = OLD_MAESTRI_ROLES[i]

        col_dict.update({get_old_desc_col(old_role): MAESTRI_DESC_COL})
        
        for std in STANDARDS:
            k = get_old_code_col(std, old_role)
            v = get_new_code_col(std)
            
            col_dict.update({k: v})

        maestri_dfs[i] = maestri_dfs[i].rename(columns=col_dict)
        
        # Drop rows with null values for the NACE code
        # Source: https://stackoverflow.com/questions/29314033/drop-rows-containing-empty-cells-from-a-pandas-dataframe
        std = STANDARDS[i + 1]
        maestri_dfs[i] = maestri_dfs[i][   maestri_dfs[i][get_new_code_col(std)].astype(bool)   ]
    
    return maestri_dfs