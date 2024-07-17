from utils.industry import Company, IndustryCode, IndustryStandard
from utils.inference.industry.infer import get_children, get_common_parent, select_cell
from utils.nlp.industry import infer_industry_code_from_llm

def classify_company(company: Company, to_std: IndustryStandard, guesses: list[IndustryCode]=[]) -> IndustryCode:
    """Classify a company that already has an industry classification under another standard.

    Args:
        company (Company): Company to be classified.
        to_std (IndustryStandard): The industry classification standard to classify the company.
        guesses (list[IndustryCode], optional): Initial list of industry classification codes. Defaults to [].

    Returns:
        IndustryCode: Code of the industry classification matched from the standard provided.
    """

    from_code = company.code
	# print(f"'{from_code.std.value}', '{from_code.value}', '{to_std.value}', '{[c.value for c in guesses]}'")

    if to_std == IndustryStandard.ISIC:
        return IndustryCode(IndustryStandard.ISIC, select_cell(from_code, "ISIC code"))

    if len(guesses) == 0:
        # Find common parent
        common_parent = get_common_parent(from_code, to_std)
        match = common_parent

        while len(get_children(match)) > 0:
            guesses = get_children(match)

            # If there is only one child, that is assumed to be the match
            if len(guesses) == 1:
                match = guesses[0]

            # If there are multiple children, 
            elif len(guesses) > 1:
                match = infer_industry_code_from_llm(company, to_std, guesses)

        return match

    elif len(guesses) == 1:
        return guesses[0]

    # print(f"Given {from_code.std.value} code: {from_code.value}, given {to_std.value} codes: {to_guesses_str}")
    return infer_industry_code_from_llm(company, to_std, guesses)