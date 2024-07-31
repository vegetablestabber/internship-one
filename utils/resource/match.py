from utils.industry import Company
from utils.inference.resource.infer import get_children, get_description
from utils.inference.resource.io import load_resource_inference
from utils.nlp.resource import query_product_code_from_company
from utils.resource import Product, ResourceCode, ResourceStandard

from utils.nlp.resource.prompts import get_detailed_company_str, get_detailed_product_str

def find_product_classification(company: Company, product: Product, product_std: ResourceStandard) -> ResourceCode:
    resource_dfs = load_resource_inference()
    inference_df = resource_dfs[product_std]
    
    # print(f"\n{get_detailed_company_str(company)}\n{get_detailed_product_str(product)}")

    guesses = [ResourceCode(product_std, value) for value in inference_df[inference_df.Level == "1"].index]
    match = query_product_code_from_company(company, product, guesses)

    while len(get_children(match)) > 0:
        guesses = get_children(match)
        print([guess.value for guess in guesses])

        # If there is only one child, that is assumed to be the match
        if len(guesses) == 1:
            match = guesses[0]

        # If there are multiple children, 
        elif len(guesses) > 1:
            match = query_product_code_from_company(company, product, guesses)

    print(match.value + ": " + get_description(match))

    return match    