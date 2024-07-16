from pandas import Series

from utils.industry import IndustryCode, IndustryStandard

from .io import load_inference

_inference_dfs = load_inference()
 
def select_series(code: IndustryCode) -> Series:
    """Select a certain row as a Series under an industry classification from its inference table.
    
    Args:
        code (IndustryCode): Code for the industry classification.

    Returns:
        Series: Relevant row from the inference table pertaining to the industry classification.
    """

    df = _inference_dfs[code.std]
    
    if code.value in df.index:
        return df.loc[code.value]

    return Series([])

def select_cell(code: IndustryCode, col: str) -> str | None:
    """Select a certain cell under an industry classification from its inference table.
    
    Args:
        code (IndustryCode): Code for the industry classification.
        col (str): Column to lookup.

    Returns:
        str | None: Relevant cell from the inference table pertaining to the industry classification.
    """

    df = _inference_dfs[code.std]

    if code.value in df.index:
        return df.loc[code.value, col]

    return None

def get_level(code: IndustryCode) -> str | None:
    """Get the level of an industry classification.
    
    Args:
        code (IndustryCode): Code for the industry classification.

    Returns:
        str | None: Level of the industry classification.
    """

    return select_cell(code, "Level")

def get_description(code: IndustryCode) -> str | None:
    """Get the description of an industry classification.
    
    Args:
        code (IndustryCode): Code for the industry classification.

    Returns:
        str | None: Description of the industry classification.
    """

    return select_cell(code, "Description")

def get_parent(code: IndustryCode, level=-1) -> IndustryCode | None:
    """Get the parent of an industry classification.
    
    Args:
        code (IndustryCode): Code for the industry classification.
        level (int): Level of the parent. Defaults to -1 for the immediate parent.

    Returns:
        str: Parent of the given industry classification.
    """

    std = code.std
    l = get_level(code)

    if level >= l:
        return None
    
    v = select_cell(code, "Parent")

    # Level == -1 (immediate parent)
    if level == -1:
        return IndustryCode(std, v)
    
    while l > level:
        l = get_level(code)

        if l != level:
            v = select_cell(code, "Parent")
            code = IndustryCode(std, v)
    
    return IndustryCode(std, v)

def get_children(code: IndustryCode) -> list[IndustryCode]:
    """Get the children of an industry classification.

    Args:
        code (IndustryCode): Code for the industry classification.

    Returns:
        list[IndustryCode]: Children of the industry classification.
    """

    df = _inference_dfs[code.std]
    return [IndustryCode(code.std, value) for value in df[df["Parent"] == code.value].index]

def get_common_parent(code: IndustryCode, other_std: IndustryStandard) -> IndustryCode:
    """Find the common parent of an industry classification with another standard.

    Args:
        code (IndustryCode): Code for the industry classfication standard.
        other_std (IndustryStandard): Other standard from which to find the common parent.

    Returns:
        IndustryCode: Common parent from the other standard.
    """

    to_df = _inference_dfs[other_std]
    level = get_level(code)
    
    if level == 1:
        return IndustryCode(other_std, "")
    
    parent = get_parent(code)
    
    while parent.value not in to_df.index:
        parent = get_parent(parent)
    
    parent = IndustryCode(other_std, parent.value)

    while len(get_children(parent)) == 1 and get_level(parent) < get_level(code) - 1:
        parent = get_children(parent)[0]
    
    return parent