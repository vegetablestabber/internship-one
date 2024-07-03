import numpy as np
from pandas import DataFrame

from ..stats import classify_scores, get_count, get_percent
from . import NON_NACE_STDS
from .similarity import get_similarity_col

### By company role and industry classification standard

# Extract all scores by role
get_scores_by_role = lambda dfs, std: [np.array(df[get_similarity_col(std)]) for df in dfs]

classify_scores_by_role = lambda dfs, std, is_percent: classify_scores(get_percent if is_percent else get_count, get_scores_by_role(dfs, std))

### By industry classification standard

# Extract the scores of a given standard
get_scores_by_std = lambda dfs: [np.concatenate(get_scores_by_role(dfs, std)) for std in NON_NACE_STDS]

classify_scores_by_std = lambda dfs, is_percent: classify_scores(get_percent if is_percent else get_count, get_scores_by_std(dfs))

def get_similarity_matrix(dfs, is_percent=False):
    values_dict = classify_scores_by_std(dfs, is_percent)
    return DataFrame.from_dict(values_dict, orient="index", columns=[std.value for std in NON_NACE_STDS]).T