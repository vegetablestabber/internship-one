from utils import DIFF_THRESHOLD
from utils.inference.industry.infer import select_cell

from . import IndustryCode, IndustryStandard

### ASSUMPTION: If the difference of codes of the same level is within a given threshold, then they are equal.

def comparable_codes(lst: list[IndustryCode]) -> list[IndustryCode]:
    """Get comparable industry classifications.

    Args:
        lst (list[IndustryCode]): List of industry classification codes.

    Returns:
        list[IndustryCode]: List of industry classification codes of the same level.
    """

    min_len = min([len(code.value) for code in lst])
    return [IndustryCode(code.std, code.value[:min_len]) if code != None else None for code in lst]

def compare(code1: IndustryCode, code2: IndustryCode) -> int:
    """Compare two industry classifications.

    Args:
        code1 (IndustryCode): Industry classification code.
        code2 (IndustryCode): Industry classification code.

    Returns:
        int: Similarity score.
    """

    if code1 == None or code1.value == "" or code2 == None or code2.value == "":
        return -1

    if code1.std == IndustryStandard.NACE and code2.std == IndustryStandard.ISIC:
        return 1 if select_cell(code1, "ISIC code") == code2.value else 0
    elif code2.std == IndustryStandard.NACE and code1.std == IndustryStandard.ISIC:
        return 1 if select_cell(code2, "ISIC code") == code1.value else 0

    # print("{0:<4} {1:>5} <-> {2:<4} {3:>5}".format(code1.std.value, code1.value, code2.std.value, code2.value))

    if code1 != code2:
        diff = abs(int(code1.value) - int(code2.value))
        return 1 if diff <= DIFF_THRESHOLD else 0
    
    return 1

def compare_multiple(code1: IndustryCode, codes: list[IndustryCode]) -> float:
    """Compare an industry classification against multiple classifications.

    Args:
        code1 (IndustryCode): Industry classification code.
        codes (list[IndustryCode]): List of industry classification codes.

    Returns:
        float: Similarity score.
    """

    codes = comparable_codes([code1, *codes])[1:]
    scores = [compare(code1, code) for code in codes]
    
    return sum(scores) / len(scores)