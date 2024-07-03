from ..types import IndustryCode, IndustryStandard
from .imports import read_inference

INFERENCE_DFS = read_inference()

def select_series(code: IndustryCode):
    df = INFERENCE_DFS[code.std]
    
    if code.value in df.index:
        return df.loc[code.value]

    return None

def select_cell(code: IndustryCode, col: str) -> str:
    df = INFERENCE_DFS[code.std]

    if code.value in df.index:
        return df.loc[code.value, col]

    return None

get_level = lambda code: select_cell(code, "Level")

get_description = lambda code: select_cell(code, "Description")

def get_parent(code: IndustryCode, level=-1):
    l = get_level(code)

    if level >= l:
        return None
    
    v = select_cell(code, "Parent")

    # Level == -1 (immediate parent)
    if level == -1:
        return IndustryCode(code.std, v)
    
    while l > level:
        l = get_level(code)

        if l != level:
            v = select_cell(code, "Parent")
    
    return IndustryCode(code.std, v)

def get_children(code: IndustryCode):
    df = INFERENCE_DFS[code.std]
    return [IndustryCode(code.std, value) for value in df[df["Parent"] == code.value].index]

# Evaluate the highest common level (HCL)
def get_common_parent(code: IndustryCode, other_std: IndustryStandard):
    to_df = INFERENCE_DFS[other_std]
    level = get_level(code)
    
    if level == 1:
        return IndustryCode(other_std, "")
    
    parent = get_parent(code)
    
    while parent.value not in to_df.index:
        # print(std.value + ": " + c.value)
        parent = get_parent(parent)
        # print(parent.value)
    
    parent = IndustryCode(other_std, parent.value)

    while len(get_children(parent)) == 1 and get_level(parent) < get_level(code) - 1:
        parent = get_children(parent)[0]
    
    return parent