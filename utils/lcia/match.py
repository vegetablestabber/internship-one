from pandas import DataFrame
from tqdm import tqdm

from utils.lcia import ISICCompany
from utils.resource import Product, ResourceStandard
from utils.resource.match import find_product_classification

def find_products_for_companies(df: DataFrame) -> DataFrame:
    isic_col = "ISIC code"
    cpc_col = "CPC code"

    tqdm.pandas(desc="Finding CPC classifications")

    df[cpc_col] = df.progress_apply(lambda row:
        find_product_classification(
            ISICCompany(row[isic_col], row["Company description"]),
            # Product(f"{row['Product name']} {row['Product description']}"),
            Product(row["Product description"]),
            ResourceStandard.CPC
        ).value,
        axis=1
    )