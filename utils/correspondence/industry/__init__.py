from .. import IndustryStandard

CORRESPONDENCE_SHEET_INFO = {
    IndustryStandard.NACE: {
        "sheet_name": "NACE - ISIC - SSIC - WZ",
        "cols": {
            IndustryStandard.NACE: "Code",
            IndustryStandard.ISIC: "ISIC Rev. 4",
            IndustryStandard.SSIC: "SSIC 2020",
            IndustryStandard.WZ: "WZ 2008",
        }
    },
    IndustryStandard.ISIC: {
        "sheet_name": "ISIC-NACE-SSIC-WZ",
        "cols": {
            IndustryStandard.NACE: "NACE Rev. 2",
            IndustryStandard.ISIC: "ISIC Rev. 4",
            IndustryStandard.SSIC: "SSIC 2020",
            IndustryStandard.WZ: "WZ 2008",
        }
    },
    IndustryStandard.SSIC: {
        "sheet_name": "SSIC-ISIC-NACE-WZ",
        "cols": {
            IndustryStandard.NACE: None,
            IndustryStandard.ISIC: "ISIC",
            IndustryStandard.SSIC: "SSIC",
            IndustryStandard.WZ: "WZ",
        }
    },
    IndustryStandard.WZ: {
        "sheet_name": "WZ-ISIC-NACE-SSIC",
        "cols": {
            IndustryStandard.NACE: "NACE Rev. 2",
            IndustryStandard.ISIC: f"ISIC\nRev. 4",
            IndustryStandard.SSIC: "SSIC 2020",
            IndustryStandard.WZ: "WZ 2008",
        }
    }
}
"""Sheet names and column names of the industry classification standard correspondence spreadsheet."""