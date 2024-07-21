from utils.inference.resource.infer import get_description
from utils.nlp.industry.prompts import get_detailed_company_str
from utils.resource import Product, ResourceCode

def get_detailed_product_str(product: Product) -> str:
	return "Product description: " + product.description.replace("\n", " ")

def get_detailed_code_str(code: ResourceCode) -> str:
	return f"{code.std.value} Code: {code.value}\n{get_description(code)}"

def get_product_match_from_company_prompt(company, product, guesses):
    product_std = guesses[0].std

    # prompt = f"Classify the product below given the description of the product and that of the company that produces the product to the most similar of the following {product_std.value} codes using their descriptions. Return a JSON object with exactly one string key-value pair, where the key is '{product_std.value}' and the value is the matched {product_std.value} code. Do NOT return any verbal information that was provided to assist in your task such as the description:\n\n{get_detailed_product_str(product)}\n\n{get_detailed_company_str(company)}"

    prompt = f"Classify the product below given its description and the description of the company that produces it to the most similar of the following {product_std.value} codes using their descriptions. Return a JSON object with exactly one string key-value pair, where the key is '{product_std.value}' and the value is the matched {product_std.value} code. Do NOT return any verbal information that was provided to assist in your task such as the description:\n\n{get_detailed_product_str(product)}\n\n{get_detailed_company_str(company)}"

    for code in guesses:
        prompt += "\n\n" + get_detailed_code_str(code)

    return prompt