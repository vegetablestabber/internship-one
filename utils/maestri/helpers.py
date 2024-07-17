from utils.industry import IndustryCode, IndustryStandard
from utils.inference.industry.infer import get_parent

def simplify_nace_str(text: str) -> str:
    """Remove extra NACE codes to simplify comparisons between other industry classification standards.

    Args:
        text (str): Text including possibly multiple NACE codes.

    Returns:
        str: Only the first code as a string.
    """

    return text.split(",")[0] if "," in text else text.split(";")[0]

def str_to_industry_codes(std: IndustryStandard, text: str) -> list[IndustryCode]:
    """Convert a string from the MAESTRI dataset to a list of industry classification codes.

    Args:
        std (IndustryStandard): Standard of industry classifications.
        text (str): Text containing industry classification codes.

    Returns:
        list[IndustryCode]: List of industry classification codes.
    """

    if text == "":
        return []
    elif ";" in text:
        return [IndustryCode(std, substr) for substr in text.split(";")]
    elif "," in text:
        return [IndustryCode(std, substr) for substr in text.split(",")]
    
    return [IndustryCode(std, text)]

def industry_codes_to_str(codes: list[IndustryCode]) -> str:
    """Convert a list of industry classification codes to a string that is valid within the MAESTRI dataset.

    Args:
        codes (list[IndustryCode]): List of industry classification codes.

    Returns:
        str: Text containing the codes of the industry classifications joined by ';'.
    """

    return ";".join([c.value for c in codes])

def filter_industry_codes_with_common_level_1_parent(code: IndustryCode, codes: list[IndustryCode]) -> list[IndustryCode]:
    """Filter industry classifications with a common level 1 parent.

    Args:
        code (IndustryCode): Industry classification code as reference.
        codes (list[IndustryCode]): List of industry classification codes to be filtered.

    Returns:
        list[IndustryCode]: Filtered list of industry classification codes.
    """

    return [c for c in codes if get_parent(c, level=1).value == get_parent(code, level=1).value]