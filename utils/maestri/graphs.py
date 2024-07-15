import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from matplotlib.axis import Axis
from pandas import DataFrame

from utils import DIFF_THRESHOLD
from utils.stats import SCORE_CATEGORIES
from utils.types import IndustryStandard

from . import MAESTRI_ROLES, NON_NACE_STDS
from .stats import classify_scores_by_role, classify_scores_by_std

BAR_WIDTH = 0.3
"""Bar width for a similarity plot."""

BAR_COLOURS = {
    "s = -1": "lightgrey",
    "s = 0": "indianred",
    "0 < s < 1": "orange",
    "s = 1": "mediumseagreen"
}
"""
List of named colours for matplotlib.
Source: https://matplotlib.org/stable/gallery/color/named_colors.html
"""

def score_subplot(dfs: list[DataFrame], std: IndustryStandard, ax: Axis, is_percent: bool):
    """Add a similarity subplot to an axis for an industry classification standard from all company roles within the MAESTRI dataset.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames.
        std (IndustryStandard): Industry classification standard to compare.
        ax (Axis): Axis to modify.
        is_percent (bool): Choose percentage values if needed.
    """

    # Obtain the dictionary with the breakdown of values by similarity score
    values_dict = classify_scores_by_role(dfs, std, is_percent)
    
    # Initial bar heights
    bottom = np.zeros(len(NON_NACE_STDS))
    
    # Looping through each category ('s = 0', '0 < s < 1', 's = 1')
    for category, values in values_dict.items():
        # Add bars for each category for all roles ('Donor', 'Intermediary', 'Receiver')
        ax.bar(MAESTRI_ROLES, values, BAR_WIDTH, color=BAR_COLOURS[category], label=category, bottom=bottom)
        
        # Increment the base bar heights
        bottom += values
    
    # Set the title of the subplot
    ax.set_title(std.value)
    
    # Rotate the x-ticks by 45 degrees
    ax.tick_params(axis="x", labelrotation=45)
    
    # If the type of plot is a percentage plot,
    if is_percent:
        # format the y-axis to be percentage values
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

def plot_scores_by_role(dfs: list[DataFrame], is_percent=False):
    """Create a similarity plot (with subplots by role) between NACE and non-NACE standards for the MAESTRI dataset.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames.
        is_percent (bool, optional): Choose percentage values if needed. Defaults to False.
    """

    fig, axs = plt.subplots(ncols=len(NON_NACE_STDS))

    # Add subplots for each standard
    for std, ax in zip(NON_NACE_STDS, axs):
        score_subplot(dfs, std, ax, is_percent)

    # Add a legend to the figure
    handles, labels = plt.gca().get_legend_handles_labels()
    fig.legend(handles, labels, ncol=len(SCORE_CATEGORIES), loc="lower center", bbox_to_anchor=[0.5, -0.05])

    # Set the title of the figure
    fig.suptitle(f"NACE threshold score distribution (t = {DIFF_THRESHOLD})")

    # Add enough padding between subplots to prevent overlapping
    fig.tight_layout()

    plt.show()

def score_plot(dfs, ax, is_percent):
    """Add a similarity subplot to an axis for an industry classification standard from all company roles within the MAESTRI dataset.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames.
        ax (Axis): Axis to modify.
        is_percent (bool): Choose percentage values if needed.
    """

    # x-axis values
    x = [std.value for std in NON_NACE_STDS]
    
    # Obtain the dictionary with the breakdown of values by similarity score
    values_dict = classify_scores_by_std(dfs, is_percent)

    # Initial bar heights
    bottom = np.zeros(len(x))
    
    # Looping through each category ('s = 0', '0 < s < 1', 's = 1')
    for category, values in values_dict.items():
        # Add bars for each category for all standards ('ISIC', 'WZ', 'SSIC')
        ax.bar(x, values, BAR_WIDTH, color=BAR_COLOURS[category], label=category, bottom=bottom)
        
        # Increment the base bar heights
        bottom += values
    
    # If the type of plot is a percentage plot,
    if is_percent:
        # format the y-axis to be percentage values
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

def plot_scores_by_std(dfs: list[DataFrame], is_percent=False):
    """Create a similarity plot between NACE and non-NACE standards for the MAESTRI dataset.

    Args:
        dfs (list[DataFrame]): MAESTRI DataFrames.
        is_percent (bool, optional): Choose percentage values if needed. Defaults to False.
    """

    fig, ax = plt.subplots()

    # Add bars to the figure
    score_plot(dfs, ax, is_percent)

    # Add a legend to the figure
    handles, labels = plt.gca().get_legend_handles_labels()
    fig.legend(handles, labels, ncol=len(SCORE_CATEGORIES), loc="lower center", bbox_to_anchor=[0.5, -0.05])

    # Set the title of the figure
    fig.suptitle(f"NACE threshold score distribution (t = {DIFF_THRESHOLD})")

    plt.show()