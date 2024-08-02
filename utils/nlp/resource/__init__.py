import numpy as np

from utils.industry import Company
from utils.inference.resource.infer import get_description
from utils.nlp.resource.prompts import get_product_match_from_company_prompt
from utils.resource import Product, ResourceCode

from .. import query_json

import spacy
nlp = spacy.load("en_core_web_trf")

# import en_core_web_trf
# nlp = en_core_web_trf.load()

def query_product_code_from_company(company: Company, product: Product, guesses: list[ResourceCode]) -> ResourceCode:
    # Using Ollama
    
    # prompt = get_product_match_from_company_prompt(company, product, guesses)
    # print("Prompt: " + prompt)

    # response = query_json(prompt)
    # print(response)

    # product_std = guesses[0].std
    
    # return ResourceCode(product_std, str(response[product_std.value]))
    
    # Using spaCy
    
    input_doc = nlp(company.description + " " + product.description)
    print(input_doc)
    
    similarities = [input_doc.similarity(nlp(get_description(guess))) for guess in guesses]
    print(similarities)
    
    for guess in guesses:
        print(get_description(guess))

    return guesses[np.argmax(similarities)]