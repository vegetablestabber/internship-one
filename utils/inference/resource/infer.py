from pandas import Series

from utils.resource import ResourceCode

from .io import load_resource_inference

_resource_dfs = load_resource_inference()
 
def select_series(code: ResourceCode) -> Series:
    """Select a certain row as a Series under an resource classification from its inference table.
    
    Args:
        code (ResourceCode): Code for the resource classification.

    Returns:
        Series: Relevant row from the inference table pertaining to the resource classification.
    """

    df = _resource_dfs[code.std]
    
    if code.value in df.index:
        return df.loc[code.value]

    return Series([])

def select_cell(code: ResourceCode, col: str) -> str | None:
    """Select a certain cell under an resource classification from its inference table.
    
    Args:
        code (ResourceCode): Code for the resource classification.
        col (str): Column to lookup.

    Returns:
        str | None: Relevant cell from the inference table pertaining to the resource classification.
    """

    df = _resource_dfs[code.std]

    if code.value in df.index:
        return df.loc[code.value, col]

    return None

def get_level(code: ResourceCode) -> str | None:
    """Get the level of an resource classification.
    
    Args:
        code (ResourceCode): Code for the resource classification.

    Returns:
        str | None: Level of the resource classification.
    """

    return select_cell(code, "Level")

def get_description(code: ResourceCode) -> str | None:
    """Get the description of an resource classification.
    
    Args:
        code (ResourceCode): Code for the resource classification.

    Returns:
        str | None: Description of the resource classification.
    """

    return select_cell(code, "Description")

def get_parent(code: ResourceCode, level=-1) -> ResourceCode | None:
    """Get the parent of an resource classification.
    
    Args:
        code (ResourceCode): Code for the resource classification.
        level (int, optional): Level of the parent. Defaults to -1 for the immediate parent.

    Returns:
        str: Parent of the given resource classification.
    """

    std = code.std
    l = get_level(code)

    if level >= l:
        return None
    
    v = select_cell(code, "Parent")

    # Level == -1 (immediate parent)
    if level == -1:
        return ResourceCode(std, v)
    
    while l > level:
        l = get_level(code)

        if l != level:
            v = select_cell(code, "Parent")
            code = ResourceCode(std, v)
    
    return ResourceCode(std, v)

def get_children(code: ResourceCode) -> list[ResourceCode]:
    """Get the children of an resource classification.

    Args:
        code (ResourceCode): Code for the resource classification.

    Returns:
        list[ResourceCode]: Children of the resource classification.
    """

    df = _resource_dfs[code.std]
    return [ResourceCode(code.std, value) for value in df[df["Parent"] == code.value].index]