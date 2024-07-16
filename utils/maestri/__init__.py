from utils import DATA_PATH, STANDARDS
from utils.industry import Company, IndustryCode, IndustryStandard

class NACECode(IndustryCode):
    def __init__(self, value):
        super().__init__(IndustryStandard.NACE, value)

class NACECompany(Company):
    def __init__(self, code: str, desc: str):
        super().__init__(NACECode(code), desc)

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