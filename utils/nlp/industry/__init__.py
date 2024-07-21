from utils.industry import Company, IndustryCode, IndustryStandard

from .. import query_json
from .prompts import get_industry_match_prompt

def query_industry_code(company: Company, to_std: IndustryStandard, guesses: list[IndustryCode]) -> IndustryCode:
	"""Infer an industry classification for a company using a LLM.

	Args:
		company (Company): Company to be classified.
		to_std (IndustryStandard): The industry classification standard to classify the company.
		guesses (list[IndustryCode]): Suggested list of industry classification codes.

	Returns:
		IndustryCode: Code of the inferred industry classification from the standard provided.
	"""

	prompt = get_industry_match_prompt(company, guesses)
	# print("Prompt: " + prompt)

	response = query_json(prompt)
	# print(response)
	
	# Example response:
	# {
	#     "NACE": "2221",
	#     "WZ"  : "22210"
	# }

	return IndustryCode(to_std, str(response[to_std.value]))