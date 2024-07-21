from pandas import DataFrame, read_csv

from . import LCIA_PATH

def load_lcia() -> DataFrame:
    df = read_csv(LCIA_PATH)

    # GWP = Global Warming Potential
    # Definition: The Global Warming Potential (GWP) was developed to allow comparisons of the global warming impacts of different gases.
    # Source: https://www.epa.gov/ghgemissions/understanding-global-warming-potentials#:~:text=The%20Global%20Warming%20Potential%20(GWP,warming%20impacts%20of%20different%20gases.

    df = df.rename(columns={
        "lcia_id": "ID",
        "lcia_name": "Company description",
        "geography_name": "Location",
        "isic4_name": "ISIC code",
        "ref_product_name": "Product name",
        "ref_product_description": "Product description",
        "cpc2_1_name": "CPC code"
    })

    cols = ["Company description", "ISIC code", "Product name", "Product description", "CPC code"]

    df = df[cols]

    df["ISIC code"] = df["ISIC code"].map(lambda str: str.split(":")[0])
    df["CPC code"] = df["CPC code"].map(lambda str: str.split(":")[0])

    # df[["Company description", "Product name", "Product description"]] = df[["Company description", "Product name", "Product description"]].replace(r"\n", " ", regex=True)

    # df = df.set_index("ID")

    return df