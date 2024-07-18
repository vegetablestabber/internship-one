from utils.resource import ResourceStandard

from .. import INFERENCE_PATH, INFERENCE_EXPORTS_PATH

RAW_RESOURCE_INFERENCE_FOLDER = INFERENCE_PATH / "resource"
"""Path to the folder containing resource classification standard inference data."""

RAW_RESOURCE_INFERENCE_PATHS = {
    ResourceStandard.CPC: [RAW_RESOURCE_INFERENCE_FOLDER / "classification_cpc2_1_all.csv"],
}
"""Paths for the raw resource classification inference tables."""

RESOURCE_INFERENCE_FOLDER = INFERENCE_EXPORTS_PATH / "resource"
"""Path to the folder containing exported industry classification inference tables."""

RESOURCE_INFERENCE_PATHS = {
    ResourceStandard.CPC: RESOURCE_INFERENCE_FOLDER / "CPC.csv",
}
"""
Paths for the formatted resource classification inference tables.
Note: Run 'notebooks/clean_inference.ipynb' to generate these files if not available.
"""