import numpy as np
from pandas import DataFrame

from utils.industry import IndustryStandard
from utils.stats import classify_scores, get_count, get_percent

from .. import NON_NACE_STDS, get_maestri_similarity_col

def get_scores_by_role(dfs: list[DataFrame], std: IndustryStandard) -> list[np.array]:
    """Extract similarity scores by role between a given industry classification standard and NACE.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames with similarity scores.
        std (IndustryStandard): Industry classification standard to lookup.

    Returns:
        list[np.array]: List of arrays containing similarity scores, each for a different company role within industrial symbiosis.
    """

    return [np.array(df[get_maestri_similarity_col(std)]) for df in dfs]

def classify_scores_by_role(dfs: list[DataFrame], std: IndustryStandard, is_fraction: bool) -> dict[str, list[int | float]]:
    """Classify similarity scores by role for a given industry classification standard.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames with similarity scores.
        std (IndustryStandard): Industry classification standard to compare.
        is_fraction: Choice for values to be fractions or counts.

    Returns:
        dict[str, list[int | float]]: Dictionary with score categories as keys and counts or fractions of similar matches as values.
    """

    return classify_scores(get_percent if is_fraction else get_count, get_scores_by_role(dfs, std))

def get_scores_by_std(dfs: list[DataFrame]) -> list[np.array]:
    """Extract similarity scores between all non-NACE standards and NACE.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames with similarity scores.

    Returns:
        list[np.array]: List of arrays containing similarity scores.
    """

    return [np.concatenate(get_scores_by_role(dfs, std)) for std in NON_NACE_STDS]

def classify_scores_by_std(dfs: list[DataFrame], is_fraction: bool):
    """Classify similarity scores for all non-NACE standards.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames with similarity scores.
        is_fraction: Choice for values to be fractions or counts.

    Returns:
        dict[str, list[int | float]]: Dictionary with score categories as keys and counts or fractions of similar matches as values.
    """

    return classify_scores(get_percent if is_fraction else get_count, get_scores_by_std(dfs))

def get_similarity_summary(dfs: list[DataFrame], is_fraction=False) -> DataFrame:
    """Summarise the similarity results for non-NACE standards through a DataFrame.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames with similarity scores.
        is_fraction: Choice for values to be fractions or counts.

    Returns:
        DataFrame: Similarity summary.
    """

    values_dict = classify_scores_by_std(dfs, is_fraction)
    return DataFrame.from_dict(values_dict, orient="index", columns=[std.value for std in NON_NACE_STDS]).T