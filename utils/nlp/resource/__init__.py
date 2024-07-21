from utils.industry import Company
from utils.nlp.resource.prompts import get_product_match_from_company_prompt
from utils.resource import Product, ResourceCode

from .. import query_json

def query_product_code_from_company(company: Company, product: Product, guesses: list[ResourceCode]) -> ResourceCode:
    prompt = get_product_match_from_company_prompt(company, product, guesses)
    # print("Prompt: " + prompt)

    response = query_json(prompt)
    # print(response)

    product_std = guesses[0].std

    return ResourceCode(product_std, str(response[product_std.value]))